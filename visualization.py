import matplotlib.pyplot as plt
import streamlit as st
from parameters import Z_SCORE_DISTRESS, Z_SCORE_SAFE, DEFAULT_PROB_THRESHOLD


def plot_z_score(z_score):
    fig, ax = plt.subplots(figsize=(6, 1.8))

    ax.axvspan(0, Z_SCORE_DISTRESS, color="red", alpha=0.3, label="Distress Zone")
    ax.axvspan(Z_SCORE_DISTRESS, Z_SCORE_SAFE, color="yellow", alpha=0.3, label="Grey Zone")
    ax.axvspan(Z_SCORE_SAFE, 5, color="green", alpha=0.3, label="Safe Zone")

    ax.axvline(z_score, color="black", linewidth=2)
    ax.set_xlim(0, 5)
    ax.set_yticks([])
    ax.set_title("Altman Z-Score")

    st.pyplot(fig)


def plot_default_probability(default_prob):
    fig, ax = plt.subplots(figsize=(6, 1.8))

    ax.barh(["Default Risk"], [default_prob])
    ax.axvline(DEFAULT_PROB_THRESHOLD, color="red", linestyle="--", label="Max Allowed")
    ax.set_xlim(0, 1)
    ax.set_title("Merton Default Probability")

    st.pyplot(fig)


def decision_badge(decision):
    if decision == "APPROVED":
        st.success("CREDIT APPROVED")
    else:
        st.error("CREDIT DENIED")


def plot_comparison_bar(df):
    """
    Bar plot comparison of Z-Scores and Default Probabilities
    for all analyzed tickers.
    """
    fig, ax1 = plt.subplots(figsize=(8, 4))

    tickers = df["Ticker"]
    z_scores = df["Z-Score"]
    default_probs = df["Default Probability"]

    ax1.bar(tickers, z_scores, color="steelblue", label="Z-Score")
    ax1.axhline(Z_SCORE_SAFE, color="green", linestyle="--", linewidth=1)
    ax1.axhline(Z_SCORE_DISTRESS, color="red", linestyle="--", linewidth=1)
    ax1.set_ylabel("Z-Score")

    ax2 = ax1.twinx()
    ax2.plot(tickers, default_probs, color="darkred", marker="o", label="Default Probability")
    ax2.axhline(DEFAULT_PROB_THRESHOLD, color="darkred", linestyle=":")
    ax2.set_ylabel("Default Probability")

    ax1.set_title("Credit Risk Comparison Across Companies")

    fig.tight_layout()
    st.pyplot(fig)