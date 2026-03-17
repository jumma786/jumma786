import argparse
import numpy as np
import pandas as pd


def calculate_metrics(df):
    metrics = {
        "total_sales": df["sales_amount"].sum(),
        "sales_by_region": df.groupby("region")["sales_amount"].sum().sort_values(ascending=False),
        "summary": df.describe(),
        "top_products": df.groupby("product")["sales_amount"].sum().sort_values(ascending=False)
    }
    return metrics


def calculate_forecast(df, periods=7):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df["day_index"] = (df["date"] - df["date"].min()).dt.days
    x = df["day_index"].values
    y = df["sales_amount"].values
    if len(x) < 2:
        return pd.DataFrame([], columns=["date", "forecast_sales"])
    coeffs = np.polyfit(x, y, deg=1)
    slope, intercept = coeffs
    future_days = pd.DataFrame({
        "day_index": range(int(x.max()) + 1, int(x.max()) + periods + 1)
    })
    future_days["forecast_sales"] = intercept + slope * future_days["day_index"]
    future_days["date"] = df["date"].min() + pd.to_timedelta(future_days["day_index"], unit="D")
    return future_days[["date", "forecast_sales"]]


def main():
    parser = argparse.ArgumentParser(description="Sales analysis CLI")
    parser.add_argument("--data", default="sales_sample.csv", help="Path to CSV file")
    parser.add_argument("--plot", action="store_true", help="Display summary plots")
    parser.add_argument("--forecast", action="store_true", help="Display 7-day linear trend forecast")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    metrics = calculate_metrics(df)

    print("First 5 rows:\n", df.head(), "\n")
    print("Summary statistics:\n", metrics["summary"], "\n")
    print(f"Total sales amount: ${metrics['total_sales']:,.2f}")
    print("\nSales by region:\n", metrics["sales_by_region"], "\n")
    print("Top products by sales:\n", metrics["top_products"], "\n")

    if args.forecast:
        forecast_df = calculate_forecast(df)
        print("7-day sales forecast (linear trend):\n", forecast_df)

    if args.plot:
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 3, figsize=(16, 4))
            metrics["sales_by_region"].plot(kind="bar", ax=ax[0], title="Sales by Region")
            metrics["top_products"].plot(kind="bar", ax=ax[1], title="Top Products")
            if args.forecast:
                forecast_df = calculate_forecast(df)
                df_plot = df.copy()
                df_plot["date"] = pd.to_datetime(df_plot["date"])
                df_plot = df_plot.sort_values("date")
                ax[2].plot(df_plot["date"], df_plot["sales_amount"], marker="o", label="Actual")
                ax[2].plot(forecast_df["date"], forecast_df["forecast_sales"], marker="x", label="Forecast")
                ax[2].set_title("Sales Trend and Forecast")
                ax[2].legend()
            else:
                ax[2].text(0.5, 0.5, "Forecast disabled", ha="center", va="center")
                ax[2].set_title("Trend")
            plt.tight_layout()
            plt.show()
        except ImportError:
            print("matplotlib not installed; cannot plot. Install with pip install matplotlib.")


if __name__ == "__main__":
    main()
