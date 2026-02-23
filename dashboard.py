import streamlit as st
import pandas as pd

from financial_data import DataDownloader
from models import Company, AltmanZScore, MertonModel, CreditDecision
from visualization import (
    plot_z_score,
    plot_default_probability,
    decision_badge,
    plot_comparison_bar
)

st.set_page_config(page_title="Credit Risk Dashboard", layout="centered")

st.title("Credit Risk Decision Engine")
st.write("Altman Z-Score + Merton Default Model")

st.markdown(
    """
    <div style="text-align: center; font-size: 14px; color: gray;">
        <strong>Author:</strong> Ana Sofía Hinojosa Bale
    </div>
    """,
    unsafe_allow_html=True
)

ticker_input = st.text_input(
    "Enter stock tickers (comma-separated)",
    placeholder="AAPL, MSFT, TSLA"
)

if ticker_input:
    tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    results = []

    with st.spinner("Analyzing companies..."):
        for ticker in tickers:
            try:
                company = Company(ticker)

                z_score = AltmanZScore(ticker).calculate()
                default_prob = MertonModel(ticker).calculate_default_probability()
                decision = CreditDecision(z_score, default_prob).decision()

                results.append({
                    "Ticker": ticker,
                    "Z-Score": z_score,
                    "Default Probability": default_prob,
                    "Credit Decision": decision
                })

            except Exception:
                results.append({
                    "Ticker": ticker,
                    "Z-Score": None,
                    "Default Probability": None,
                    "Credit Decision": "ERROR"
                })

    df = pd.DataFrame(results)

    df["Z-Score"] = pd.to_numeric(df["Z-Score"], errors="coerce")
    df["Default Probability"] = pd.to_numeric(df["Default Probability"], errors="coerce")

    st.subheader("Summary Table")

    st.dataframe(
        df.assign(
            **{
                "Z-Score": df["Z-Score"].round(2),
                "Default Probability": df["Default Probability"].apply(
                    lambda x: f"{x:.2%}" if pd.notnull(x) else "—"
                )
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Cross-Company Comparison")
    plot_comparison_bar(df.dropna())

    for _, row in df.iterrows():
        if pd.isna(row["Z-Score"]) or pd.isna(row["Default Probability"]):
            continue

        st.markdown("---")
        st.subheader(f"Company: {row['Ticker']}")

        col1, col2 = st.columns(2)
        col1.metric("Altman Z-Score", f"{row['Z-Score']:.2f}")
        col2.metric("Default Probability", f"{row['Default Probability']:.2%}")

        decision_badge(row["Credit Decision"])

        plot_z_score(row["Z-Score"])
        plot_default_probability(row["Default Probability"])