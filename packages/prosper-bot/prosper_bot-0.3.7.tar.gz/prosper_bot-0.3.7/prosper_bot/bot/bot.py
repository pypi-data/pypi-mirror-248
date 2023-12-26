import logging
from datetime import timedelta
from decimal import Decimal
from time import sleep

import humanize
import simplejson as json
from humanize import naturaldelta
from prosper_api.client import Client
from prosper_shared.omni_config import ConfigKey, config_schema

from prosper_bot.allocation_strategy.fixed_target import (
    FixedTargetAllocationStrategy,
    FixedTargetAllocationStrategyTargets,
)
from prosper_bot.cli import (
    DRY_RUN_CONFIG,
    SIMULATE_CONFIG,
    VERBOSE_CONFIG,
    build_config,
)

logger = logging.getLogger(__file__)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.INFO
)

MIN_BID_CONFIG = "bot.min_bid"
STRATEGY_CONFIG = "bot.strategy"

POLL_TIME = timedelta(minutes=1)


@config_schema
def _schema():
    return {
        "prosper_bot": {
            "bot": {
                ConfigKey(
                    "min-bid",
                    "Minimum amount of a loan to purchase.",
                    default=Decimal("25.00"),
                ): Decimal,
                ConfigKey(
                    "strategy",
                    "Strategy for balancing your portfolio.",
                    default=FixedTargetAllocationStrategyTargets.AGGRESSIVE,
                ): FixedTargetAllocationStrategyTargets,
            }
        }
    }


class Bot:
    """Prosper trading bot."""

    def __init__(self, config=None):
        """Initializes the bot with the given argument values."""
        if config is None:
            config = build_config()
        self.config = config
        if self.config.get_as_bool(VERBOSE_CONFIG):
            logging.root.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        self.client = Client(config=self.config)
        self.simulate = self.config.get_as_bool(SIMULATE_CONFIG, False)
        self.dry_run = self.config.get_as_bool(DRY_RUN_CONFIG) or self.simulate
        self.min_bid = self.config.get_as_decimal(MIN_BID_CONFIG, Decimal(25.00))
        self.targets = self.config.get_as_enum(
            STRATEGY_CONFIG, FixedTargetAllocationStrategyTargets
        )

    def run(self):
        """Main loop for the trading bot."""
        cash = None
        sleep_time_delta = POLL_TIME
        while True:
            try:
                cash, sleep_time_delta = self._do_run(cash)
            except KeyboardInterrupt:
                logger.info("Interrupted...")
                break
            except Exception as e:
                logger.warning(
                    f"Caught exception running bot loop: {e}. Continuing after {humanize.naturaldelta(sleep_time_delta)}..."
                )
                logger.debug("", exc_info=e)

            sleep(sleep_time_delta.total_seconds())

    def _do_run(self, cash):
        account = self.client.get_account_info()
        logger.debug(json.dumps(account, indent=2, default=str))
        new_cash = self.min_bid if self.simulate else account.available_cash_balance
        if cash is not None and cash == new_cash:
            return cash, POLL_TIME

        cash = new_cash

        # TODO: Support other allocation strategies
        #   The allocation strategies are designed to be flexible, but that's not possible if we hard-code the strategy
        #   class.
        allocation_strategy = FixedTargetAllocationStrategy(
            self.client, account, targets=self.targets
        )

        invest_amount = self._get_bid_amount(cash, self.min_bid)
        if invest_amount or self.dry_run:
            logger.info("Enough cash is available; searching for loans...")

            listing = next(allocation_strategy)
            lender_yield = listing.lender_yield
            listing_number = listing.listing_number
            if self.dry_run:
                logger.info(
                    f"DRYRUN: Would have purchased ${invest_amount:5.2f} of listing {listing_number} ({listing.prosper_rating}) at {lender_yield * 100:5.2f}%"
                )
            else:
                order_result = self.client.order(listing_number, invest_amount)
                logging.info(
                    f"Purchased ${invest_amount:5.2f} of {listing_number} ({listing.prosper_rating}) at {lender_yield * 100:5.2f}%"
                )
                logging.debug(json.dumps(order_result, indent=2, default=str))

            # Set the sleep time here in case of no matching listings being found (highly unlikely).
            sleep_time_delta = timedelta(seconds=5)
        else:
            sleep_time_delta = POLL_TIME
            logger.info(f"Starting polling every {naturaldelta(sleep_time_delta)}")

        return cash, sleep_time_delta

    @staticmethod
    def _get_bid_amount(cash, min_bid):
        if cash < min_bid:
            return 0
        return min_bid + cash % min_bid


def runner():
    """Entry-point for Python script."""
    Bot().run()


if __name__ == "__main__":
    Bot().run()
