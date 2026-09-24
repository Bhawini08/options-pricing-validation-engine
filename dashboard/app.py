import streamlit as st
from options.models import OptionSpec, black_scholes, crr_binomial, monte_carlo, greeks
from options.validation import convergence_table, greek_surface
st.set_page_config(page_title="Options Validation Engine",layout="wide")
st.title("Options Pricing, Greeks & Model Validation Engine")
s=st.sidebar.number_input("Spot",value=100.0); k=st.sidebar.number_input("Strike",value=100.0); t=st.sidebar.slider("Maturity",0.05,5.0,1.0); v=st.sidebar.slider("Volatility",0.05,1.0,0.20); r=st.sidebar.slider("Rate",-0.02,0.15,0.04)
o=OptionSpec(s,k,t,r,v)
b=black_scholes(o); tree=crr_binomial(o,500); mc=monte_carlo(o,100000)
c1,c2,c3=st.columns(3); c1.metric("BSM",format(b,".4f")); c2.metric("CRR 500",format(tree,".4f")); c3.metric("MC",format(mc["price"],".4f"))
st.subheader("Greeks"); st.json(greeks(o))
st.subheader("Convergence"); st.dataframe(convergence_table(o),use_container_width=True)
surf=greek_surface(o); st.subheader("Delta surface data"); st.dataframe(surf.head(100),use_container_width=True)
