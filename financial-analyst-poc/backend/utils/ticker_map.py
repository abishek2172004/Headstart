# backend/utils/ticker_map.py

INDIA_TICKER_MAP = {
    # Major Banks
    "SBI": "SBIN.NS", "SBIN": "SBIN.NS",
    "HDFC": "HDFCBANK.NS", "HDFCBANK": "HDFCBANK.NS",
    "ICICI": "ICICIBANK.NS", "ICICIBANK": "ICICIBANK.NS",
    "AXIS": "AXISBANK.NS", "AXISBANK": "AXISBANK.NS",
    "KOTAK": "KOTAKBANK.NS", "KOTAKBANK": "KOTAKBANK.NS",

    # Top IT
    "INFY": "INFY.NS", "INFOSYS": "INFY.NS",
    "TCS": "TCS.NS", "TATA CONSULTANCY": "TCS.NS",
    "WIPRO": "WIPRO.NS",
    "HCL": "HCLTECH.NS", "HCLTECH": "HCLTECH.NS",
    "TECHM": "TECHM.NS",

    # Conglomerates / Heavyweights
    "RELIANCE": "RELIANCE.NS",
    "LT": "LT.NS", "L&T": "LT.NS",
    "ADANIPORTS": "ADANIPORTS.NS",
    "TITAN": "TITAN.NS",

    # Automobiles
    "MARUTI": "MARUTI.NS",
    "TATAMOTORS": "TATAMOTORS.NS", "TATA MOTORS": "TATAMOTORS.NS",
    "TVS": "TVSMOTOR.NS",
    "BAJAJ": "BAJAJ-AUTO.NS", "BAJAJAUTO": "BAJAJ-AUTO.NS",

    # FMCG / Consumer
    "ITC": "ITC.NS",
    "HUL": "HINDUNILVR.NS", "HINDUSTAN UNILEVER": "HINDUNILVR.NS",
    "NESTLE": "NESTLEIND.NS",
    "ASIANPAINTS": "ASIANPAINT.NS", "ASIANPAINT": "ASIANPAINT.NS",
    "DMART": "DMART.NS", "AVENUE SUPERMARTS": "DMART.NS",

    # Pharma
    "SUNPHARMA": "SUNPHARMA.NS",
    "CIPLA": "CIPLA.NS",
    "LUPIN": "LUPIN.NS",
    "DRREDDY": "DRREDDY.NS", "REDDY": "DRREDDY.NS",

    # Metals / Commodities
    "TATASTEEL": "TATASTEEL.NS",
    "JSW": "JSWSTEEL.NS", "JSWSTEEL": "JSWSTEEL.NS",
    "HINDALCO": "HINDALCO.NS",

    # Energy / Oil / Gas
    "ONGC": "ONGC.NS",
    "POWERGRID": "POWERGRID.NS",
    "NTPC": "NTPC.NS",

    # Telecom
    "JIO": "RELIANCE.NS",  # Jio belongs to Reliance
    "AIRTEL": "BHARTIARTL.NS", "BHARTI": "BHARTIARTL.NS",

    # Finance NBFC
    "BAJAJFIN": "BAJFINANCE.NS", "BAJFINANCE": "BAJFINANCE.NS",
    "BAJAJFINSERV": "BAJAJFINSV.NS",

    # Other Popular Stocks
    "ZOMATO": "ZOMATO.NS",
    "NYKAA": "NYKAA.NS",
    "PAYTM": "PAYTM.NS",
    "MCDOWELL": "MCDOWELL-N.NS",
    "IRCTC": "IRCTC.NS",
}

# Common US symbols are kept deterministic so a temporary Yahoo/network
# failure cannot turn a valid ticker question into a generic LLM response.
US_TICKER_MAP = {
    "AAPL": "AAPL",
    "MSFT": "MSFT",
    "GOOGL": "GOOGL",
    "GOOG": "GOOG",
    "AMZN": "AMZN",
    "NVDA": "NVDA",
    "META": "META",
    "TSLA": "TSLA",
    "NFLX": "NFLX",
    "JPM": "JPM",
    "V": "V",
    "MA": "MA",
    "WMT": "WMT",
    "KO": "KO",
    "PEP": "PEP",
}
