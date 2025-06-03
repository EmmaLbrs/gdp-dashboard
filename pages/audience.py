import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("Audience")

# Initial data
audience_data = pd.DataFrame([
    {"Event": "Tool Tuesday", "Year": "2024", "Audience Type": "General", "Participation Level": "Active"},
    {"Event": "Frauen* im Fokus", "Year": "2024", "Audience Type": "Specialized", "Participation Level": "Active"},
    {"Event": "Datencafe", "Year": "2024", "Audience Type": "General", "Participation Level": "Passive"},
    {"Event": "Blauer Salon", "Year": "2024", "Audience Type": "Specialized", "Participation Level": "Passive"},
])

# Value mappings
x_map = {"General": 0.2, "Medium": 0.5, "Specialized": 0.8}
y_map = {"Passive": 0.2, "Medium": 0.5, "Active": 0.8}

# Editable Table
st.markdown("### Edit Audience Data")
edited_df = st.data_editor(
    audience_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Audience Type": st.column_config.SelectboxColumn(options=["General", "Medium", "Specialized"]),
        "Participation Level": st.column_config.SelectboxColumn(options=["Passive", "Medium", "Active"]),
        "Year": st.column_config.TextColumn(help="Enter year as YYYY", required=True, max_chars=4)
    }
)

# Layout
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Filter")
    selected_years = st.multiselect("Filter by Year", edited_df["Year"].unique(), default=list(edited_df["Year"].unique()))
    selected_events = st.multiselect("Filter by Event", edited_df["Event"].unique(), default=list(edited_df["Event"].unique()))

filtered = edited_df[
    (edited_df["Year"].isin(selected_years)) &
    (edited_df["Event"].isin(selected_events))
]

# Plot
with col1:
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Audience Type (General ↔ Specialized)", fontsize=10)
    ax.set_ylabel("Participation Level (Passive ↔ Active)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.title("Audience Matrix", fontsize=12)

    # Optional quadrant labels
    quadrants = {
        "Mass Appeal / Spectator": (0.2, 0.2),
        "Niche Thinkers": (0.8, 0.2),
        "Community Builders": (0.2, 0.8),
        "Engaged Experts": (0.8, 0.8)
    }

    for label, (x, y) in quadrants.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=9, bbox=dict(facecolor='lightgreen', alpha=0.3))

    for _, row in filtered.iterrows():
        x = x_map.get(row["Audience Type"], 0.5)
        y = y_map.get(row["Participation Level"], 0.5)
        ax.plot(x, y, 'o', color='darkgreen')
        ax.text(x, y + 0.02, row["Event"], fontsize=8, ha='center')

    st.pyplot(fig)

# Sidebar nav
st.sidebar.title("Tools")
st.sidebar.page_link("app.py", label="4 Modules")
st.sidebar.page_link("pages/supportlevel.py", label="Level of Support")
st.sidebar.page_link("pages/audience.py", label="Audience")
