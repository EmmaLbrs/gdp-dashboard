import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")
st.title("🎯 Interactive Event Role Radar")

# Initial data setup
def get_initial_data():
    return pd.DataFrame([
        {"Event": "F*iF", "Year": "2024", "Community Builder": "High", "Research Accelerator": "Medium", "Creative Innovation Hub": "Medium", "Tech & Tools Depot": "Low"},
        {"Event": "Tool Tuesday", "Year": "2024", "Community Builder": "Medium", "Research Accelerator": "Medium", "Creative Innovation Hub": "Medium", "Tech & Tools Depot": "High"},
        {"Event": "Julie Elias", "Year": "2024", "Community Builder": "Medium", "Research Accelerator": "High", "Creative Innovation Hub": "Medium", "Tech & Tools Depot": "Low"},
        {"Event": "DatenCafe", "Year": "2024", "Community Builder": "High", "Research Accelerator": "Medium", "Creative Innovation Hub": "Low", "Tech & Tools Depot": "Medium"},
    ])

categories = ['Community Builder', 'Research Accelerator', 'Creative Innovation Hub', 'Tech & Tools Depot']
value_map = {"Low": 1, "Medium": 5, "High": 10}

# Load or initialize session state
data_key = "event_data"
if data_key not in st.session_state:
    st.session_state[data_key] = get_initial_data()

# Editable table
st.markdown("### 📝 Edit Event Data")
df = st.session_state[data_key]
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        cat: st.column_config.SelectboxColumn(options=["Low", "Medium", "High"]) for cat in categories
    } | {
        "Year": st.column_config.TextColumn(
            help="Enter year as a 4-digit number, e.g., 2024",
            required=True,
            max_chars=4
        )
    }
)
st.session_state[data_key] = edited_df

# Main layout
col1, col2 = st.columns([2, 1])

# Chart
with col1:
    st.markdown("### 📈 Radar Chart")

    # Filtered data will be used below after filters in col2
    filtered_data_placeholder = st.empty()

# Filters and info
with col2:
    st.markdown("### 🔍 Filter Settings")
    selected_years = st.multiselect("Filter by Year", options=sorted(edited_df['Year'].unique()), default=sorted(edited_df['Year'].unique()))
    selected_events = st.multiselect("Filter by Event", options=sorted(edited_df['Event'].unique()), default=sorted(edited_df['Event'].unique()))

    st.markdown("---")
    st.write("**Years:**", ", ".join(selected_years))
    st.write("**Events:**", ", ".join(selected_events))

# Apply filters and render chart
with col1:
    data_rows = edited_df[edited_df['Year'].isin(selected_years) & edited_df['Event'].isin(selected_events)]

    def create_radar_chart(ax, values, label):
        n_categories = len(categories)
        angles = np.linspace(0, 2 * np.pi, n_categories, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        ax.fill(angles, values, alpha=0.2)
        ax.plot(angles, values, linewidth=2, label=label)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticklabels([])

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={'projection': 'polar'})
    for _, row in data_rows.iterrows():
        values = [value_map[row[cat]] for cat in categories]
        create_radar_chart(ax, values[:], row["Event"])
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig)

# Sidebar for navigation
st.sidebar.title("Menu")
st.sidebar.page_link("supportlevel.py", label="Level of Support")
