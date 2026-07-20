import logging
logger = logging.getLogger(__name__)


class FinancialRatios:

    # -------------------------------------------------
    # Net Profit Margin
    # -------------------------------------------------

    @staticmethod
    def net_profit_margin(net_profit, sales):

        """
        Net Profit Margin (%)

        Formula:
        (Net Profit / Sales) × 100
        """

        if sales is None or sales == 0:
            return None

        return round((net_profit / sales) * 100, 2)

    # -------------------------------------------------
    # Operating Profit Margin
    # -------------------------------------------------

    @staticmethod
    def operating_profit_margin(operating_profit, sales):

        """
        Operating Profit Margin (%)
        """

        if sales is None or sales == 0:
            return None

        return round((operating_profit / sales) * 100, 2)

    # -------------------------------------------------
    # OPM Cross Check
    # -------------------------------------------------

    @staticmethod
    def check_opm(calculated_opm, source_opm, tolerance=1):

        """
        Compare calculated OPM with source value.

        Returns:
            True  -> Within tolerance
            False -> Difference exceeds tolerance
        """

        if calculated_opm is None or source_opm is None:
            return True

        difference = abs(calculated_opm - source_opm)

        if difference > tolerance:

            logger.warning(
                f"OPM mismatch | Calculated={calculated_opm} "
                f"Source={source_opm}"
            )

            return False

        return True

    # -------------------------------------------------
    # Return on Equity
    # -------------------------------------------------

    @staticmethod
    def roe(net_profit, equity_capital, reserves):

        """
        ROE (%)

        Formula:
        Net Profit /
        (Equity Capital + Reserves)
        """

        equity = equity_capital + reserves

        if equity <= 0:
            return None

        return round((net_profit / equity) * 100, 2)

    # -------------------------------------------------
    # Return on Capital Employed
    # -------------------------------------------------

    @staticmethod
    def roce(
        ebit,
        equity_capital,
        reserves,
        borrowings
    ):

        """
        ROCE (%)

        Formula:
        EBIT /
        (Equity + Reserves + Borrowings)
        """

        capital = (
            equity_capital +
            reserves +
            borrowings
        )

        if capital <= 0:
            return None

        return round((ebit / capital) * 100, 2)

    # -------------------------------------------------
    # Return on Assets
    # -------------------------------------------------

    @staticmethod
    def roa(net_profit, total_assets):

        """
        ROA (%)

        Formula:
        Net Profit /
        Total Assets
        """

        if total_assets is None or total_assets <= 0:
            return None

        return round(
            (net_profit / total_assets) * 100,
            2
        )