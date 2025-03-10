import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'ANALISA KANTIN/sta24.csv'  # Replace with the correct file path
data = pd.read_csv(file_path)

# Generate the Bar Chart - Distribution of Food Purchase Locations (Canteen vs. Online)
def plot_bar_chart():
    location_counts = data['Where do you buy food more often?'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.bar(location_counts.index, location_counts.values, color=['skyblue', 'orange'])
    plt.title('Distribution of Food Purchase Locations (Canteen vs. Online)')
    plt.xlabel('Location')
    plt.ylabel('Number of Responses')
    plt.xticks(rotation=45)
    st.pyplot()

# Generate the Pie Chart - Most Common Reasons for Online Food Ordering
def plot_pie_chart():
    online_reasons = data['What is the main reason you choose to buy food online? (Choose a maximum of 2)'].dropna()
    online_reasons = online_reasons.str.split(';').explode().value_counts()
    plt.figure(figsize=(8, 6))
    online_reasons.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Most Common Reasons for Choosing Online Food Ordering')
    plt.ylabel('')
    st.pyplot()

# Generate the Stacked Bar Chart - Comparison of Preferences Based on Obstacles
def plot_stacked_bar_chart():
    obstacles_column = data['What are the most common obstacles you experience when buying food at the canteen?']
    obstacle_list = ['Long queues', 'Limited food options', 'Unhealthy food options', 'Expensive', 'Other']
    for obstacle in obstacle_list:
        data[obstacle] = obstacles_column.str.contains(obstacle, case=False, na=False).astype(int)
    
    obstacle_counts = data.groupby('Where do you buy food more often?')[obstacle_list].sum()
    
    obstacle_counts.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')
    plt.title('Comparison of Preferences for Food Purchase Based on Obstacles')
    plt.xlabel('Food Purchase Location')
    plt.ylabel('Number of Responses')
    plt.xticks(rotation=0)
    st.pyplot()

# Streamlit App
def main():
    st.title('Food Purchase Preferences Analysis')
    st.markdown("This app analyzes student preferences for food purchases and reasons for choosing online or canteen options.")
    
    # Bar Chart - Food Purchase Location Distribution
    st.subheader("1. Distribution of Food Purchase Locations")
    plot_bar_chart()
    
    # Pie Chart - Reasons for Online Ordering
    st.subheader("2. Most Common Reasons for Choosing Online Ordering")
    plot_pie_chart()
    
    # Stacked Bar Chart - Comparison Based on Obstacles
    st.subheader("3. Comparison of Preferences Based on Obstacles")
    plot_stacked_bar_chart()

if __name__ == "__main__":
    main()
