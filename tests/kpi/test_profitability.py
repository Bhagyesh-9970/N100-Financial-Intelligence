from src.analytics.ratios import FinancialRatios


print("=" * 60)
print("SPRINT 2 DAY 08")
print("PROFITABILITY RATIO TESTS")
print("=" * 60)

print()

print("Net Profit Margin")

print(
    FinancialRatios.net_profit_margin(
        120,
        1000
    )
)

print()

print("Operating Profit Margin")

print(
    FinancialRatios.operating_profit_margin(
        240,
        1200
    )
)

print()

print("ROE")

print(
    FinancialRatios.roe(
        150,
        400,
        600
    )
)

print()

print("ROCE")

print(
    FinancialRatios.roce(
        220,
        500,
        700,
        300
    )
)

print()

print("ROA")

print(
    FinancialRatios.roa(
        150,
        5000
    )
)

print()

print("OPM Cross Check")

print(
    FinancialRatios.check_opm(
        20.1,
        20.4
    )
)

print()

print("All Profitability Tests Completed Successfully.")