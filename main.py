#%%
import pandas as pd

print('Hello, Wolrd!')
# reads data from excel and creates dataframe
file_path = "C:\\Users\\asusr\\Documents\\Python\\Performance Screen\\data\\"
file_name = "fund_bm_pricing.xlsx"

fund_pricing = pd.read_excel(f"{file_path}{file_name}",
                           sheet_name="fund_data",
                           header=0,
                           names=['Date', 'FN', 'FK', 'FJ', 'FL', 'FM'],
                           index_col='Date'
                           )

# creates a subset dataframe from fund_pricing dataframe
fund_fn_pricing = fund_pricing['FN']


benchmark_pricing = pd.read_excel(f"{file_path}{file_name}",
                           sheet_name="Benchmark_data",
                           header=0,
                           names=['Date', 'FN-Bm', 'FK-Bm', 'FJ-Bm', 'FL-Bm', 'FM-Bm'],
                           index_col='Date'
                           )

# creates a subset dataframe from fund_pricing dataframe
fund_fn_benchmark = benchmark_pricing['FN-Bm']

#%%

# merges fund pricing with fund benchmark pricing 
fund_with_benchmark = pd.merge(fund_fn_pricing, fund_fn_benchmark,
                               how='outer',
                               on='Date')

fbm_monthly = fund_with_benchmark.resample('M').ffill()

# need a table that matches fund and benchmark pricing

# %%
# daily TE
fund_with_benchmark['fund_rtn'] = fund_with_benchmark['FN'].pct_change()
fund_with_benchmark['bm_rtn'] = fund_with_benchmark['FN-Bm'].pct_change()
fund_with_benchmark['tracking_error'] = fund_with_benchmark['fund_rtn'] - fund_with_benchmark['bm_rtn']

fund_tracking_error_D = fund_with_benchmark['tracking_error'].std()
print(f'Daily tracking error is {fund_tracking_error_D:.2%}')

# monthly TE
fbm_monthly['fund_rtn'] = fbm_monthly['FN'].pct_change()
fbm_monthly['bm_rtn'] = fbm_monthly['FN-Bm'].pct_change()
fbm_monthly['tracking_error'] = fbm_monthly['fund_rtn'] - fbm_monthly['bm_rtn']

fund_tracking_error_M = fbm_monthly['tracking_error'].std()
fund_tracking_error_9M = fund_tracking_error_M
print(f'Monthly tracking error is {fund_tracking_error_M:.2%}')

# %%
# reading - https://www.cfainstitute.org/en/research/cfa-digest/2013/11/whats-wrong-with-multiplying-by-the-square-root-of-twelve-digest-summary
