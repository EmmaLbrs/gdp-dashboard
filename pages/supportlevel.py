import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("Level of Support Typology")

# Define editable data with levels
support_data = pd.DataFrame([
    {"Event": "Tool Tuesday", "Year": "2024", "User Initiative": "Medium", "Staff Involvement": "Medium"},
    {"Event": "Frauen* im Fokus", "Year": "2024", "User Initiative": "Medium", "Staff Involvement": "Medium"},
    {"Event": "Datencafe", "Year": "2024", "User Initiative": "Medium", "Staff Involvement": "Medium"},
    {"Event": "Blauer Salon", "Year": "2024", "User Initiative": "Medium", "Staff Involvement": "Medium"},
])

# Value map for plotting
level_mapX = {"Indepedent": 0.2, "Medium": 0.5, "Supported": 0.8}
level_mapY = {"Unbegleitet": 0.2, "Medium": 0.5, "Moderiert": 0.8}


# Make editable
st.markdown("### Edit Support Levels")
edited_support = st.data_editor(
    support_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "User Initiative": st.column_config.SelectboxColumn(options=["Indepedent", "Medium", "Supported"]),
        "Staff Involvement": st.column_config.SelectboxColumn(options=["Unbegleitet", "Medium", "Moderiert"]),
        "Year": st.column_config.TextColumn(
            help="Enter year as YYYY", required=True, max_chars=4
        )
    }
)

# Layout
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### Filter")
    filter_years = st.multiselect("Year", edited_support["Year"].unique(), default=list(edited_support["Year"].unique()))
    filter_events = st.multiselect("Event", edited_support["Event"].unique(), default=list(edited_support["Event"].unique()))
    if st.button("Select All"):
        filter_events = list(edited_support["Event"].unique())
    if st.button("Mask All"):
        filter_events = []

# Filter data
filtered = edited_support[
    (edited_support["Year"].isin(filter_years)) &
    (edited_support["Event"].isin(filter_events))
]

# Plot
with col1:
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Nutzerinitiative / User Initiative (Selbstständig ↔ Unterstützt)", fontsize=10)
    ax.set_ylabel("Grad der Moderation / Staff Involvement (Unbegleitet ↔ Moderiert)", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.title("Support-Typologie nach Nutzerinitiative & Moderation", fontsize=12)

    quadrants = {
        "Community of Practice\n(peer-led)": (0.2, 0.2),
        "Teaching People How\n(structured, independent execution)": (0.2, 0.8),
        "Doing Things for People\n(structured, staff-led)": (0.8, 0.8),
        "Doing Things with People\n(collaborative, guided)": (0.5, 0.5)
    }

    for label, (x, y) in quadrants.items():
        ax.text(x, y, label, ha='center', va='center', fontsize=9, bbox=dict(facecolor='lightblue', alpha=0.3))

    for _, row in filtered.iterrows():
        x = level_mapX.get(row['User Initiative'], 0.5)
        y = level_mapY.get(row['Staff Involvement'], 0.5)
        ax.plot(x, y, 'o', color='darkblue')
        ax.text(x, y + 0.02, row['Event'], fontsize=8, ha='center')

    st.pyplot(fig)

# Sidebar nav
st.sidebar.title("Tools")
st.sidebar.page_link("app.py", label="4 Modules")
st.sidebar.page_link("pages/supportlevel.py", label="Level of Support")
st.sidebar.page_link("pages/audience.py", label="Audience")
st.sidebar.page_link("pages/space.py", label="Space and Place")
