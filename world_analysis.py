import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
import pycountry
import seaborn as sns
import geopandas as gpd
import streamlit as st
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import folium
from folium.plugins import HeatMapWithTime
from streamlit_folium import st_folium
import os
import tempfile
# Set page configuration
st.set_page_config(
    page_title="Global COVID-19 Data Dashboard",
    layout="wide",  # Full-width layout
    initial_sidebar_state="collapsed"  # Hide the sidebar by default
)

# Custom CSS with dark background and light text for contrast
st.markdown("""
    <style>
        /* Main background and font */
        .main { 
            background-color: #1f2937;  /* Dark background for a modern look */
            font-family: 'Segoe UI', sans-serif; 
            margin: 0;
            padding: 0;
            color: #e5e7eb;  /* Light gray text for high contrast against dark background */
        }

        /* Header styling */
        .title h1 {
            color: #bb86fc;  /* Light purple for headers to stand out against dark background */
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            padding-top: 40px;
            padding-bottom: 20px;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        /* Sub-header styling */
        .sub-header {
            color: #82b1ff;  /* Light blue for sub-headers to create hierarchy */
            font-size: 1.9rem;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 30px;
            font-weight: 500;
        }

        /* Section styling */
        .section { 
            background: #2d3748;  /* Slightly lighter dark background for sections */
            border-radius: 12px; 
            padding: 40px; 
            box-shadow: 0px 12px 36px rgba(0, 0, 0, 0.12);  /* Softer, larger shadow for depth */
            margin: 30px auto;
            width: 85%;  /* More flexible for responsiveness */
            max-width: 1200px;
        }

        /* Section hover effect */
        .section:hover {
            box-shadow: 0px 16px 48px rgba(0, 0, 0, 0.15);
        }

        /* Description box styling */
        .description {
            font-size: 1.1rem;
            color: #d1d5db;  /* Lighter gray for description text */
            margin: 20px 0;
            padding: 20px;
            background-color: #3f4c64;  /* Darker gray background for description */
            border-left: 6px solid #bb86fc;  /* Purple accent to match header */
            border-radius: 8px;
            line-height: 1.6;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.05);
        }

        /* Selectbox styling */
        .stSelectbox {
            font-size: 1.1rem;
            color: #e5e7eb;  /* Light gray text for selectbox */
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid #4b5563;  /* Darker border to match background */
            background-color: #2d3748;  /* Dark background for selectbox */
            width: 100%;
            box-sizing: border-box;
            margin-top: 10px;
            transition: border-color 0.3s ease;
        }

        .stSelectbox:focus {
            border-color: #82b1ff;  /* Light blue border for focus effect */
            outline: none;
        }

        /* Button styling */
        .stButton {
            background-color: #6200ea;  /* Purple button for a strong call to action */
            color: white;
            font-size: 1.2rem;
            border-radius: 8px;
            padding: 14px 24px;
            transition: background-color 0.3s, transform 0.2s ease-in-out;
            border: none;
            cursor: pointer;
            width: 100%;
            text-align: center;
        }

        /* Button hover effect */
        .stButton:hover {
            background-color: #3700b3;  /* Darker purple on hover */
            transform: translateY(-2px);
        }

        /* Info box styling */
        .stInfo { 
            background-color: #374151;  /* Darker background for info sections */
            padding: 20px; 
            border-radius: 8px; 
            margin-top: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); 
        }

        /* Footer or Bottom CTA */
        .footer {
            background-color: #1f2937;  /* Matching dark footer */
            color: #e5e7eb;  /* Light text for footer */
            text-align: center;
            padding: 20px 0;
            font-size: 1rem;
            position: fixed;
            width: 100%;
            bottom: 0;
            left: 0;
        }

        .footer a {
            color: #bb86fc;  /* Purple for footer links */
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        /* Responsive design for smaller screens */
        @media (max-width: 768px) {
            .section {
                width: 95%; 
                padding: 20px;
            }

            .stButton {
                font-size: 1.1rem;
                padding: 12px 20px;
            }

            .stSelectbox {
                font-size: 1rem;
                padding: 12px;
            }

            .description {
                font-size: 1rem;
            }

            .title h1 {
                font-size: 2.5rem;
            }

            .sub-header {
                font-size: 1.7rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Header section with updated title styling and tagline
st.markdown("""
<div class="title">
    <h1>Global COVID-19 Data Dashboard</h1>
</div>
<div class="sub-header">
    Explore critical global COVID-19 trends, vaccination progress, and insights from around the world.
</div>
""", unsafe_allow_html=True)

# Dashboard description with updated professional tone
st.markdown("""
<div class="description">
    Welcome to the **Global COVID-19 Data Dashboard**, your comprehensive source for the latest global COVID-19 metrics and trends. 
    This dashboard provides:
    - **Real-time updates** on global vaccination progress and case statistics.
    - **Interactive charts** for analyzing worldwide trends.
    - **Key insights** to understand the evolving pandemic at a global scale.
    
    Utilize the tools and visualizations below to delve deeper into global COVID-19 data and make well-informed decisions. Together, we can face the challenges of the pandemic with clarity and resilience.
</div>
""", unsafe_allow_html=True)




# Load and prepare data
@st.cache_data
def load_and_prepare_data():
    # Load global COVID-19 data
    global_data = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_19_data.csv')
    global_data['ObservationDate'] = pd.to_datetime(global_data['ObservationDate'])

    # Fill missing values in global data
    if 'Province/State' in global_data:
        global_data['Province/State'] = global_data['Province/State'].fillna('Unknown')

    # Clean negative values
    for column in ['Confirmed', 'Deaths', 'Recovered']:
        global_data[column] = global_data[column].clip(lower=0).fillna(0)

    # Aggregate global data
    global_totals = global_data.groupby('Country/Region').sum(numeric_only=True).reset_index()
    global_totals_sum = global_totals[['Confirmed', 'Deaths', 'Recovered']].sum()
    global_totals['Active'] = global_totals['Confirmed'] - (global_totals['Deaths'] + global_totals['Recovered'])
    # Calculate Mortality Rate
    global_totals['Mortality Rate'] = (global_totals['Deaths'] / global_totals['Confirmed']) * 1000

    # Load India-specific COVID-19 data
    india_data = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_19_india.csv')
    india_data = india_data.drop(columns=["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"])
    india_data['Active_cases'] = india_data['Confirmed'] - (india_data['Cured'] + india_data['Deaths'])
    india_data['State/UnionTerritory'] = india_data['State/UnionTerritory'].replace({
        'Maharashtra***': "Maharashtra",
        'Bihar****': "Bihar",
        'Madhya Pradesh***': "Madhya Pradesh",
        'Karanataka': "Karnataka"
    })

    # State-wise summary data
    statewise_data = pd.pivot_table(india_data, values=['Confirmed', 'Deaths', 'Cured'], 
                                    index="State/UnionTerritory", aggfunc='max')
    statewise_data['Recovery Rate'] = (statewise_data['Cured'] * 100) / statewise_data['Confirmed']
    statewise_data['Mortality Rate'] = (statewise_data['Deaths'] * 100) / statewise_data['Confirmed']
    statewise_data = statewise_data.sort_values(by="Confirmed", ascending=False)

    return global_totals_sum, global_totals, statewise_data

# Define plotting functions for professional look
def plot_global_totals(global_totals_sum):
    fig, ax = plt.subplots()
    ax.bar(global_totals_sum.index, global_totals_sum.values, color=['blue', 'red', 'green'])
    ax.set_title('Global COVID-19 Totals')
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45)
    return fig

def plot_top_countries_active_cases(global_totals):
    top_countries = global_totals.nlargest(10, 'Active')
    fig, ax = plt.subplots()
    ax.bar(top_countries['Country/Region'], top_countries['Active'], color='orange')
    ax.set_title('Top 10 Countries by Active COVID-19 Cases')
    plt.xticks(rotation=45)
    return fig

def plot_top_countries_mortality(global_totals):
    global_totals['Mortality Rate'] = (global_totals['Deaths'] / global_totals['Confirmed']).replace([float('inf'), -float('inf')], 0) * 100
    # Drop any rows where confirmed cases are 0 to avoid infinite mortality rates
    top_countries_mortality = global_totals[global_totals['Confirmed'] > 0].nlargest(10, 'Mortality Rate')
    fig, ax = plt.subplots()
    ax.bar(top_countries_mortality['Country/Region'], top_countries_mortality['Mortality Rate'], color='red')
    ax.set_title('Top 10 Countries by Mortality Rate (%)')
    ax.set_xlabel('Country')
    ax.set_ylabel('Mortality Rate (%)')
    plt.xticks(rotation=45)
    return fig



# Main function for dashboard
def main():
    # Title for the analysis section with a more impactful styling
    st.markdown("<div class='sub-header'>Choose Your COVID-19 Analysis Type</div>", unsafe_allow_html=True)

    # Dropdown for selecting analysis type with a custom style
    option = st.selectbox(
        "Select Analysis Type:",
        ("Home", "Vaccination Analysis", "COVID-19 Cases and Deaths Analysis"),
        index=0,  # Set default selection to "Home"
        help="Select the analysis type you want to explore, such as vaccination data or case statistics."
    )

    # Divider for separation with a more subtle effect
    st.markdown("<hr style='margin: 40px 0; border: 1px solid #3e4c59;'>", unsafe_allow_html=True)

    # Description text with improved styling and content
    st.markdown("""
        <p style="color: #d1d5db; font-size: 1.2rem; text-align: center; line-height: 1.6; margin-top: 10px;">
            Choose from different analysis types to explore key insights related to the COVID-19 pandemic. 
            You can explore trends in <b>vaccination coverage</b>, and analyze the global impact of COVID-19 
            with up-to-date information on <b>cases</b> and <b>death rates</b> across countries.
        </p>
        <p style="color: #e5e7eb; font-size: 1rem; text-align: center; line-height: 1.6;">
            Use the options below to dive deep into real-time data and gain actionable insights. Stay informed, stay safe!
        </p>
    """, unsafe_allow_html=True)
    global_totals_sum, global_totals, statewise_data = load_and_prepare_data()



    df = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_19_data.csv')
    df['ObservationDate'] = pd.to_datetime(df['ObservationDate'])

    if 'Province/State' in df:
        df['Province/State'] = df['Province/State'].fillna('Unknown')

    for column in ['Confirmed', 'Deaths', 'Recovered']:
        df[column] = df[column].clip(lower=0).fillna(0)
    datewise_data = df.groupby('ObservationDate').sum(numeric_only=True)
    datewise_data['Active'] = datewise_data['Confirmed'] - (datewise_data['Recovered'] + datewise_data['Deaths'])
    datewise_data['daily_confirmed'] = datewise_data['Confirmed'].diff()
    datewise_data['daily_recovered'] = datewise_data['Recovered'].diff()
    datewise_data['daily_deaths'] = datewise_data['Deaths'].diff()
    datewise_data['daily_active'] = datewise_data['Active'].diff()
    columns_to_fix = ['daily_confirmed', 'daily_recovered', 'daily_deaths', 'daily_active']
    for column in columns_to_fix:
        datewise_data[column] = datewise_data[column].mask(datewise_data[column] < 0).ffill().fillna(0)

    # Calculate 7-day moving average for daily cases
    datewise_data['7_day_avg_confirmed'] = datewise_data['daily_confirmed'].rolling(window=7).mean()
    datewise_data['7_day_avg_recovered'] = datewise_data['daily_recovered'].rolling(window=7).mean()
    datewise_data['7_day_avg_deaths'] = datewise_data['daily_deaths'].rolling(window=7).mean()
    datewise_data['7_day_avg_active'] = datewise_data['daily_active'].rolling(window=7).mean()

    # Forward-fill any remaining NaN or negative values in the moving averages
    columns_to_fix = ['7_day_avg_confirmed', '7_day_avg_recovered', '7_day_avg_deaths', '7_day_avg_active']
    for column in columns_to_fix:
        datewise_data[column] = datewise_data[column].mask(datewise_data[column] < 0).ffill().fillna(0)

    # Optional: Reset the index if needed
    datewise_data = datewise_data.reset_index()
    df1 = pd.read_csv('/Users/ayyalashriyatha/Desktop/data.csv')
    df1['year_week_date'] = pd.to_datetime(df1['year_week'] + '-1', format='%G-W%V-%u')
    df1['new_cases'] = df1['new_cases'].fillna(0)
    df1['tests_done'] = df1['tests_done'].fillna(0)
    # Calculate positivity rate if missing
    df1['calculated_positivity_rate'] = (df1['new_cases'] / df1['tests_done']) * 100

    # Calculate positivity rate safely
    df1['calculated_positivity_rate'] = (df1['new_cases'] / df1['tests_done']).replace([float('inf'), -float('inf')], 0) * 100

    # Replace NaN or extreme positivity rates
    df1['calculated_positivity_rate'] = df1['calculated_positivity_rate'].fillna(0)

    # Optionally cap positivity rates to a reasonable maximum (e.g., 100%)
    max_positivity_threshold = 100
    df1['calculated_positivity_rate'] = df1['calculated_positivity_rate'].clip(upper=max_positivity_threshold)

    aggregated_df = df1.groupby('year_week_date').agg(
        tests_done=('tests_done', 'sum'),  # Sum of tests done for the week
        calculated_positivity_rate=('calculated_positivity_rate', 'mean')  # Mean of positivity rate
    ).reset_index()

    # Calculate a rolling average for the positivity rate (e.g., 3-week rolling average)
    aggregated_df['rolling_positivity_rate'] = aggregated_df['calculated_positivity_rate'].rolling(window=3).mean()
    df_map = df.groupby(['ObservationDate', 'Country/Region']).agg({'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum'}).reset_index()

    df_map.rename(columns={'ObservationDate': 'Date', 'Country/Region': 'Country_Region', 'Confirmed': 'ConfirmedCases', 'Deaths': 'TotalDeaths', 'Recovered': 'TotalRecovered'}, inplace=True)
    country_iso_map = {country.name: country.alpha_3 for country in pycountry.countries}
    df_map['iso_alpha'] = df_map['Country_Region'].map(country_iso_map)
    df_map['Date'] = pd.to_datetime(df_map['Date'])


    df_map['Recovery_Rate'] = (df_map['TotalRecovered'] / df_map['ConfirmedCases']) * 100
    df_map['Mortality_Rate'] = (df_map['TotalDeaths'] / df_map['ConfirmedCases']) * 100 

    df3 = pd.read_csv('/Users/ayyalashriyatha/Desktop/vaccination-data.csv')

    df3 = df3.dropna(subset=['TOTAL_VACCINATIONS', 'PERSONS_VACCINATED_1PLUS_DOSE'])

    # 2. Convert data types
    # Convert 'DATE_UPDATED' to datetime format if necessary
    if 'DATE_UPDATED' in df.columns:
        df3['DATE_UPDATED'] = pd.to_datetime(df3['DATE_UPDATED'], errors='coerce')

    # 3. Calculate additional metrics (if needed)
    # For example, we can calculate the percentage of the population vaccinated
    if 'PERSONS_VACCINATED_1PLUS_DOSE' in df.columns and 'PERSONS_LAST_DOSE' in df.columns:
        df3['PERCENT_VACCINATED'] = df3['PERSONS_VACCINATED_1PLUS_DOSE'] / df3['TOTAL_VACCINATIONS'] * 100

    # 4. Remove duplicates
    df3 = df3.drop_duplicates()

    if option == "Home":
        # Title with a modern and engaging style
        st.markdown("""
            <div class="title">
                <h1>COVID-19 Data Dashboard</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Welcome message with a more friendly and informative tone
        st.markdown("""
            <div class="description">
                <p style="color: #d1d5db; font-size: 1.2rem; text-align: center; line-height: 1.8; margin-top: 20px;">
                    Welcome to the <b>COVID-19 Data Dashboard</b>, your hub for global and country-specific pandemic insights. 
                    Dive into real-time data and track the latest trends in COVID-19 cases, deaths, vaccinations, and more.
                </p>
                <p style="color: #e5e7eb; font-size: 1rem; text-align: center; line-height: 1.6;">
                    Use the sidebar to easily navigate between global and country-specific analyses, gain actionable insights, and stay informed about the ongoing fight against COVID-19.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Optional: A call to action to encourage further engagement
        st.markdown("""
            <div style="text-align: center; margin-top: 30px;">
                <button class="stButton">Start Exploring</button>
            </div>
        """, unsafe_allow_html=True)
        
        # Subtitle or action to highlight features of the dashboard
        st.markdown("""
            <div class="sub-header">
                Explore Key Insights:
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <ul style="font-size: 1.1rem; color: #d1d5db; line-height: 1.8; text-align: center;">
                <li>Global COVID-19 case and death trends</li>
                <li>Real-time vaccination coverage updates</li>
                <li>Detailed country-level analysis and comparisons</li>
            </ul>
        """, unsafe_allow_html=True)


    elif option == "COVID-19 Cases and Deaths Analysis":
        st.markdown("""
            <div class="title">
                <h1>Global COVID-19 Analytics</h1>
            </div>
        """, unsafe_allow_html=True)

        # Description for this section with a more engaging and informative tone
        st.markdown("""
            <div class="description">
                <p style="color: #d1d5db; font-size: 1.2rem; text-align: center; line-height: 1.8; margin-top: 20px;">
                    Explore the latest global trends and insights on COVID-19 cases, deaths, and recovery rates.
                    Select different visualizations to understand how the pandemic is evolving across countries.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Radio button for selecting visualization options
        world_option = st.radio(
            "Select Visualization:",
            options=(
                "Global Overview",
                "Top Countries by COVID-19 Metrics",
                "COVID-19 Trends and Rates"
            ),
            index=0,  # Default option selected as "Global Overview"
            help="Choose how you want to visualize the global and country-specific COVID-19 data."
        )

        # Divider to visually separate sections
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #cccccc;'>", unsafe_allow_html=True)


        if world_option == "Global Overview":
            st.markdown("<div class='sub-header'>Global COVID-19 Overview</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    View the worldwide distribution of COVID-19 cases, deaths, and recoveries, with a breakdown of key statistics across continents.
                </p>
            """, unsafe_allow_html=True)
            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Global COVID-19 Totals", 
                    "Cumulative COVID-19 Cases Over Time"
                ),
                index=0,  # Default selection
                help="Select how you'd like to view the global COVID-19 data: totals or trends over time."
            )

            # Divider to visually separate sections
            st.markdown("<hr style='margin: 30px 0; border: 1px solid #cccccc;'>", unsafe_allow_html=True)
            if world_sub_option == "Cumulative COVID-19 Cases Over Time":
                st.markdown("<div class='sub-header'>Cumulative COVID-19 Cases Over Time</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the growth of cumulative COVID-19 cases globally over time. This section allows you to analyze the trends and rate of spread.
                    </p>
                """, unsafe_allow_html=True)
                plt.figure(figsize=(14, 8))
                plt.plot(datewise_data['ObservationDate'], datewise_data['Confirmed'], label='Confirmed', color='blue')
                plt.plot(datewise_data['ObservationDate'], datewise_data['Recovered'], label='Recovered', color='green')
                plt.plot(datewise_data['ObservationDate'], datewise_data['Active'], label='Active', color='orange')
                plt.plot(datewise_data['ObservationDate'], datewise_data['Deaths'], label='Deaths', color='red')

                # Add labels and title
                plt.xlabel('Date')
                plt.ylabel('Cumulative Cases')
                plt.title('Cumulative COVID-19 Cases Over Time')
                plt.legend()
                plt.grid()

                # Use Streamlit to display the plot
                st.pyplot(plt)
                plt.close()  # Close the figure to avoid displaying it twice
            elif world_sub_option == "Global COVID-19 Totals":
                st.markdown("<div class='sub-header'>Global COVID-19 Totals</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        View the current global total of COVID-19 cases, deaths, and recoveries. This section provides an overview of the pandemic's impact worldwide.
                    </p>
                """, unsafe_allow_html=True)
                st.header("Global COVID-19 Totals")
                st.write(global_totals_sum)
                st.pyplot(plot_global_totals(global_totals_sum))

        elif world_option == "COVID-19 Trends and Rates":
            st.markdown("<div class='sub-header'>COVID-19 Trends and Rates</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    Analyze the trends in COVID-19 cases, death rates, and recovery rates over time across regions and countries.
                </p>
            """, unsafe_allow_html=True)
            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Daily COVID-19 Cases with 7-Day Moving Average",
                    "Weekly Tests and Positivity Rate Over Time",
                    "Spread Of COVID-19 Over Time",
                    "COVID-19 Cases Animated Heatmap"
                ),
                index=0,  # Default selection
                help="Select a visualization to explore different aspects of the COVID-19 pandemic: daily cases, test positivity, or global spread trends."
            )

            # Divider to visually separate sections
            st.markdown("<hr style='margin: 30px 0; border: 1px solid #cccccc;'>", unsafe_allow_html=True)
            if world_sub_option == "Daily COVID-19 Cases with 7-Day Moving Average":
                st.markdown("<div class='sub-header'>Daily COVID-19 Cases with 7-Day Moving Average</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Analyze the daily reported COVID-19 cases along with a 7-day moving average for smoother trend visualization. This helps understand the pattern of new cases over time.
                    </p>
                """, unsafe_allow_html=True)
                plt.figure(figsize=(14, 8))
                plt.bar(datewise_data['ObservationDate'], datewise_data['daily_confirmed'], label='Daily New Cases', color='lightblue')
                plt.bar(datewise_data['ObservationDate'], datewise_data['daily_recovered'], label='Daily Recoveries', color='lightgreen')
                plt.bar(datewise_data['ObservationDate'], datewise_data['daily_deaths'], label='Daily Deaths', color='lightcoral')

                # Plot the 7-day moving average on top of bars
                plt.plot(datewise_data['ObservationDate'], datewise_data['7_day_avg_confirmed'], label='7-Day Avg New Cases', color='blue', linewidth=2)
                plt.plot(datewise_data['ObservationDate'], datewise_data['7_day_avg_recovered'], label='7-Day Avg Recoveries', color='green', linewidth=2)
                plt.plot(datewise_data['ObservationDate'], datewise_data['7_day_avg_deaths'], label='7-Day Avg Deaths', color='red', linewidth=2)

                # Add labels and title
                plt.xlabel('Date')
                plt.ylabel('Daily Cases')
                plt.title('Daily COVID-19 Cases with 7-Day Moving Average')
                plt.legend()
                plt.grid()

                st.pyplot(plt)
                plt.close()
            elif world_sub_option == "COVID-19 Cases Animated Heatmap":
            
                                # Load the datasets
                data_india = pd.read_csv("/Users/ayyalashriyatha/Desktop/complete.csv", encoding="cp1252")
                data_world = pd.read_csv("/Users/ayyalashriyatha/Desktop/time-series-19-covid-combined (1).csv")

                # Rename columns for consistency
                data_world = data_world.rename(columns={
                    "Lat": "Latitude",
                    "Long": "Longitude",
                    "Confirmed": "Total Confirmed cases",
                    "Date": "Date"
                })

                # Ensure date columns are in datetime format
                data_india["Date"] = pd.to_datetime(data_india["Date"])
                data_world["Date"] = pd.to_datetime(data_world["Date"])

                # Filter out rows with zero or missing cases
                data_india = data_india[data_india["Total Confirmed cases"] > 0]
                data_world = data_world[data_world["Total Confirmed cases"] > 0]

                # Combine datasets
                combined_data = pd.concat([
                    data_india[["Latitude", "Longitude", "Total Confirmed cases", "Date"]],
                    data_world[["Latitude", "Longitude", "Total Confirmed cases", "Date"]]
                ], ignore_index=True)

                # Group by date for HeatMapWithTime
                grouped_data = combined_data.groupby("Date")

                # Prepare heatmap data
                heatmap_data = []
                time_index = []

                for date, group in grouped_data:
                    heatmap_data.append(
                        group[["Latitude", "Longitude", "Total Confirmed cases"]].values.tolist()
                    )
                    time_index.append(str(date.date()))  # Store date for time slider

                # Create base map
                map = folium.Map(
                    location=[20, 0],  # Center of the world
                    zoom_start=2,
                    no_wrap=True,
                    max_bounds=True
                )

                # Add animated heatmap
                heatmap = HeatMapWithTime(
                    heatmap_data,
                    radius=7,  # Adjust the radius for better visualization
                    gradient={0.2: 'blue', 0.4: 'lime', 0.5: 'yellow', 0.6: 'red'},  # Color gradient
                    auto_play=True,
                    display_index=True,
                    index=time_index  # Pass the date information for the time slider
                )
                heatmap.add_to(map)

                # Streamlit app with download button to save the map
                st.title("COVID-19 Visualization")

                # Create download button to save the map
                if st.button("Download COVID-19 Animated Heatmap"):
                    # Create a temporary file to save the map HTML
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w') as tmpfile:
                        # Save the map to the temporary file
                        map.save(tmpfile.name)
                        
                        # Provide the file to download
                        with open(tmpfile.name, "rb") as f:
                            st.download_button(
                                label="Download Heatmap HTML",
                                data=f.read(),
                                file_name="covid_heatmap.html",
                                mime="application/octet-stream"
                            )

            elif world_sub_option == "Weekly Tests and Positivity Rate Over Time":
                st.markdown("<div class='sub-header'>Weekly Tests and Positivity Rate Over Time</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the trend of weekly tests conducted and the positivity rate over time. This helps in understanding the correlation between testing and the spread of the virus.
                    </p>
                """, unsafe_allow_html=True)
                fig, ax1 = plt.subplots(figsize=(14, 8))
                ax1.set_xlabel('Date', fontsize=14)
                ax1.set_ylabel('Weekly Tests', color='blue', fontsize=14)
                ax1.plot(aggregated_df['year_week_date'], aggregated_df['tests_done'], color='blue', label='Weekly Tests', linewidth=2)
                ax1.tick_params(axis='y', labelcolor='blue')

                # Configure grid lines for better readability
                ax1.grid(visible=True, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

                # Second y-axis for positivity rate
                ax2 = ax1.twinx()
                ax2.set_ylabel('Positivity Rate (%)', color='orange', fontsize=14)
                ax2.plot(aggregated_df['year_week_date'], aggregated_df['rolling_positivity_rate'], color='orange', linestyle='-', marker='o', label='Positivity Rate (%)', linewidth=2)
                ax2.tick_params(axis='y', labelcolor='orange')

                # Set x-axis major locator and formatter for better date visibility
                ax1.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Use 'nbins' instead of 'n'
                plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')  # Rotate x-axis labels for better visibility

                # Add legends
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')

                # Set title and layout
                fig.suptitle('Weekly Tests and Positivity Rate Over Time', fontsize=16)
                fig.tight_layout()

                # Use Streamlit to display the plot
                st.pyplot(fig)
                plt.close(fig)  # Close the figure to avoid displaying it twice

                fig, ax1 = plt.subplots(figsize=(16, 8))  # Adjusted size

                # Plot weekly tests on the first y-axis as a bar chart
                ax1.set_xlabel('Date', fontsize=14)
                ax1.set_ylabel('Weekly Tests', color='blue', fontsize=14)
                ax1.bar(aggregated_df['year_week_date'], aggregated_df['tests_done'], color='darkblue', alpha=0.6, label='Weekly Tests')
                ax1.tick_params(axis='y', labelcolor='blue')

                # Configure x-axis date format
                ax1.xaxis.set_major_locator(mdates.MonthLocator())
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
                plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')  # Rotate x-axis labels for better visibility

                # Second y-axis for positivity rate
                ax2 = ax1.twinx()
                ax2.set_ylabel('Positivity Rate (%)', color='red', fontsize=14)

                # Plot the rolling positivity rate with a dashed line style
                ax2.plot(aggregated_df['year_week_date'], aggregated_df['rolling_positivity_rate'], color='red', marker='o', linestyle='--', label='Positivity Rate (%)', linewidth=2)
                ax2.tick_params(axis='y', labelcolor='red')

                # Optionally, set limits for the y-axis to improve clarity
                ax2.set_ylim(0, aggregated_df['rolling_positivity_rate'].max() + 5)  # Adjust the limits as needed

                # Add legends and grid
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')
                ax1.grid(True)

                # Title and layout
                fig.suptitle('Weekly Tests and Positivity Rate Over Time', fontsize=16)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            elif world_sub_option == "Spread Of COVID-19 Over Time":
                st.markdown("<div class='sub-header'>Spread of COVID-19 Over Time</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Visualize the global spread of COVID-19 over time, with data on new cases and how the virus has spread across different regions.
                    </p>
                """, unsafe_allow_html=True)
                df['ObservationDate'] = pd.to_datetime(df['ObservationDate'])
                df_grouped = df.groupby(['ObservationDate', 'Country/Region'], as_index=False).agg(
                    {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum'}
                )

                # Create the animated scatter map
                fig = px.scatter_geo(
                    df_grouped,
                    locations="Country/Region",
                    locationmode="country names",
                    color="Confirmed",
                    size="Confirmed",
                    hover_name="Country/Region",
                    animation_frame=df_grouped["ObservationDate"].dt.strftime('%Y-%m-%d'),
                    title="Spread of COVID-19 Over Time",
                    template="plotly_dark",
                    color_continuous_scale="Reds",
                )

                fig.update_layout(
                    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
                )

                # Display the animation in Streamlit
                st.title("COVID-19 Spread Over Time")
                st.plotly_chart(fig)
        
        elif world_option == "Top Countries by COVID-19 Metrics":
            st.markdown("<div class='sub-header'>Top Countries by COVID-19 Metrics</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    Discover which countries are most impacted by COVID-19, based on cases, deaths, and recovery metrics.
                </p>
            """, unsafe_allow_html=True)
            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Top 10 Countries by Active COVID-19 Cases", 
                    "Top 10 Countries by Mortality Rate",
                    "COVID-19 Confirmed Cases by Country",
                    "COVID-19 Recovery Rates by Country",
                    "COVID-19 Mortality Rates by Country",
                    "COVID-19 Cumulative Confirmed Cases in Top 5 Countries",
                    "Country Clusters Based on COVID-19 Metrics"
                ),
                index=0,  # Default selection
                help="Explore various global COVID-19 data insights, including cases, recovery rates, mortality rates, and clustering of countries."
            )

            # Divider to visually separate sections
            st.markdown("<hr style='margin: 30px 0; border: 1px solid #cccccc;'>", unsafe_allow_html=True)
            if world_sub_option == "Top 10 Countries by Active COVID-19 Cases":
                st.markdown("<div class='sub-header'>Top 10 Countries by Active COVID-19 Cases</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        View the countries with the highest number of active COVID-19 cases. This data helps track the current global burden of the pandemic.
                    </p>
                """, unsafe_allow_html=True)
                st.header("Top 10 Countries by Active COVID-19 Cases")
                st.pyplot(plot_top_countries_active_cases(global_totals))

            elif world_sub_option == "COVID-19 Confirmed Cases by Country":
                st.markdown("<div class='sub-header'>COVID-19 Confirmed Cases by Country</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Get a detailed view of COVID-19 confirmed cases across different countries. This can help identify the most affected regions.
                    </p>
                """, unsafe_allow_html=True)
                st.header("COVID-19 Confirmed Cases by Country (Latest Data)")
                grouped_data = df.groupby(['ObservationDate', 'Country/Region']).agg({
                    'Confirmed': 'sum',
                    'Deaths': 'sum',
                    'Recovered': 'sum'
                }).reset_index()

                latest_data = grouped_data[grouped_data['ObservationDate'] == grouped_data['ObservationDate'].max()]

                fig = px.choropleth(
                    latest_data,
                    locations='Country/Region',
                    locationmode='country names',
                    color='Confirmed',
                    hover_name='Country/Region',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    labels={'Confirmed': 'Confirmed Cases'},
                    title='COVID-19 Confirmed Cases by Country (Latest Data)'
                )
                st.plotly_chart(fig)

            elif world_sub_option == "COVID-19 Cumulative Confirmed Cases in Top 5 Countries":
                st.markdown("<div class='sub-header'>COVID-19 Cumulative Confirmed Cases in Top 5 Countries</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        See the cumulative number of confirmed COVID-19 cases in the top 5 countries, helping to understand the pandemic's overall spread.
                    </p>
                """, unsafe_allow_html=True)
                df['ObservationDate'] = pd.to_datetime(df['ObservationDate'])
                df['Confirmed'] = pd.to_numeric(df['Confirmed'], errors='coerce').fillna(0)
                df['Deaths'] = pd.to_numeric(df['Deaths'], errors='coerce').fillna(0)
                df['Recovered'] = pd.to_numeric(df['Recovered'], errors='coerce').fillna(0)
                df['Active Cases'] = df['Confirmed'] - df['Recovered'] - df['Deaths']

                # Filter for the top 5 affected countries by max confirmed cases
                top_countries = df.groupby('Country/Region')['Confirmed'].max().nlargest(5).index
                df_top = df[df['Country/Region'].isin(top_countries)]

                # Streamlit App
                st.title("COVID-19 Cumulative Confirmed Cases - Top 5 Countries")

                # Sidebar for filtering
                selected_countries = st.sidebar.multiselect(
                    "Select Countries",
                    options=top_countries,
                    default=list(top_countries)
                )

                start_date = st.sidebar.date_input(
                    "Start Date",
                    value=df['ObservationDate'].min(),
                    min_value=df['ObservationDate'].min(),
                    max_value=df['ObservationDate'].max()
                )

                end_date = st.sidebar.date_input(
                    "End Date",
                    value=df['ObservationDate'].max(),
                    min_value=df['ObservationDate'].min(),
                    max_value=df['ObservationDate'].max()
                )

                # Filter data based on user input
                filtered_df = df_top[
                    (df_top['Country/Region'].isin(selected_countries)) &
                    (df_top['ObservationDate'] >= pd.to_datetime(start_date)) &
                    (df_top['ObservationDate'] <= pd.to_datetime(end_date))
                ]

                # Plot data
                fig = go.Figure()
                for country in selected_countries:
                    country_data = filtered_df[filtered_df['Country/Region'] == country]
                    fig.add_trace(go.Scatter(
                        x=country_data['ObservationDate'], 
                        y=country_data['Confirmed'],
                        mode='lines', 
                        name=country,
                        line=dict(width=2)
                    ))

                # Customize layout
                fig.update_layout(
                    title="Cumulative Confirmed COVID-19 Cases",
                    xaxis_title="Date",
                    yaxis_title="Confirmed Cases",
                    template="plotly_dark",
                    legend_title_text="Country",
                    hovermode="x unified",
                    margin=dict(t=50, l=20, r=20, b=50),
                    xaxis=dict(rangeslider=dict(visible=True), rangeselector=dict(buttons=[
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(step="all")
                    ])),
                )

                # Display the plot
                st.plotly_chart(fig, use_container_width=True)

            elif world_sub_option == "COVID-19 Mortality Rates by Country":
                st.markdown("<div class='sub-header'>COVID-19 Mortality Rates by Country</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Examine the mortality rates across countries to assess the impact of COVID-19 in different regions, which could inform health interventions.
                    </p>
                """, unsafe_allow_html=True)
                fig_mortality = px.choropleth(
                    df_map,
                    locations="iso_alpha",
                    color="Mortality_Rate",
                    hover_name="Country_Region",
                    animation_frame="Date",
                    color_continuous_scale=px.colors.sequential.Reds,
                    title='COVID-19 Mortality Rates by Country',
                    labels={'Mortality_Rate': 'Mortality Rate (%)'}
                )
                st.plotly_chart(fig_mortality)
            elif world_sub_option == "Country Clusters Based on COVID-19 Metrics":
                st.markdown("<div class='sub-header'>Country Clusters Based on COVID-19 Metrics</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore clusters of countries based on key COVID-19 metrics such as cases, recovery rates, and mortality rates. This helps identify patterns and groupings of similar regions.
                    </p>
                """, unsafe_allow_html=True)
                st.subheader("Country Clusters Based on COVID-19 Metrics")

                # Prepare data for clustering
                country_data = df.groupby("Country/Region")[['Confirmed', 'Deaths', 'Recovered']].sum()
                
                # Scale the data
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(country_data)
                
                # Apply KMeans clustering
                kmeans = KMeans(n_clusters=4, random_state=42).fit(scaled_data)
                country_data['Cluster'] = kmeans.labels_

                # Streamlit UI
                st.write("The following clusters are created based on the similarity in COVID-19 metrics (Confirmed Cases, Deaths, and Recoveries):")

                # Display country-wise cluster mapping
                cluster_table = country_data.reset_index()[['Country/Region', 'Cluster']].sort_values(by='Cluster')
                st.dataframe(cluster_table)

                # Scatter Plot with Plotly
                fig = px.scatter(
                    country_data.reset_index(),
                    x='Confirmed', y='Deaths',
                    color='Cluster',
                    hover_name='Country/Region',
                    size='Recovered',  # Bubble size as recovery cases
                    title="Country Clusters Based on COVID-19 Metrics",
                    template="plotly_dark",
                )
                
                # Display plot
                st.plotly_chart(fig)

            elif world_sub_option == "COVID-19 Recovery Rates by Country":
                st.markdown("<div class='sub-header'>COVID-19 Recovery Rates by Country</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Track recovery rates across countries to understand how effectively regions are managing and recovering from COVID-19.
                    </p>
                """, unsafe_allow_html=True)
                fig_recovery = px.choropleth(
                    df_map,
                    locations="iso_alpha",
                    color="Recovery_Rate",
                    hover_name="Country_Region",
                    animation_frame="Date",
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='COVID-19 Recovery Rates by Country',
                    labels={'Recovery_Rate': 'Recovery Rate (%)'}
                )

                st.plotly_chart(fig_recovery)

            elif world_sub_option == "Top 10 Countries by Mortality Rate":
                st.markdown("<div class='sub-header'>Top 10 Countries by Mortality Rate</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the countries with the highest mortality rates from COVID-19, which could help identify areas with high vulnerability.
                    </p>
                """, unsafe_allow_html=True)
                st.header("Top 10 Countries by Mortality Rate (%)")
                st.pyplot(plot_top_countries_mortality(global_totals))
            
    elif option == "Vaccination Analysis":
    # Main option for selecting vaccination visualization type
        world_option = st.radio(
            "Select Visualization:",
            options=(
                "Vaccination Coverage by Country",
                "Vaccination Trends and Totals",
                "Global Vaccination Insights"
            ),
            index=0,  # Default selection to "Vaccination Coverage by Country"
            help="Explore global vaccination data, including coverage, trends, and insights across countries."
        )

        # Divider for visual separation
        st.markdown("<hr style='margin: 30px 0; border: 1px solid #cccccc;'>", unsafe_allow_html=True)
        if world_option == "Vaccination Coverage by Country":
            st.markdown("<div class='sub-header'>Vaccination Coverage by Country</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    Dive deep into vaccination coverage across countries. Explore how different nations are progressing towards herd immunity with vaccination rates and doses administered.
                </p>
            """, unsafe_allow_html=True)

            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Total Vaccinations Administered by Country (Top 20)",
                    "Total Vaccinations per 100 People by Country (Top 20)",
                    "Choropleth Map of Percentage Vaccinated with at Least One Dose by Country",
                    "Total Vaccinations vs Per 100 People"
                ),
                help="Select a specific view to examine vaccination coverage, doses administered, and global trends."
            )
            if world_sub_option == "Total Vaccinations Administered by Country (Top 20)":
                st.markdown("<div class='sub-header'>Top 20 Countries by Total Vaccinations Administered</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        View the total number of COVID-19 vaccinations administered in the top 20 countries. This chart provides a comparison of vaccination efforts across regions.
                    </p>
                """, unsafe_allow_html=True)
                df3 = df3[df3['TOTAL_VACCINATIONS'].notna()]  # Filter out rows with NaN values in 'TOTAL_VACCINATIONS'
                # Top 20 countries by total vaccinations
                top_vaccinated_countries = df3.sort_values('TOTAL_VACCINATIONS', ascending=False).head(20)

                fig = plt.figure(figsize=(14, 8))
                sns.barplot(x='TOTAL_VACCINATIONS', y='COUNTRY', data=top_vaccinated_countries, hue="TOTAL_VACCINATIONS")
                plt.title('Total Vaccinations Administered by Country (Top 20)', fontsize=18)
                plt.xlabel('Total Vaccinations', fontsize=14)
                plt.ylabel('Country', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                st.pyplot(fig)

            elif world_sub_option == "Total Vaccinations per 100 People by Country (Top 20)":
                st.markdown("<div class='sub-header'>Top 20 Countries by Total Vaccinations per 100 People</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the top 20 countries with the highest number of vaccinations administered per 100 people. This metric highlights the relative vaccination effort in each country.
                    </p>
                """, unsafe_allow_html=True)
                top_vaccination_rate_countries = df3.sort_values('TOTAL_VACCINATIONS_PER100', ascending=False).head(20)

                fig = plt.figure(figsize=(14, 8))
                sns.barplot(x='TOTAL_VACCINATIONS_PER100', y='COUNTRY', data=top_vaccination_rate_countries, hue="TOTAL_VACCINATIONS_PER100")
                plt.title('Total Vaccinations per 100 People by Country (Top 20)', fontsize=18)
                plt.xlabel('Total Vaccinations per 100 People', fontsize=14)
                plt.ylabel('Country', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                st.pyplot(fig)
            
            elif world_sub_option == "Choropleth Map of Percentage Vaccinated with at Least One Dose by Country":
                st.markdown("<div class='sub-header'>Choropleth Map of Vaccination Percentage by Country</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Visualize a choropleth map showing the percentage of people vaccinated with at least one dose across countries. This map provides a global overview of vaccination progress.
                    </p>
                """, unsafe_allow_html=True)
                df3 = df3[df3['TOTAL_VACCINATIONS'].notnull()]  # Keep only rows with total vaccinations
                df3 = df3[df3['COUNTRY'].notnull()]  # Ensure country names are present

                # Optionally, convert 'WHO_REGION' to a categorical type for better visualization
                df3['WHO_REGION'] = df3['WHO_REGION'].astype('category')

                df3['PERCENT_VACCINATED_1PLUS_DOSE'] = (df3['PERSONS_VACCINATED_1PLUS_DOSE'] / df3['TOTAL_VACCINATIONS']) * 100

                # Create a choropleth map
                fig = px.choropleth(
                    df3,
                    locations='ISO3',  # Use ISO3 codes for location matching
                    color='PERCENT_VACCINATED_1PLUS_DOSE',  # Data to be represented
                    hover_name='COUNTRY',  # Hover data
                    color_continuous_scale=px.colors.sequential.Plasma,  # Color scale
                    labels={'PERCENT_VACCINATED_1PLUS_DOSE': 'Percentage Vaccinated (1+ Dose)'},
                    title='Choropleth Map of Percentage Vaccinated with at Least One Dose by Country'
                )

                # Show the figure
                fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="LightGreen")
                st.plotly_chart(fig)
            elif world_sub_option == "Total Vaccinations vs Per 100 People":
                st.markdown("<div class='sub-header'>Total Vaccinations vs Vaccinations per 100 People</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Compare the total number of vaccinations administered against the number of vaccinations per 100 people. This visualization helps identify the countries with the highest absolute and relative vaccination coverage.
                    </p>
                """, unsafe_allow_html=True)
                df3.dropna(subset=['TOTAL_VACCINATIONS', 'TOTAL_VACCINATIONS_PER100'], inplace=True)

                # Add a 'Population' column (assumed from 'Total Vaccinations' and 'Vaccinations per 100 people')
                df3['POPULATION'] = (df3['TOTAL_VACCINATIONS'] / df3['TOTAL_VACCINATIONS_PER100']) * 100

                # Streamlit app
                st.title("Interactive Vaccination Data Bubble Chart")

                # Dropdown to filter by WHO region
                regions = df3['WHO_REGION'].unique()
                selected_region = st.selectbox(
                    "Filter by WHO Region:",
                    options=['All'] + list(regions),
                    index=0
                )

                # Filter data based on the selected region
                if selected_region != 'All':
                    filtered_df = df3[df3['WHO_REGION'] == selected_region]
                else:
                    filtered_df = df3

                # Create the bubble chart using Plotly
                fig_bubble = px.scatter(
                    filtered_df, 
                    x='TOTAL_VACCINATIONS_PER100', 
                    y='TOTAL_VACCINATIONS', 
                    size='POPULATION', 
                    color='WHO_REGION', 
                    hover_name='COUNTRY', 
                    title="Vaccination Data: Total Vaccinations vs. Per 100 People",
                    labels={
                        'TOTAL_VACCINATIONS': 'Total Vaccinations',
                        'TOTAL_VACCINATIONS_PER100': 'Vaccinations per 100 People'
                    },
                    size_max=60,
                    height=600
                )

                # Display the chart in Streamlit
                st.plotly_chart(fig_bubble, use_container_width=True)

        
        elif world_option == "Global Vaccination Insights":
            st.markdown("<div class='sub-header'>Global Vaccination Insights</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    Gain insights into global vaccination efforts, including the total number of vaccinations administered, coverage in various regions, and comparison across continents.
                </p>
            """, unsafe_allow_html=True)
            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Total Vaccinations by WHO Region",
                    "Vaccination Stages by Top 10 Countries"
                ),
                help="Select a specific visualization to explore vaccination distribution and progress across regions and top countries."
            )
            if world_sub_option == "Total Vaccinations by WHO Region":
                st.markdown("<div class='sub-header'>Total Vaccinations by WHO Region</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the total number of COVID-19 vaccinations administered by WHO region. This visualization breaks down vaccination efforts globally, highlighting progress by region.
                    </p>
                """, unsafe_allow_html=True)
                region_vaccinations = df3.groupby('WHO_REGION')['TOTAL_VACCINATIONS'].sum().reset_index()
                fig = plt.figure(figsize=(10, 6))
                sns.barplot(x='TOTAL_VACCINATIONS', y='WHO_REGION', data=region_vaccinations, hue='TOTAL_VACCINATIONS')
                plt.title('Total Vaccinations by WHO Region', fontsize=18)
                plt.xlabel('Total Vaccinations', fontsize=14)
                plt.ylabel('WHO Region', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                st.pyplot(fig)

            elif world_sub_option == "Vaccination Stages by Top 10 Countries":
                st.markdown("<div class='sub-header'>Vaccination Stages by Top 10 Countries</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        See the current vaccination stages for the top 10 countries with the highest vaccination totals. This visualization provides a clear comparison of the stages each country is in regarding vaccinations (e.g., first dose, second dose, fully vaccinated).
                    </p>
                """, unsafe_allow_html=True)
                top_countries = df3.nlargest(10, 'TOTAL_VACCINATIONS')
                # Select necessary columns for stacked bar chart
                df_stacked = top_countries[['COUNTRY', 'PERSONS_VACCINATED_1PLUS_DOSE', 'PERSONS_LAST_DOSE', 'PERSONS_BOOSTER_ADD_DOSE']]
                df_stacked.set_index('COUNTRY').plot(kind='bar', stacked=True, figsize=(14, 7), color=['skyblue', 'orange', 'green'])

                # Customize chart
                plt.title('Vaccination Stages by Top 10 Countries')
                plt.xlabel('Country')
                plt.ylabel('Number of Vaccinations')
                plt.legend(title='Vaccination Type', labels=['1+ Dose', 'Last Dose', 'Booster Dose'])
                plt.xticks(rotation=45)

                # Display chart in Streamlit
                st.pyplot(plt.gcf())
            
        elif world_option == "Vaccination Trends and Totals":
            st.markdown("<div class='sub-header'>Vaccination Trends and Totals</div>", unsafe_allow_html=True)
            st.markdown("""
                <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                    Analyze global vaccination trends over time, including totals, daily vaccinations, and the progress of different countries towards vaccination goals.
                </p>
            """, unsafe_allow_html=True)

            world_sub_option = st.radio(
                "Choose Visualization:",
                options=(
                    "Cumulative Vaccinations Over Time",
                    "Booster Doses Administered by Country (Top 20)"
                ),
                help="Choose between visualizing the cumulative progress of vaccinations over time or exploring booster doses administered in the top 20 countries."
            )

            if world_sub_option == "Cumulative Vaccinations Over Time":
                st.markdown("<div class='sub-header'>Cumulative Vaccinations Over Time</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        This visualization tracks the global cumulative total of COVID-19 vaccinations over time. It allows you to observe the overall progress in vaccination campaigns worldwide and identify key milestones.
                    </p>
                """, unsafe_allow_html=True)
                if 'DATE_UPDATED' in df3.columns:
                    df3['DATE_UPDATED'] = pd.to_datetime(df3['DATE_UPDATED'], errors='coerce')
                    df3.set_index('DATE_UPDATED', inplace=True)

                fig = plt.figure(figsize=(14, 8))
                cumulative_vaccinations = df3['TOTAL_VACCINATIONS'].resample('ME').sum().cumsum()
                sns.lineplot(x=cumulative_vaccinations.index, y=cumulative_vaccinations, color='blue')
                plt.title('Cumulative Vaccinations Over Time', fontsize=18)
                plt.xlabel('Date', fontsize=14)
                plt.ylabel('Cumulative Total Vaccinations', fontsize=14)
                plt.xticks(rotation=45)
                plt.grid()
                st.pyplot(fig)

            elif world_sub_option == "Booster Doses Administered by Country (Top 20)":
                st.markdown("<div class='sub-header'>Booster Doses Administered by Country (Top 20)</div>", unsafe_allow_html=True)
                st.markdown("""
                    <p style="color: #d1d5db; font-size: 1.1rem; text-align: center; margin-top: 20px;">
                        Explore the number of booster doses administered by the top 20 countries. This visualization highlights countries leading in booster dose campaigns, showcasing their commitment to increasing immunity and addressing variants.
                    </p>
                """, unsafe_allow_html=True)
                top_booster_countries = df3.sort_values('PERSONS_BOOSTER_ADD_DOSE', ascending=False).head(20)
                fig = plt.figure(figsize=(14, 8))
                sns.barplot(x='PERSONS_BOOSTER_ADD_DOSE', y='COUNTRY', data=top_booster_countries, hue="PERSONS_BOOSTER_ADD_DOSE")
                plt.title('Booster Doses Administered by Country (Top 20)', fontsize=18)
                plt.xlabel('Number of Booster Doses Administered', fontsize=14)
                plt.ylabel('Country', fontsize=14)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
                st.pyplot(fig)
            


        
if __name__ == "__main__":
    main()
