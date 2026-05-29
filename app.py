import streamlit as st
from tools.risk_tool import calculate_risk
from run_agent import generate_investment_advice

st.set_page_config(page_title="FinAI – Smart Investment Advisor", layout="centered")

# -------------------- THEME STATE --------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # default theme

# Read URL params
params = st.query_params
if "_theme" in params:
    st.session_state.dark_mode = (params["_theme"] == "dark")

# -------------------- TOGGLE UI (TOP LEFT) --------------------
st.markdown("""
<style>
.theme-toggle-container {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 9999;
}
.switch {
  position: relative;
  display: inline-block;
  width: 55px;
  height: 28px;
}
.switch input { display:none; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #4CAF50;
}
input:checked + .slider:before {
  transform: translateX(26px);
}
</style>
""", unsafe_allow_html=True)

# HTML Toggle Component
st.markdown("""
<div class="theme-toggle-container">
<label class="switch">
  <input type="checkbox" id="theme-toggle">
  <span class="slider"></span>
</label>
</div>

<script>
const toggle = document.getElementById("theme-toggle");
toggle.checked = %s;

toggle.addEventListener("change", (event) => {
    const mode = event.target.checked ? "dark" : "light";
    window.parent.postMessage({themeToggle: mode}, "*");
});
</script>
""" % ("true" if st.session_state.dark_mode else "false"), unsafe_allow_html=True)

# Receive toggle state from JS
if "_theme" in params:
    st.session_state.dark_mode = params["_theme"] == "dark"

# Save theme choice in URL
st.query_params["_theme"] = "dark" if st.session_state.dark_mode else "light"

# -------------------- APPLY THEME COLORS --------------------
BG = "#0D1117" if st.session_state.dark_mode else "#FFFFFF"
TEXT = "#FFFFFF" if st.session_state.dark_mode else "#000000"
INPUT_BG = "#1A1F24" if st.session_state.dark_mode else "#F1F1F1"
CARD = "#161B22" if st.session_state.dark_mode else "#FFFFFF"

# -------------------- FIX TOGGLE VISIBILITY --------------------
toggle_bg = "#444444" if st.session_state.dark_mode else "#C0C0C0"   # dark → dark grey, light → grey
toggle_knob = "#FFFFFF" if st.session_state.dark_mode else "#333333"  # dark → white knob, light → black knob

st.markdown(f"""
<style>
.theme-toggle-container .slider {{
    background-color: {toggle_bg} !important;
    box-shadow: 0px 0px 10px #00000055;
}}
.theme-toggle-container .slider:before {{
    background-color: {toggle_knob} !important;
    box-shadow: 0px 0px 6px #000;
}}
</style>
""", unsafe_allow_html=True)

# Apply background + text theme
st.markdown(f"""
<style>
body, .stApp {{
    background-color: {BG};
    color: {TEXT};
}}
label, h1, h2, h3, p, span {{
    color: {TEXT} !important;
}}
.chat-card {{
    background-color: {CARD};
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
    border: 1px solid #444;
}}
input, textarea {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
}}
</style>
""", unsafe_allow_html=True)


# ---------------------- PAGE HEADER --------------------------------
st.markdown(
    "<h1 style='text-align:center;'>📊 FinAI – Investment Advisor</h1>",
    unsafe_allow_html=True
)
st.write("Your personal AI-powered financial advisor.")


# ---------------------- INPUT FORM ---------------------------------
st.markdown("<h3>🧾 Enter Your Financial Details</h3>", unsafe_allow_html=True)

age = st.number_input("👤 Age", min_value=18, max_value=100, value=25)
salary = st.number_input("💼 Monthly Salary (₹)", min_value=0, value=40000)
expenses = st.number_input("🧾 Monthly Expenses (₹)", min_value=0, value=15000)
savings = st.number_input("🏦 Current Savings (₹)", min_value=0, value=20000)


# ------------------- GENERATE BUTTON -------------------------------
generate_css = """
<style>
.stButton>button {
    background-color: #888888 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
}
.stButton>button:hover {
    background-color: #6e6e6e !important;
}
</style>
"""
st.markdown(generate_css, unsafe_allow_html=True)

if st.button("🚀 Generate Investment Plan"):
    risk = calculate_risk(age, salary, expenses, savings)
    advice = generate_investment_advice(age, salary, expenses, savings, risk)

    st.markdown(f"""
    <div class="chat-card">
        <h3>🎯 Risk Profile: {risk.capitalize()}</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chat-card">
        <h3>📘 Personalized Investment Plan</h3>
        {advice}
    </div>
    """, unsafe_allow_html=True)
