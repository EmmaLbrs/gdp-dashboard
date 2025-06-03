import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("Space / Place")

# Initial editable data
audience_data = pd.DataFrame([
    {"Event": "F*iF", "Year": "2024", "Format": "Hybrid"},
    {"Event": "Tool Tuesday", "Year": "2024", "Format": "Online"},
    {"Event": "DatenCafe", "Year": "2024", "Format": "On Site"},
    {"Event": "Blauer Salon", "Year": "2024", "Format": "On Site"},
    {"Event": "Text Mining mit R", "Year": "2024", "Format": "On Site"},
])

# Mapping format to x-axis values
format_map = {"Online": 0.0, "Hybrid": 0.5, "On Site": 1.0}

# Editable table
st.markdown("### Edit Event Formats")
edited_data = st.data_editor(
    audience_data,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Format": st.column_config.SelectboxColumn(options=["Online", "Hybrid", "On Site"]),
        "Year": st.column_config.TextColumn(help="Enter year as YYYY", max_chars=4)
    }
)

# Layout
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 🔍 Filter")
    filter_years = st.multiselect("Year", edited_data["Year"].unique(), default=list(edited_data["Year"].unique()))
    filter_events = st.multiselect("Event", edited_data["Event"].unique(), default=list(edited_data["Event"].unique()))
    if st.button("Select All"):
        filter_events = list(edited_data["Event"].unique())
    if st.button("Mask All"):
        filter_events = []

# Filter data
filtered = edited_data[
    (edited_data["Year"].isin(filter_years)) &
    (edited_data["Event"].isin(filter_events))
]

# Plot
with col1:
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.2, 0.3)
    ax.axhline(0, color='black', linewidth=0.5)

    y_base = 0.05
    y_offsets = [i * 0.03 for i in range(len(filtered))]

    for i, (_, row) in enumerate(filtered.iterrows()):
        x = format_map.get(row["Format"], 0.5)
        y = y_base + y_offsets[i]
        ax.plot(x, y, 'o', color='darkgreen')
        ax.text(x, y + 0.01, row["Event"], ha='center', fontsize=9)

    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(['Online', 'Hybrid', 'On Site'])
    ax.set_yticks([])
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    st.pyplot(fig)

# Sidebar nav
st.sidebar.title("Tools")
st.sidebar.page_link("app.py", label="4 Modules")
st.sidebar.page_link("pages/supportlevel.py", label="Level of Support")
st.sidebar.page_link("pages/audience.py", label="Audience")
st.sidebar.page_link("pages/space.py", label="Space and Place")