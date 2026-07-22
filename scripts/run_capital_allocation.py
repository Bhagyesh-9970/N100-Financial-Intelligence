"""
Run Capital Allocation Engine
"""

import pandas as pd

from src.analytics.capital_allocation import (
    CapitalAllocationEngine
)

INPUT = "data/interim/validated/cashflow.csv"


def main():

    df = pd.read_csv(INPUT)

    engine = CapitalAllocationEngine()

    result = engine.process(df)

    print(result.head())


if __name__ == "__main__":

    main()