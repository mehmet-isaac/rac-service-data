import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

st.set_page_config(page_title="Replacement Car Dashboard", layout="wide")
st.title("🚗 Replacement Car Service Dashboard")

# Load the data
df = pd.read_csv("replacement_car_cases.csv")

# Sidebar Filters
st.sidebar.header("🔎 Filters")
rental_filter = st.sidebar.multiselect("Select Rental Company", options=df['rental_company'].unique(), default=df['rental_company'].unique())

# Filter the data
filtered_df = df[df['rental_company'].isin(rental_filter)]

# KPI Cards
st.markdown("### 📊 Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Avg Delivery Delay (hrs)", round(filtered_df['delivery_delay_hours'].mean(), 1))
col2.metric("Total Complaints", int(filtered_df['complaint_made'].sum()))
col3.metric("Avg Rental Duration (days)", round(filtered_df['rental_duration_days'].mean(), 1))

# Chart 1: Complaints per Rental Company
st.markdown("### 🚨 Complaints by Rental Company")
fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df[filtered_df['complaint_made']], x='rental_company', palette='Reds', ax=ax1)
ax1.set_ylabel("Number of Complaints")
st.pyplot(fig1)

# Chart 2: Delivery Delay Distribution
st.markdown("### ⏱️ Delivery Delay Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df['delivery_delay_hours'], bins=20, kde=True, ax=ax2)
ax2.set_xlabel("Delivery Delay (Hours)")
st.pyplot(fig2)

# Chart 3: Complaint Reasons Pie Chart
if filtered_df['complaint_reason'].notna().sum() > 0:
    st.markdown("### ❗ Complaint Reasons")
    fig3, ax3 = plt.subplots()
    filtered_df['complaint_reason'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3)
    ax3.set_ylabel('')
    st.pyplot(fig3)

# Chart 4: Avg Rental Duration by Car Brand
st.markdown("### 🚘 Avg Rental Duration by Car Brand")
avg_durations = filtered_df.groupby('car_brand')['rental_duration_days'].mean().sort_values()
fig4, ax4 = plt.subplots()
sns.barplot(x=avg_durations.index, y=avg_durations.values, palette='Blues', ax=ax4)
ax4.set_ylabel("Days")
st.pyplot(fig4)
# Chart 5: Avg Delivery Delay by Rental Company
st.markdown("### 📦 Avg Delivery Delay by Rental Company")
avg_delays = filtered_df.groupby('rental_company')['delivery_delay_hours'].mean().sort_values()

fig5, ax5 = plt.subplots()
sns.barplot(x=avg_delays.index, y=avg_delays.values, palette='Oranges', ax=ax5)
ax5.set_ylabel("Average Delay (Hours)")
ax5.set_xlabel("Rental Company")
st.pyplot(fig5)