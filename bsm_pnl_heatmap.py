import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

# BSM formula
def black_scholes(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "Call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

st.title("Black-Scholes Option PnL Heatmap (Red-Green)")

S = st.number_input("Current Spot Price (S)", min_value=0.01, value=100.0)
K = st.number_input("Strike Price (K)", min_value=0.01, value=100.0)
T = st.number_input("Time to Expiry (T in years)", min_value=0.01, value=1.0)
r = st.number_input("Risk-Free Interest Rate (r)", min_value=0.0, value=0.05)
sigma = st.number_input("Volatility (σ)", min_value=0.01, value=0.2)

option_type = st.selectbox("Option Type", ["Call", "Put"])
buy_price = st.number_input("Buy Price of Option", min_value=0.0, value=5.0)

# Heatmap generation
st.markdown("### Heatmap Range Settings")
spot_range = st.slider("Spot Price Range", min_value=50, max_value=150, value=(80, 120))
vol_range = st.slider("Volatility Range (%)", min_value=5, max_value=100, value=(10, 50))

spot_vals = np.round(np.linspace(spot_range[0], spot_range[1], 40), 1)
vol_vals = np.round(np.linspace(vol_range[0]/100, vol_range[1]/100, 40), 3)

pnl_matrix = []
text_matrix = []

for i, v in enumerate(vol_vals):
    row = []
    text_row = []
    for j, s in enumerate(spot_vals):
        price = black_scholes(s, K, T, r, v, option_type)
        pnl = round(price - buy_price, 2)
        row.append(pnl)
        if i % 3 == 0 and j % 3 == 0:
            text_row.append(str(pnl))
        else:
            text_row.append("")
    pnl_matrix.append(row)
    text_matrix.append(text_row)

# red green scale for pnl
colorscale = [
    [0.0, "red"],
    [0.5, "white"],
    [1.0, "green"]
]

# Heatmap generation
fig = go.Figure(data=go.Heatmap(
    z=pnl_matrix,
    x=spot_vals,
    y=np.round(vol_vals * 100, 2),
    colorscale=colorscale,
    zmid=0, 
    colorbar=dict(title='PnL'),
    text=text_matrix,
    texttemplate="%{text}",
    hovertemplate="Spot: %{x}<br>Vol: %{y}%<br>PnL: %{z}<extra></extra>"
))

fig.update_layout(
    xaxis_title="Spot Price",
    yaxis_title="Volatility (%)",
    title="PnL Heatmap (Red = Loss, Green = Profit)",
    height=700
)

st.plotly_chart(fig, use_container_width=True)
