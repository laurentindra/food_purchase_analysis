import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'ANALISA KANTIN/sta24.csv'  # Correct file path to the CSV file inside the folder

# Error handling for file loading
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"The file {file_path} could not be found.")
    st.stop()  # Stop the app if the file is not found
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()  # Stop the app if any other error occurs

# Display the dataset as a table
def display_dataset():
    st.subheader("Dataset Preview")
    st.dataframe(data)  # Display the entire dataset in a table format

# Generate the Bar Chart - Distribution of Food Purchase Locations (Canteen vs. Online)
def plot_bar_chart():
    try:
        location_counts = data['Where do you buy food more often?'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))  # Create figure and axis
        ax.bar(location_counts.index, location_counts.values, color=['skyblue', 'orange'])
        ax.set_title('Distribution of Food Purchase Locations (Canteen vs. Online)')
        ax.set_xlabel('Location')
        ax.set_ylabel('Number of Responses')
        ax.set_xticklabels(location_counts.index, rotation=45)
        st.pyplot(fig)  # Pass the figure to st.pyplot
    except KeyError:
        st.error("The column 'Where do you buy food more often?' is missing in the dataset.")
    except Exception as e:
        st.error(f"An error occurred while generating the bar chart: {e}")

# Generate the Pie Chart - Most Common Reasons for Online Food Ordering
def plot_pie_chart():
    try:
        online_reasons = data['What is the main reason you choose to buy food online? (Choose a maximum of 2)'].dropna()
        online_reasons = online_reasons.str.split(';').explode().value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))  # Create figure and axis
        online_reasons.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, ax=ax)
        ax.set_title('Most Common Reasons for Choosing Online Food Ordering')
        st.pyplot(fig)  # Pass the figure to st.pyplot
    except KeyError:
        st.error("The column 'What is the main reason you choose to buy food online? (Choose a maximum of 2)' is missing in the dataset.")
    except Exception as e:
        st.error(f"An error occurred while generating the pie chart: {e}")

# Generate the Stacked Bar Chart - Comparison of Preferences Based on Obstacles
def plot_stacked_bar_chart():
    try:
        obstacles_column = data['What are the most common obstacles you experience when buying food at the canteen?']
        obstacle_list = ['Long queues', 'Limited food options', 'Unhealthy food options', 'Expensive', 'Other']
        for obstacle in obstacle_list:
            data[obstacle] = obstacles_column.str.contains(obstacle, case=False, na=False).astype(int)

        obstacle_counts = data.groupby('Where do you buy food more often?')[obstacle_list].sum()
        
        fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axis
        obstacle_counts.plot(kind='bar', stacked=True, colormap='Set2', ax=ax)
        ax.set_title('Comparison of Preferences for Food Purchase Based on Obstacles')
        ax.set_xlabel('Food Purchase Location')
        ax.set_ylabel('Number of Responses')
        ax.set_xticklabels(obstacle_counts.index, rotation=0)
        st.pyplot(fig)  # Pass the figure to st.pyplot
    except KeyError:
        st.error("The column 'What are the most common obstacles you experience when buying food at the canteen?' is missing in the dataset.")
    except Exception as e:
        st.error(f"An error occurred while generating the stacked bar chart: {e}")

# Streamlit App
def main():
    st.title('Food Purchase Preferences Analysis')
    st.markdown("This app analyzes student preferences for food purchases and reasons for choosing online or canteen options.")
    
    # Display the dataset
    display_dataset()
    
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
