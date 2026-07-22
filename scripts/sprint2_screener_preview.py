import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def main():

    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity
        FROM financial_ratios
        WHERE return_on_equity_pct > 15
          AND debt_to_equity < 1
        ORDER BY return_on_equity_pct DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    print("=" * 60)
    print("SPRINT 2 SCREENER PREVIEW")
    print("=" * 60)

    print(
        f"\nMatching rows: {len(df)}"
    )

    print("\nResults:")

    if df.empty:

        print("No companies matched the criteria.")

    else:

        print(
            df.to_string(
                index=False
            )
        )

    print("\nValidation:")

    if 15 <= len(df) <= 50:

        print(
            "[PASS] Result count is between 15 and 50."
        )

    else:

        print(
            "[REVIEW] Result count is outside "
            "the expected 15-50 range."
        )


if __name__ == "__main__":

    main()