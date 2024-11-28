from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{symbol}/{period}")
async def get_stock_data(symbol: str, period: str):
    try:
        # Fetch stock data
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period)  # Last month's data

        # Format data for ApexCharts
        candlestick_data = [
            {
                "x": str(index.date()),
                "y": [
                    round(row["Open"], 2),
                    round(row["High"], 2),
                    round(row["Low"], 2),
                    round(row["Close"], 2),
                ],
            }
            for index, row in history.iterrows()
        ]
        return {"symbol": symbol, "data": candlestick_data}
    except Exception as e:
        return {"error": str(e)}
