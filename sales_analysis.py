import argparse
import pandas as pd


def calculate_metrics(df):
    metrics = {
        "total_sales": df["sales_amount"].sum(),
        "sales_by_region": df.groupby("region")["sales_amount"].sum().sort_values(ascending=False),
        "summary": df.describe(),
        "top_products": df.groupby("product")["sales_amount"].sum().sort_values(ascending=False)
    }
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Sales analysis CLI")
    parser.add_argument("--data", default="sales_sample.csv", help="Path to CSV file")
    parser.add_argument("--plot", action="store_true", help="Display summary plots")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    metrics = calculate_metrics(df)

    print("First 5 rows:\n", df.head(), "\n")
    print("Summary statistics:\n", metrics["summary"], "\n")
    print(f"Total sales amount: ${metrics['total_sales']:,.2f}")
    print("\nSales by region:\n", metrics["sales_by_region"], "\n")
    print("Top products by sales:\n", metrics["top_products"], "\n")

    if args.plot:
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(1, 2, figsize=(12, 4))
            metrics["sales_by_region"].plot(kind="bar", ax=ax[0], title="Sales by Region")
            metrics["top_products"].plot(kind="bar", ax=ax[1], title="Top Products")
            plt.tight_layout()
            plt.show()
        except ImportError:
            print("matplotlib not installed; cannot plot. Install with pip install matplotlib.")


if __name__ == "__main__":
    main()
