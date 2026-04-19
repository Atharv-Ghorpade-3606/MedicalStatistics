import streamlit as st

# ----------------------------------
# Page Config
# ----------------------------------
st.set_page_config(
    page_title="Urine Color Scale",
    page_icon="🧪",
    layout="centered"
)
st.title("Urine Test")
st.markdown("Slide to match urine sample color")
st.divider()
# Urine Color Scale
urine_scale = [
    ("Pale Yellow", "#FFFACD", "Well hydrated", "Normal"),
    ("Yellow", "#FFD700", "Normal urine color", "Healthy"),
    ("Dark Yellow", "#DAA520", "Mild dehydration", "Drink more water"),
    ("Amber", "#FFBF00", "Dehydration", "Dehydration risk"),
    ("Orange", "#FF8C00", "Possible liver issue", "Liver disorder"),
    ("Red", "#B22222", "Blood detected", "UTI / Kidney stones"),
    ("Brown", "#654321", "Severe dehydration", "Liver disorder"),
    ("Cloudy", "#E8E8E8", "Possible infection", "UTI")
]

# ----------------------------------
# Slider
# ----------------------------------
color_index = st.slider(
    " ",
    0,
    len(urine_scale) - 1,
    4,
    label_visibility="collapsed"
)

color_name, color_hex, observation, condition = urine_scale[color_index]

# ----------------------------------
# Calculate Thumb Position %
# ----------------------------------
position_percent = (color_index / (len(urine_scale) - 1)) * 100

# ----------------------------------
# CSS Styling
# ----------------------------------
st.markdown(
    f"""
    <style>
    /* Remove tooltip */
    div[data-baseweb="slider"] span {{
        display: none ;
    }}

    /* Slider gradient track */
    div[data-baseweb="slider"] > div {{
        background: linear-gradient(
            to right,
            #FFFACD, #FFD700, #DAA520, #FFBF00,
            #FF8C00, #B22222, #654321, #E8E8E8
        );
        height: 10px;
        border-radius: 10px;
    }}
    /* Slider thumb */
    div[data-baseweb="thumb"] {{
        background-color: {color_hex} !important;
        border: 3px solid black;
        width: 22px;
        height: 22px;
    }}
    /* Floating label */
    .color-label {{
        position: relative;
        top: -38px;
        left: {position_percent}%;
        transform: translateX(-50%);
        font-weight: bold;
        color: {color_hex};
        font-size: 14px;
        background: black;
        padding: 2px 8px;
        border-radius: 8px;
        display: inline-block;
    }}
    </style>
    <div class="color-label">
        {color_name}
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# Result
st.subheader("🩺 Result")
st.success(f"Observed Color: **{color_name}**")
st.warning(f"Inference: **{observation}**")
st.info(f"Possible Condition: **{condition}**")
st.caption("⚠️ Educational purpose only")
