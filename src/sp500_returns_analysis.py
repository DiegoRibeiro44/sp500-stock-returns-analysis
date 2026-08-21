from __future__ import annotations

import argparse
from pathlib import Path

import kagglehub
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import kstest, shapiro


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"


def download_dataset() -> Path:
    return Path(kagglehub.dataset_download("camnugent/sandp500"))


def load_data(dataset_path: Path) -> pd.DataFrame:
    data = pd.read_csv(dataset_path / "all_stocks_5yr.csv")
    data["date"] = pd.to_datetime(data["date"])
    return data


def analyze_ticker(data: pd.DataFrame, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = data.loc[data["Name"] == ticker].sort_values("date").copy()
    df = df.dropna().drop_duplicates()
    df = df.loc[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df["Return"] = df["close"].pct_change()
    return df.dropna(subset=["Return"])


def save_price_volume_plot(df: pd.DataFrame, ticker: str) -> None:
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.plot(df["date"], df["close"], color="steelblue")
    plt.title(f"Closing Price - {ticker}")
    plt.subplot(1, 2, 2)
    plt.plot(df["date"], df["volume"], color="darkorange")
    plt.title(f"Volume - {ticker}")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{ticker.lower()}_price_volume.png", dpi=150)
    plt.close()


def save_returns_distribution(df: pd.DataFrame, ticker: str) -> None:
    plt.figure(figsize=(10, 6))
    sns.histplot(df["Return"], kde=True, color="teal")
    plt.title(f"Daily Returns Distribution - {ticker}")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{ticker.lower()}_returns_distribution.png", dpi=150)
    plt.close()


def build_report(df: pd.DataFrame, ticker: str) -> str:
    shapiro_test = shapiro(df["Return"])
    ks_test = kstest(df["Return"], "norm", args=(df["Return"].mean(), df["Return"].std()))
    negative_return_probability = (df["Return"] < 0).mean()
    return f"""# SP500 Returns Analysis

Ticker: {ticker}
Date range: {df["date"].min().date()} to {df["date"].max().date()}

## Return Summary
{df["Return"].describe().to_string()}

## Normality Tests
- Shapiro-Wilk: statistic={shapiro_test.statistic:.6f}, p-value={shapiro_test.pvalue:.6f}
- Kolmogorov-Smirnov: statistic={ks_test.statistic:.6f}, p-value={ks_test.pvalue:.6f}

## Probability of Negative Return
{negative_return_probability:.2%}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze daily returns for an S&P 500 ticker.")
    parser.add_argument("--ticker", default="AAPL")
    parser.add_argument("--start-date", default="2014-01-01")
    parser.add_argument("--end-date", default="2018-12-31")
    return parser.parse_args()


def main() -> None:
    sns.set_theme(style="whitegrid")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    args = parse_args()
    data = load_data(download_dataset())
    analyzed = analyze_ticker(data, args.ticker.upper(), args.start_date, args.end_date)

    save_price_volume_plot(analyzed, args.ticker.upper())
    save_returns_distribution(analyzed, args.ticker.upper())

    report = build_report(analyzed, args.ticker.upper())
    report_path = OUTPUTS_DIR / f"{args.ticker.lower()}_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
