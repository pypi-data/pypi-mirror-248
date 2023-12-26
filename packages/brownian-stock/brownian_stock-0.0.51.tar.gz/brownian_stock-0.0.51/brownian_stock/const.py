DEFAULT_REPOSITORY_DIR = "./jquants"
DEFAULT_DB_PATH = "./db.sqlite3"

# DataFrame操作用の定数
COL_STOCK_CODE = "Code"
COL_COMPANY_NAME = "CompanyName"
COL_MARKET = "MarketCode"
COL_SECTOR = "Sector17Code"
COL_SECTOR_DETAIL = "Sector33Code"
COL_DATE = "Date"

COL_OPEN = "Open"
COL_CLOSE = "Close"
COL_HIGH = "High"
COL_LOW = "Low"
COL_TURNOVER_VALUE = "TurnoverValue"
COL_TRADING_VOLUME = "Volume"
COL_ADJUSTMENT_FACTOR = "AdjustmentFactor"

# Index系の定数
COL_INDEX_VALUE = "IndexValue"

COL_LIST = [
    COL_STOCK_CODE,
    COL_COMPANY_NAME,
    COL_MARKET,
    COL_DATE,
    COL_TRADING_VOLUME,
]

# Stockの特徴量
KEY_STOCK_CODE = "STOCK_CODE"
KEY_COMPANY_NAME = "COMPANY_NAME"
KEY_MARKET = "MARKET"
KEY_INDUSTRY_TYPE = "INDUSTRY_TYPE"
KEY_CURRENT_PRICE = "CURRENT_PRICE"
KEY_TRADING_VOLUME = "TRADING_VOLUME"
KEY_MU = "MU"
KEY_SIGMA = "SIGMA"
KEY_SHAPR_RATIO = "SHARP_RATIO"

# Statementsの特徴量
STATEMENTS_HASH = "DisclosureNumber"
STATEMENTS_STOCK_CODE = "Code"
STATEMENTS_COMPANY_NAME = "CompanyName"
STATEMENTS_DATE = "DisclosedDate"
STATEMENTS_FISCAL_YEAR_START = "CurrentFiscalYearStartDate"
STATEMENTS_FISCAL_YEAR_END = "CurrentFiscalYearEndDate"

STATEMENTS_QUARTER = "TypeOfCurrentPeriod"
STATEMENTS_TYPE_OF_DOCUMENT = "TypeOfDocument"
STATEMENTS_STOCK_NUM = "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock"
STATEMENTS_TREASURY_STOCK_NUM = "NumberOfTreasuryStockAtTheEndOfFiscalYear"
STATEMENTS_NET_SALES = "NetSales"
STATEMENTS_PROFIT = "Profit"
STATEMENTS_ASSETS = "TotalAssets"
STATEMENTS_EQUITY = "Equity"

STATEMENTS_FORECAST_NET_SALES = "ForecastNetSales"
STATEMENTS_FORECAST_PROFIT = "ForecastProfit"


# 配当系
STATEMENTS_DIVIDEND_RESULT_1Q = "ResultDividendPerShare1stQuarter"
STATEMENTS_DIVIDEND_RESULT_2Q = "ResultDividendPerShare2ndQuarter"
STATEMENTS_DIVIDEND_RESULT_3Q = "ResultDividendPerShare3rdQuarter"
STATEMENTS_DIVIDEND_RESULT_4Q = "ResultDividendPerShareFiscalYearEnd"
STATEMENTS_DIVIDEND_RESULT = "ResultDividendPerShareAnnual"

STATEMENTS_DIVIDEND_FORECAST_1Q = "ForecastDividendPerShare1stQuarter"
STATEMENTS_DIVIDEND_FORECAST_2Q = "ForecastDividendPerShare2ndQuarter"
STATEMENTS_DIVIDEND_FORECAST_3Q = "ForecastDividendPerShare3rdQuarter"
STATEMENTS_DIVIDEND_FORECAST_4Q = "ForecastDividendPerShareFiscalYearEnd"
STATEMENTS_DVIDEND_FORECAST = "ForecastDividendPerShareAnnual"


SECTOR_DETAIL_LIST = [
    "50",
    "1050",
    "2050",
    "3050",
    "3100",
    "3150",
    "3200",
    "3250",
    "3300",
    "3350",
    "3400",
    "3450",
    "3500",
    "3550",
    "3600",
    "3650",
    "3700",
    "3750",
    "3800",
    "4050",
    "5050",
    "5100",
    "5150",
    "5200",
    "5250",
    "6050",
    "6100",
    "7050",
    "7100",
    "7150",
    "7200",
    "8050",
    "9050",
    "9999",
]
