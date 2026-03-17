import pandas as pd
from sales_analysis import calculate_metrics, calculate_forecast


def test_calculate_metrics_total_sales():
    df = pd.DataFrame({
        "region": ["North", "South", "North"],
        "product": ["Widget", "Gadget", "Widget"],
        "sales_amount": [100.0, 200.0, 150.0],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
    })
    metrics = calculate_metrics(df)
    assert metrics["total_sales"] == 450.0
    assert metrics["sales_by_region"]["North"] == 250.0
    assert metrics["sales_by_region"]["South"] == 200.0
    assert metrics["top_products"]["Widget"] == 250.0
    assert metrics["top_products"]["Gadget"] == 200.0


def test_calculate_forecast_length():
    df = pd.DataFrame({
        "region": ["North", "South", "North"],
        "product": ["Widget", "Gadget", "Widget"],
        "sales_amount": [100.0, 200.0, 150.0],
        "date": ["2026-01-01", "2026-01-02", "2026-01-03"],
    })
    forecast = calculate_forecast(df, periods=3)
    assert len(forecast) == 3
