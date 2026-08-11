import pandas as pd
files=['data/interim/cleaned/companies.csv','data/interim/cleaned/cashflow.csv','data/interim/cleaned/profitandloss.csv','data/interim/cleaned/balancesheet.csv','data/interim/cleaned/financial_ratios.csv','data/interim/cleaned/analysis.csv']
for f in files:
    df=pd.read_csv(f)
    print(f, df.shape)
    print(df.columns.tolist()[:40])
    print(df.head(2).to_string(index=False))
    print('---')
