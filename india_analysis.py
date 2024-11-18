import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry
import seaborn as sns
import folium
import geopandas as gpd
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import json

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    layout="wide",  # Full-width layout
    initial_sidebar_state="collapsed"  # Hide the sidebar
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
    <h1>India COVID-19 Data Dashboard</h1>
</div>
<div class="sub-header">
    Discover critical COVID-19 trends, vaccination data, and insights to stay ahead in the fight against the pandemic.
</div>
""", unsafe_allow_html=True)

# Dashboard description with updated professional tone
st.markdown("""
<div class="description">
    Welcome to the **India COVID-19 Data Dashboard**, your go-to platform for the latest COVID-19 metrics and trends. 
    This dashboard offers:
    - **Real-time updates** on vaccination progress and case statistics.
    - **Interactive charts** for trend analysis.
    - **Actionable insights** to understand regional and national scenarios better.
    
    Use the tools and visualizations below to dive deeper into India's COVID-19 data and empower yourself with informed decisions. Together, we can navigate this crisis with clarity and resilience.
</div>
""", unsafe_allow_html=True)





def plot_statewise_data(statewise_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(statewise_data.index, statewise_data['Confirmed'], color='orange')
    ax.set_xlabel('Confirmed Cases')
    ax.set_title('State-wise Confirmed COVID-19 Cases in India')
    ax.invert_yaxis()
    return fig
def compare_daily_cases_with_slider(state1, state2, data):
    """
    Function to compare daily new COVID-19 cases between two states with a live timeline graph and slider.

    Parameters:
    - state1: Name of the first state
    - state2: Name of the second state
    - data: DataFrame containing COVID-19 data with columns: 'Date', 'Name of State / UT', 'New cases'
    
    Returns:
    - An interactive plot comparing daily new cases for the two states with a slider.
    """
    
    # Filter data for the two states
    state1_data = data[data['Name of State / UT'] == state1]
    state2_data = data[data['Name of State / UT'] == state2]
    
    # Check if both states are in the dataset
    if state1_data.empty or state2_data.empty:
        print(f"Error: One or both states ({state1}, {state2}) not found in the dataset.")
        return
    
    # Create traces for both states
    trace1 = go.Scatter(x=state1_data['Date'], 
                        y=state1_data['New cases'], 
                        mode='lines', 
                        name=state1, 
                        line=dict(color='blue'))
    
    trace2 = go.Scatter(x=state2_data['Date'], 
                        y=state2_data['New cases'], 
                        mode='lines', 
                        name=state2, 
                        line=dict(color='red'))

    # Create frames for the animation
    frames = [go.Frame(
        data=[go.Scatter(x=state1_data['Date'][:k], y=state1_data['New cases'][:k], mode='lines', name=state1),
              go.Scatter(x=state2_data['Date'][:k], y=state2_data['New cases'][:k], mode='lines', name=state2)],
        name=str(i)
    ) for i, k in enumerate(range(1, len(state1_data)+1))]
    
    # Create layout with a slider
    layout = go.Layout(
        title=f"Comparison of Daily New COVID-19 Cases: {state1} vs {state2}",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Daily New Cases"),
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }],
        sliders=[{
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'visible': True,
                'xanchor': 'right',
                'prefix': 'Date: ',
                'visible': True
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10},
            'len': 0.9,
            'x': 0.1,
            'y': 0.0,
            'steps': [{
                'args': [
                    [f'{state1_data["Date"].iloc[i]}'],
                    {'frame': {'duration': 500, 'redraw': True}, 'mode': 'immediate'}
                ],
                'label': f'{state1_data["Date"].iloc[i]}',
                'method': 'animate'
            } for i in range(len(state1_data))]
        }]
    )
    
    # Create the figure with data and frames
    fig = go.Figure(data=[trace1, trace2], layout=layout, frames=frames)
    
    # Show the figure
    fig.show()
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
    global_totals['Mortality Rate'] = (global_totals['Deaths'] / global_totals['Confirmed']) * 100

    # Prepare datewise data
    datewise_data = global_data.groupby('ObservationDate').sum(numeric_only=True).reset_index()
    datewise_data['Daily Confirmed'] = datewise_data['Confirmed'].diff().fillna(0)
    datewise_data['Growth Rate'] = datewise_data['Daily Confirmed'].pct_change().fillna(0) * 100

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

    return global_totals_sum, global_totals, statewise_data, datewise_data

def main():
    

    # Dropdown for analysis options
    option = st.selectbox(
        label="Select Analysis Type:",
        options=["Home", "Vaccination Analysis", "COVID-19 Cases and Deaths Analysis"],
        index=0,
        help="Navigate through different COVID-19 data analyses for India."
    )

    # Divider with a subtle accent color
    st.markdown("""
    <hr style="border: 0; border-top: 2px solid #82b1ff; margin: 40px 0;">
    """, unsafe_allow_html=True)

    # Additional information or navigation prompt
    st.markdown("""
    <div class="description" style="text-align: center; color: #e5e7eb; font-size: 1.1rem;">
        Use the dropdown above to navigate to the section you wish to explore:
        <ul style="text-align: left; margin-top: 20px;">
            <li><strong style="color: #bb86fc;">Vaccination Analysis</strong>: Track vaccination progress across states and age groups.</li>
            <li><strong style="color: #bb86fc;">COVID-19 Cases and Deaths Analysis</strong>: Understand trends in reported cases, recoveries, and mortality rates.</li>
        </ul>
        <br>
        Explore, analyze, and gain insights into India's ongoing fight against COVID-19.
    </div>
    """, unsafe_allow_html=True)

    # Now render the selected analysis based on the dropdown choice
    if option == "Home":
        st.subheader("Welcome to the COVID-19 Analysis Dashboard")
        st.write("Choose an analysis option to explore further.")

    global_totals_sum, global_totals, statewise_data, datewise_data = load_and_prepare_data()
    covid_19 = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_19_india.csv')
    covid_vaccine = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_vaccine_statewise.csv')
    df = pd.read_csv('/Users/ayyalashriyatha/Desktop/covid_19_india.csv')
    covid_df = covid_19.drop(["Sno","Time","ConfirmedIndianNational","ConfirmedForeignNational"],axis=1)
    covid_df['Active_cases']=covid_df['Confirmed']-(covid_df['Cured']+covid_df['Deaths'])
    covid_df['State/UnionTerritory']=covid_df['State/UnionTerritory'].replace('Maharashtra***',"Maharashtra")
    covid_df['State/UnionTerritory']=covid_df['State/UnionTerritory'].replace('Bihar****',"Bihar")
    covid_df['State/UnionTerritory']=covid_df['State/UnionTerritory'].replace('Madhya Pradesh***',"Madhya Pradesh")
    covid_df['State/UnionTerritory']=covid_df['State/UnionTerritory'].replace('Karanataka',"Karnataka")
    top10ActiveCases=covid_df.groupby(by='State/UnionTerritory').max()[['Active_cases','Date']].sort_values(by=['Active_cases'],ascending=False).reset_index()

    df11 = pd.read_csv('/Users/ayyalashriyatha/Desktop/complete.csv')
    df11['Name of State / UT'] = df11['Name of State / UT'].replace({
        'Telengana': 'Telangana',
        'Telangana***': 'Telangana',
        'Union Territory of Ladakh': 'Ladakh',
        'Union Territory of Jammu and Kashmir': 'Jammu and Kashmir',
        'Union Territory of Chandigarh': 'Chandigarh'
    })

    # Convert Date column to datetime
    df11['Date'] = pd.to_datetime(df11['Date'], errors='coerce')

    # Convert Death column to numeric, handling non-numeric entries by setting them to NaN
    df11['Death'] = pd.to_numeric(df11['Death'], errors='coerce')
    df11['Death']=df11['Death'].fillna(0)

    vaccination=covid_vaccine.drop(columns=['Sputnik V (Doses Administered)','AEFI','18-44 Years (Doses Administered)','45-60 Years (Doses Administered)','60+ Years (Doses Administered)'],axis=1)
    vaccine=covid_vaccine[covid_vaccine.State!='India']
    vaccine = vaccine.rename(columns={'Total Individuals Vaccinated':"Total"})

        #Most vaccinated State
    max_vacc=vaccine.groupby('State')['Total'].sum().to_frame('Total')
    max_vacc=max_vacc.sort_values(by='Total',ascending=False)[:10]

        #Least vaccinated State
    min_vacc=vaccine.groupby('State')['Total'].sum().to_frame('Total')
    min_vacc=min_vacc.sort_values(by='Total',ascending=True)[:10]

    if option == "Vaccination Analysis":
        st.markdown("""
        <div class="section">
            <h2 style="color: #82b1ff; text-align: center; margin-bottom: 20px;">Vaccination Analysis in India</h2>
            <p style="color: #d1d5db; text-align: center; font-size: 1.2rem;">
                Dive into detailed insights about COVID-19 vaccination progress in India. Explore interactive visualizations 
                showcasing demographics, state-wise coverage, and trends.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Grouped Dropdown Menu for Selecting Visualization
        st.markdown("""
        <div class="section" style="margin-top: 30px;">
            <h3 style="color: #bb86fc; margin-bottom: 15px;">Select a Visualization to Explore</h3>
        </div>
        """, unsafe_allow_html=True)
        visualization_option = st.selectbox(
            label="Choose a category:",
            options=["Demographics", "State Coverage", "Trends"],
            index=0,
            help="Select a category to explore vaccination data in detail."
        )

        
        if visualization_option == "Demographics":
            st.markdown("""
            <div class="section" style="margin-top: 30px;">
                <h3 style="color: #bb86fc;">Demographic Visualizations</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Analyze vaccination distribution across various demographics such as gender and age groups.
                </p>
            </div>
            """, unsafe_allow_html=True)
            demo_option = st.radio(
                label="Select Demographic Visualization:",
                options=[
                    "Male vs Female Vaccination",
                    "Gender-wise Distribution of Doses",
                    "Age-wise Distribution of Doses"
                ],
                index=0,
                help="Choose a specific demographic breakdown for vaccination data."
            )
            st.write(f"### You selected: {demo_option}")
            if demo_option == "Male vs Female Vaccination":
                st.markdown("""
                <div class="description">
                    <strong>Male vs Female Vaccination:</strong> Explore how vaccination efforts are distributed between 
                    males and females in different regions. This data helps understand gender parity in vaccination drives.
                </div>
                """, unsafe_allow_html=True)
                data = {
                    'Gender': ['Male', 'Female'],
                    'Vaccinations': [vaccination['Male(Individuals Vaccinated)'].sum(), vaccination['Female(Individuals Vaccinated)'].sum()]
                }
                vaccination_df = pd.DataFrame(data)

                # Create the pie chart
                fig = px.pie(
                    vaccination_df,
                    names='Gender',
                    values='Vaccinations',
                    title="Male vs Female Vaccination",
                    color=['#1f77b4', '#ff7f0e'],  # Custom colors for male and female
                    hole=0.3  # Makes it a donut chart
                )

                # Update the traces to show percentages
                fig.update_traces(textinfo='label+percent', pull=[0.1, 0])  # Pull out the male section slightly

                # Update the layout for better appearance
                fig.update_layout(
                    title_font=dict(size=20, color='black', family="Arial"),
                    legend=dict(title="Gender"),
                    margin=dict(t=50, b=0, l=0, r=0)  # Adjust margins for better spacing
                )

                # Show the figure
                st.plotly_chart(fig)
            elif demo_option == "Gender-wise Distribution of Doses":
                st.markdown("""
                <div class="description">
                    <strong>Gender-wise Distribution of Doses:</strong> See the distribution of doses (first, second, and booster) 
                    across gender categories. Gain insights into equitable dose distribution among genders.
                </div>
                """, unsafe_allow_html=True)
                age_groups = ['18-44 Years (Doses Administered)', '45-60 Years (Doses Administered)', '60+ Years (Doses Administered)']
                age_distribution = covid_vaccine[age_groups].sum()

                # Bar Chart for Age-wise Distribution of Vaccination
                fig = plt.figure(figsize=(10, 6))
                plt.bar(age_distribution.index, age_distribution.values, color='lightblue')
                plt.title('Age-wise Distribution of Vaccination Doses Administered')
                plt.xlabel('Age Group')
                plt.ylabel('Number of Doses Administered')
                plt.xticks(rotation=45)
                plt.grid(axis='y')
                st.pyplot(fig)
            elif demo_option == "Age-wise Distribution of Doses":
                st.markdown("""
                <div class="description">
                    <strong>Age-wise Distribution of Doses:</strong> Visualize vaccination rates across different age groups 
                    to understand the outreach to vulnerable populations.
                </div>
                """, unsafe_allow_html=True)
                gender_groups = ['Male (Doses Administered)', 'Female (Doses Administered)', 'Transgender (Doses Administered)']
                gender_distribution = covid_vaccine[gender_groups].sum()

                # Bar Chart for Gender-wise Distribution of Vaccination
                fig = plt.figure(figsize=(10, 6))
                plt.bar(gender_distribution.index, gender_distribution.values, color='lightgreen')
                plt.title('Gender-wise Distribution of Vaccination Doses Administered')
                plt.xlabel('Gender')
                plt.ylabel('Number of Doses Administered')
                plt.xticks(rotation=45)
                plt.grid(axis='y')
                st.pyplot(fig)

        elif visualization_option == "State Coverage":
            st.markdown("""
            <div class="section" style="margin-top: 30px;">
                <h3 style="color: #bb86fc;">State Coverage Visualizations</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Explore the vaccination progress across different states in India. Understand which regions have the highest 
                    and lowest coverage, and analyze vaccination efforts on a geographical scale.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Radio button for selecting specific state coverage visualization
            state_option = st.radio(
                label="Select a State Coverage Visualization:",
                options=[
                    "Top 10 Vaccinated States",
                    "Least 10 Vaccinated States",
                    "Vaccination by State",
                    "Geographical Heat Map of Vaccination Coverage"
                ],
                index=0,
                help="Choose an analysis type to explore state-wise vaccination data."
            )
            
            # Display the selected option dynamically
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Option:</strong> <span style="color: #bb86fc;">{state_option}</span>
            </div>
            """, unsafe_allow_html=True)
            if state_option == "Top 10 Vaccinated States":
                st.markdown("""
                <div class="description">
                    <strong>Top 10 Vaccinated States:</strong> Explore the states with the highest number of vaccinated individuals. 
                    This visualization highlights the success stories in vaccination efforts and their demographic impact.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for actual visualization (e.g., bar chart)
                st.write("📊 [Bar Chart Placeholder: Top 10 Vaccinated States]")
                fig, ax = plt.subplots(figsize=(12, 6))
                plt.title("Top 10 Vaccinated States in India", fontsize=20, fontweight='bold')

                # Create a bar plot with hue set to 'State/Union Territory'
                palette = sns.color_palette("Blues", len(max_vacc.iloc[:10]))
                max_value_index = max_vacc['Total'].idxmax()  # Get the index of the maximum value

                sns.barplot(
                    data=max_vacc.iloc[:10],
                    y='Total',
                    x=max_vacc.index[:10],
                    hue=max_vacc.index[:10],  # Set the hue to the x variable
                    linewidth=2,
                    edgecolor='black',
                    palette=palette,
                    legend=False  # Disable the legend since hue is used for the same variable
                )

                # Change color of the bar with the maximum value
                for p in ax.patches:
                    if p.get_height() == max_vacc['Total'].max():
                        p.set_color('#FF6347')  # Highlight color for maximum value

                # Add data labels on top of the bars
                for p in ax.patches:
                    ax.annotate(
                        f'{int(p.get_height())}',  # Get the height of the bar for labeling
                        (p.get_x() + p.get_width() / 2., p.get_height()),  # Positioning the label
                        ha='center', va='bottom', fontsize=12, fontweight='bold'
                    )

                # Set x and y labels
                ax.set_xlabel("States", fontsize=14)
                ax.set_ylabel("Total Vaccinations", fontsize=14)

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45, ha='right')

                # Add gridlines with lighter style
                ax.yaxis.grid(True, linestyle='--', alpha=0.5)
                plt.tight_layout()

                st.pyplot(fig)
            
            elif state_option == "Least 10 Vaccinated States":
                st.markdown("""
                <div class="description">
                    <strong>Least 10 Vaccinated States:</strong> Analyze states with the lowest vaccination rates. 
                    This data can help identify areas requiring more focused vaccination campaigns.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for visualization
                st.write("📉 [Bar Chart Placeholder: Least 10 Vaccinated States]")
                # Create the figure
                fig, ax = plt.subplots(figsize=(12, 5))
                plt.title("Least 5 Vaccinated States in India", fontsize=20, fontweight='bold')

                # Create a bar plot for the least vaccinated states
                # Assuming `min_vacc` contains the states with the least vaccinations
                sns.barplot(
                    data=min_vacc.iloc[:10],  # Only take the least 5
                    y='Total',
                    x=min_vacc.index[:10],
                    hue=min_vacc.index[:10],  # Set the hue to the x variable
                    linewidth=2,
                    edgecolor='black',
                    palette='pastel',  # Using a pastel color palette for softer colors
                    legend=False  # Disable the legend since hue is used for the same variable
                )

                # Add data labels on top of the bars
                for p in ax.patches:
                    ax.annotate(
                        f'{int(p.get_height())}',  # Get the height of the bar for labeling
                        (p.get_x() + p.get_width() / 2., p.get_height()),  # Positioning the label
                        ha='center', va='bottom', fontsize=12, fontweight='bold'
                    )

                # Set x and y labels
                ax.set_xlabel("States", fontsize=14)
                ax.set_ylabel("Total Vaccinations", fontsize=14)
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=30, ha='right')

                # Add gridlines to the y-axis for better visibility
                ax.yaxis.grid(True, linestyle='--', alpha=0.7)

                # Adjust layout for better spacing
                plt.tight_layout()

                st.pyplot(fig)
            elif state_option == "Vaccination by State":
                st.markdown("""
                <div class="description">
                    <strong>Vaccination by State:</strong> A comprehensive visualization of vaccination progress across all states. 
                    Compare vaccination rates and trends at a glance.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for visualization
                st.write("📊 [Comprehensive State Data Visualization Placeholder]")
                                # Summing vaccination doses for each state across all age groups
                vaccine['Total Doses Administered'] = (vaccine['18-44 Years (Doses Administered)'] + 
                                                vaccine['45-60 Years (Doses Administered)'] + 
                                                vaccine['60+ Years (Doses Administered)'])

                # Aggregating by state
                df_state_vaccination = vaccine.groupby('State')['Total Doses Administered'].sum().reset_index()

                # Create the bar plot using Plotly Express
                fig = px.bar(df_state_vaccination, 
                            x='State', 
                            y='Total Doses Administered',
                            title='Total Vaccination Doses Administered by State',
                            labels={'State': 'State', 'Total Doses Administered': 'Total Doses Administered'},
                            template='plotly_dark')

                # Customize layout for a cleaner look
                fig.update_layout(
                    xaxis_tickangle=-45,
                    xaxis_title='State',
                    yaxis_title='Total Doses Administered',
                    showlegend=False
                )

                # Streamlit interface
                st.title("Vaccination Data Visualization")
                st.write("This chart shows the total vaccination doses administered by state.")

                # Display the plotly figure inside Streamlit
                st.plotly_chart(fig)

            elif state_option == "Geographical Heat Map of Vaccination Coverage":
                st.markdown("""
                <div class="description">
                    <strong>Geographical Heat Map of Vaccination Coverage:</strong> Visualize vaccination distribution 
                    geographically across India. This heat map highlights regions with varying levels of coverage for targeted analysis.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for geographical heat map
                st.write("🗺️ [Heat Map Placeholder: Vaccination Coverage]")
                vaccine.columns = vaccine.columns.str.strip()

                # Ensure 'State' names in your DataFrame match the GeoJSON state names
                vaccine['State'] = vaccine['State'].str.strip()  # Remove extra spaces from state names in DataFrame

                # Load Indian states GeoJSON file
                with open('/Users/ayyalashriyatha/Desktop/Indian_states.geojson', 'r') as f:
                    india_states_geojson = json.load(f)

                # Create choropleth map for Indian states using GeoJSON
                fig = px.choropleth(vaccine, 
                                    locations="State", 
                                    geojson=india_states_geojson,
                                    color="Total Doses Administered", 
                                    hover_name="State", 
                                    hover_data=["Covaxin (Doses Administered)", 
                                                "CoviShield (Doses Administered)", 
                                                "Sputnik V (Doses Administered)"],
                                    color_continuous_scale="Viridis", 
                                    title="COVID-19 Vaccination Coverage Across India by State",
                                    locationmode="geojson-id",  # Use 'geojson-id' instead of 'geojson'
                                    featureidkey="properties.NAME_1")  # Match state names with 'NAME_1'

                # Update geojson layout for India
                fig.update_geos(fitbounds="locations")

                # Streamlit Layout
                st.title("Interactive Vaccination Coverage Map for India")
                st.plotly_chart(fig) 

        elif visualization_option == "Trends":
            st.markdown("""
            <div class="section" style="margin-top: 30px;">
                <h3 style="color: #bb86fc;">Vaccination Trends</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Analyze the vaccination trends in India over time. Explore how vaccination efforts have progressed and 
                    visualize patterns that can inform future health policies.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Radio button for trend visualizations
            trends_option = st.radio(
                label="Select a Trend Visualization:",
                options=[
                    "Vaccination Rate Over Time",
                    "Interactive Animated Line Chart for Vaccination Coverage"
                ],
                index=0,
                help="Choose a trend visualization to analyze vaccination progress over time."
            )
            
            # Dynamic feedback for the user's selection
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Trend:</strong> <span style="color: #bb86fc;">{trends_option}</span>
            </div>
            """, unsafe_allow_html=True)
            if trends_option == "Vaccination Rate Over Time":
                st.markdown("""
                <div class="description">
                    <strong>Vaccination Rate Over Time:</strong> View how vaccination rates have evolved over weeks and months. 
                    This trend highlights key milestones and periods of increased or decreased vaccination activity.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for visualization
                st.write("📈 [Line Chart Placeholder: Vaccination Rate Over Time]")
                covid_vaccine = covid_vaccine[covid_vaccine['State'] != 'India']
                covid_vaccine['Updated On'] = pd.to_datetime(covid_vaccine['Updated On'], errors='coerce', dayfirst=True)


                # Group by 'Updated On' for cumulative vaccination rate over time
                df_time = covid_vaccine.groupby('Updated On').sum()
                df_time['Cumulative First Dose'] = df_time['First Dose Administered'].cumsum()
                df_time['Cumulative Second Dose'] = df_time['Second Dose Administered'].cumsum()

                # Plot line chart for vaccination rate over time
                fig = plt.figure(figsize=(10, 6))
                plt.plot(df_time.index, df_time['Cumulative First Dose'], label="First Dose")
                plt.plot(df_time.index, df_time['Cumulative Second Dose'], label="Second Dose")
                plt.xlabel("Date")
                plt.ylabel("Cumulative Doses Administered")
                plt.title("Vaccination Rate Over Time")
                plt.legend()
                st.pyplot(fig)
            elif trends_option == "Interactive Animated Line Chart for Vaccination Coverage":
                st.markdown("""
                <div class="description">
                    <strong>Interactive Animated Line Chart:</strong> Experience vaccination trends dynamically with an 
                    animated chart. Watch how coverage has changed across time, creating a clear picture of progress.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for animated visualization
                st.write("📊 [Animated Line Chart Placeholder: Vaccination Coverage]")
                vaccine['State'] = vaccine['State'].str.strip()  # Clean any extra spaces or characters
                vaccine['Date'] = pd.to_datetime(vaccine['Updated On'])

                # Streamlit Layout
                st.title("Interactive Animated Line Chart for Vaccination Coverage")

                # Create a dropdown to select the vaccine
                vaccine_options = {
                    'Covaxin': ' Covaxin (Doses Administered)',
                    'CoviShield': 'CoviShield (Doses Administered)',
                    'Sputnik V': 'Sputnik V (Doses Administered)',
                    'All Vaccines': 'all'
                }

                selected_vaccine = st.selectbox(
                    'Select Vaccine to Display:',
                    options=list(vaccine_options.keys()),
                    index=3  # Default to 'All Vaccines'
                )

                # Filter data based on selected vaccine
                if selected_vaccine != 'All Vaccines':
                    selected_vaccine_column = vaccine_options[selected_vaccine]
                    filtered_df = vaccine[['State', 'Date', selected_vaccine_column]]
                    fig = px.line(filtered_df, x='Date', y=selected_vaccine_column, color='State', 
                                title=f"{selected_vaccine} Vaccination Coverage Over Time", 
                                labels={selected_vaccine_column: "Doses Administered"})
                else:
                    # Reshape the data to long format for all vaccines
                    long_df = vaccine.melt(id_vars=['State', 'Date'], 
                                        value_vars=[' Covaxin (Doses Administered)', 
                                                    'CoviShield (Doses Administered)', 
                                                    'Sputnik V (Doses Administered)'],
                                        var_name='Vaccine', 
                                        value_name='Doses Administered')
                    
                    # Plot all vaccine data in long format
                    fig = px.line(long_df, x='Date', y='Doses Administered', color='State', 
                                line_group='Vaccine', title="All Vaccines Vaccination Coverage Over Time", 
                                labels={"Doses Administered": "Doses Administered", "Vaccine": "Vaccine Type"})

                # Customize layout for better visuals
                fig.update_layout(
                    title='Vaccination Coverage Over Time',
                    xaxis_title='Date',
                    yaxis_title='Doses Administered',
                    hovermode='closest',
                    template='plotly_dark',  # Change chart template for visual appeal
                    showlegend=True
                )

                # Display the plot
                st.plotly_chart(fig)

        
        
        
        
    if option == "COVID-19 Cases and Deaths Analysis":
        st.title("India COVID-19 Analytics")

        # Grouped Dropdown Menu for Selecting Visualization
        category = st.selectbox(
            "Select a Category to Explore:",
            options=[
                "State-wise Analysis",
                "Top States",
                "Trends",
                "Comparisons",
                "Heat Maps"
            ]
        )
        if category == "State-wise Analysis":
            st.markdown("""
            <div class="section">
                <h3 style="color: #bb86fc;">State-wise COVID-19 Analysis</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Dive into detailed insights about COVID-19 cases and deaths across states in India. 
                    Explore data distributions and trends to understand the impact at a regional level.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Radio button for selecting state-wise visualizations
            india_option = st.radio(
                label="Select a Visualization to Explore:",
                options=[
                    "State-wise COVID-19 Data",
                    "COVID-19 Cases and Deaths in India"
                ],
                index=0,
                help="Choose between state-wise overall data or specific insights on cases and deaths."
            )
            st.markdown(f"""
                <div class="description" style="margin-top: 20px;">
                    <strong>Selected Visualization:</strong> 
                    <span style="color: #bb86fc;">{india_option}</span>
                </div>
                """, unsafe_allow_html=True)

            if india_option == "State-wise COVID-19 Data":
                st.markdown("""
                <div class="description">
                    <strong>State-wise COVID-19 Data:</strong> View detailed metrics for each state, including 
                    active cases, recoveries, and total deaths. This breakdown provides an overview of the pandemic's 
                    impact regionally.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for state-wise data visualization
                st.write("📊 [Bar Chart Placeholder: State-wise COVID-19 Data]")
                st.header("State-wise COVID-19 Data in India")
                st.write(statewise_data.style.background_gradient(cmap="CMRmap"))
                st.pyplot(plot_statewise_data(statewise_data))
            elif india_option == "COVID-19 Cases and Deaths in India":
                st.markdown("""
                <div class="description">
                    <strong>COVID-19 Cases and Deaths in India:</strong> Analyze total cases and deaths reported 
                    across the nation. This visualization helps identify trends and hotspots requiring attention.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for cases and deaths visualization
                st.write("📈 [Line Chart Placeholder: Cases and Deaths in India]")
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=False)
                df = df.sort_values(by='Date')
                daily_df = df.groupby('Date').agg({
                    'Confirmed': 'sum',
                    'Deaths': 'sum'
                }).reset_index()

                # Calculate daily cases and deaths
                daily_df['daily_cases'] = daily_df['Confirmed'].diff().fillna(daily_df['Confirmed'])
                daily_df['daily_deaths'] = daily_df['Deaths'].diff().fillna(daily_df['Deaths'])

                # Calculate cumulative cases and deaths
                daily_df['cumulative_cases'] = daily_df['Confirmed'].cumsum()
                daily_df['cumulative_deaths'] = daily_df['Deaths'].cumsum()

                # Plot Daily Cases and Deaths
                fig1, ax1 = plt.subplots(figsize=(12, 6))
                ax1.plot(daily_df['Date'], daily_df['daily_cases'], label='Daily Cases', color='blue')
                ax1.plot(daily_df['Date'], daily_df['daily_deaths'], label='Daily Deaths', color='red')
                ax1.set_title('Daily COVID-19 Cases and Deaths in India')

                st.pyplot(fig1)
        elif category == "Top States":
            st.markdown("""
            <div class="section">
                <h3 style="color: #bb86fc;">Top States Analysis</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Explore the states with the highest impact in terms of active cases, deaths, or overall trends. 
                    Identify regional hotspots and their progression over time.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Radio button for selecting top states visualizations
            india_option = st.radio(
                label="Select a Visualization to Explore:",
                options=[
                    "Top States by Active Cases",
                    "Top States by Deaths",
                    "COVID-19 Trends for Top 10 States"
                ],
                index=0,
                help="Choose a category to analyze the states most affected by COVID-19."
            )

            # Display the selected option dynamically
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Visualization:</strong> 
                <span style="color: #bb86fc;">{india_option}</span>
            </div>
            """, unsafe_allow_html=True)
            if india_option == "Top States by Active Cases":
                st.markdown("""
                <div class="description">
                    <strong>Top States by Active Cases:</strong> Visualize the states with the highest number 
                    of active COVID-19 cases. This chart provides a snapshot of ongoing pandemic severity.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for top active cases visualization
                st.write("📊 [Bar Chart Placeholder: Top States by Active Cases]")
                st.header("Top States by Active COVID-19 Cases")
                fig = plt.figure(figsize=(16,10))
                plt.title("Top 10 States with Most Active Cases in India", fontsize=22, fontweight='bold')

                # Assign `x` to `hue` and set `legend=False`
                ax = sns.barplot(
                    data=top10ActiveCases.iloc[:10], 
                    y='Active_cases', 
                    x='State/UnionTerritory', 
                    hue='State/UnionTerritory',    # Assign `x` to `hue`
                    palette='viridis', 
                    linewidth=2, 
                    edgecolor='black',
                    dodge=False                     # To keep bars in single row
                )

                # Add data labels above bars
                for p in ax.patches:
                    ax.annotate(format(p.get_height(), ','),
                                (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', 
                                va='center', 
                                xytext=(0, 10), 
                                textcoords='offset points',
                                fontsize=12,
                                fontweight='bold',
                                color='black')

                # Customize x and y labels
                plt.xlabel("States", fontsize=14, fontweight='bold')
                plt.ylabel("Total Active Cases", fontsize=14, fontweight='bold')

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45, ha='right', fontsize=12)
                plt.yticks(fontsize=12)

                # Add grid
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                st.pyplot(fig)
            

            elif india_option == "Top States by Deaths":
                st.markdown("""
                <div class="description">
                    <strong>Top States by Deaths:</strong> Analyze the states with the highest recorded COVID-19 deaths. 
                    This visualization highlights regions that have experienced the most significant impact.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for top deaths visualization
                st.write("📊 [Bar Chart Placeholder: Top States by Deaths]")
                st.header("Top States by Deaths")
                top10Deaths = (
                    covid_df.groupby('State/UnionTerritory')
                    .apply(lambda x: x.loc[x['Deaths'].idxmax()])  # Select row with max deaths per state
                    [['State/UnionTerritory', 'Deaths', 'Date']]
                    .sort_values(by='Deaths', ascending=False)
                    .reset_index(drop=True)
                    .head(10)  # Select only top 10 states
                )

                # Optional: Rename columns if desired
                top10Deaths.columns = ['State/UnionTerritory', 'Deaths', 'Date']
                fig = plt.figure(figsize=(14, 8))
                plt.title("Top 10 States with Most COVID-19 Deaths in India", fontsize=20, fontweight='bold')

                sns.barplot(
                    data=top10Deaths,
                    y="State/UnionTerritory",
                    x="Deaths",
                    hue='State/UnionTerritory',   
                    palette='Reds_r', 
                    edgecolor='black',                
                )

                # Add data labels for each bar
                for index, value in enumerate(top10Deaths['Deaths']):
                    plt.text(value, index, f"{value:,}", va="center", ha="left", fontweight='bold')

                plt.xlabel("Number of Deaths", fontsize=14)
                plt.ylabel("State/Union Territory", fontsize=14)
                plt.grid(axis='x', linestyle="--", alpha=0.7)

                st.pyplot(fig)
            elif india_option == "COVID-19 Trends for Top 10 States":
                st.markdown("""
                <div class="description">
                    <strong>COVID-19 Trends for Top 10 States:</strong> Examine the progression of cases, recoveries, 
                    and deaths in the 10 most impacted states. This trend chart helps in monitoring and comparing state-level progress.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for trends visualization
                st.write("📈 [Line Chart Placeholder: COVID-19 Trends for Top 10 States]")
                st.header("COVID-19 Trends for Top 10 States")
                # Filter the top 10 states
                top_states = top10ActiveCases['State/UnionTerritory'].values
                
                # Convert 'Date' column to datetime format if it's not already
                covid_df['Date'] = pd.to_datetime(covid_df['Date'])
                
                # Extract Month and Year from 'Date' and create a new column for Month-Year
                covid_df['Month_Year'] = covid_df['Date'].dt.to_period('M')
                
                # Prepare data for plotting: Group by Month-Year and State
                death_trends = covid_df[covid_df['State/UnionTerritory'].isin(top_states)] \
                                .groupby(['Month_Year', 'State/UnionTerritory'])['Deaths'] \
                                .sum().unstack()
                
                # Create a new figure and axis
                fig, ax = plt.subplots(figsize=(16, 8))
                
                # Plotting the trends
                sns.lineplot(data=death_trends.T, ax=ax)  # Use the transposed data
                ax.set_title('COVID-19 Death Trends for Top 10 States (Month-Year)', fontsize=20)
                ax.set_xlabel('Month-Year', fontsize=15)
                ax.set_ylabel('Total Deaths', fontsize=15)
                ax.legend(title='States', bbox_to_anchor=(1.05, 1), loc='upper left')
                
                # Rotate x-tick labels and adjust spacing to avoid overlap
                plt.xticks(rotation=45, ha='right', fontsize=12)
                plt.tight_layout()  # Adjust layout to prevent clipping of labels
                
                # Pass the figure to Streamlit
                st.pyplot(fig)
        elif category == "Trends":
            st.markdown("""
            <div class="section">
                <h3 style="color: #bb86fc;">COVID-19 Trends Analysis</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Discover the progression of COVID-19 cases over time through dynamic visualizations. 
                    Analyze trends to understand the pandemic's trajectory and its regional impact.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Radio button for selecting trends visualizations
            india_option = st.radio(
                label="Select a Trend Visualization:",
                options=[
                    "Covid19 Confirmed Cases Over Time",
                    "Total Covid19 Confirmed Cases HEATMAP Over Time", 
                    "Bar Race for Confirmed Cases Over Time"
                ],
                index=0,
                help="Choose a visualization to explore how COVID-19 cases evolved over time."
            )

            # Dynamic display of selected option
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Visualization:</strong> 
                <span style="color: #bb86fc;">{india_option}</span>
            </div>
            """, unsafe_allow_html=True)
            if india_option == "Covid19 Confirmed Cases Over Time":
                st.markdown("""
                <div class="description">
                    <strong>Confirmed Cases Over Time:</strong> Visualize the cumulative progression of confirmed COVID-19 cases 
                    across India. This line chart reveals key peaks and patterns in the spread of the virus.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for line chart visualization
                st.write("📈 [Line Chart Placeholder: Confirmed Cases Over Time]")
                daily_cases = df11.groupby('Date')['Total Confirmed cases'].sum()
                # Create the plot
                plt.figure(figsize=(12, 6))
                plt.plot(daily_cases, label='Total Confirmed Cases')
                plt.xlabel('Date')
                plt.ylabel('Confirmed Cases')
                plt.title('Total Confirmed COVID-19 Cases Over Time')
                plt.legend()

                # Display the plot in Streamlit
                st.pyplot(plt)
            elif india_option == "Total Covid19 Confirmed Cases HEATMAP Over Time":
                st.markdown("""
                <div class="description">
                    <strong>Heatmap of Confirmed Cases Over Time:</strong> Explore a geographical heatmap that highlights 
                    the distribution and intensity of confirmed cases over time, providing a spatial view of the pandemic's spread.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for heatmap visualization
                st.write("🌍 [Heatmap Placeholder: Confirmed Cases Over Time]")
                fig = px.scatter_geo(
                    df11,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name='Name of State / UT',
                    size='Total Confirmed cases',
                    color='Total Confirmed cases',
                    color_continuous_scale='Reds',
                    title='Total Confirmed COVID-19 Cases by State in India Over Time',
                    projection='natural earth',
                    animation_frame='Date',  # Directly use 'Date' column for animation
                    size_max=100  # Adjust bubble size for better visibility
                )

                # Set map scope to Asia and restrict to India's latitude and longitude range
                fig.update_geos(
                    scope='asia',
                    lataxis_range=[5, 37],   # Approximate latitude range for India
                    lonaxis_range=[67, 97],  # Approximate longitude range for India
                    showcountries=True,      # Show country borders
                    countrycolor="Black"     # Country border color
                )

                # Customize animation settings for smoother transitions
                fig.update_layout(
                    updatemenus=[{
                        'buttons': [
                            {
                                'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}],
                                'label': 'Play',
                                'method': 'animate'
                            },
                            {
                                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                                'label': 'Pause',
                                'method': 'animate'
                            }
                        ],
                        'direction': 'left',
                        'pad': {'r': 10, 't': 87},
                        'showactive': False,
                        'type': 'buttons',
                        'x': 0.1,
                        'xanchor': 'right',
                        'y': 0,
                        'yanchor': 'top'
                    }]
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig)
            elif india_option == "Bar Race for Confirmed Cases Over Time":
                st.markdown("""
                <div class="description">
                    <strong>Bar Race Visualization:</strong> Watch an animated bar chart race that dynamically ranks states 
                    based on their number of confirmed cases over time, offering an engaging and comparative perspective.
                </div>
                """, unsafe_allow_html=True)
                # Placeholder for bar race visualization
                st.write("📊 [Bar Race Placeholder: Confirmed Cases Over Time]")
                df = pd.read_csv("/Users/ayyalashriyatha/Desktop/confirmed_cases_india.csv")

                selected_states = ['Kerala', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 
                   'West Bengal', 'Delhi', 'Andhra Pradesh', 'Rajasthan', 'Bihar']

                # Assuming df is already loaded with the necessary data
                df_filtered = df[df['state'].isin(selected_states)]

                # Reshape the data from wide format to long format
                df_long = pd.melt(df_filtered, id_vars=['state'], var_name='date', value_name='cases')

                # Convert 'date' to datetime format
                df_long['date'] = pd.to_datetime(df_long['date'])

                # Sort dates to ensure chronological order
                dates = sorted(df_long['date'].unique())

                # Create frames for animation
                frames = []
                for date in dates:
                    df_date = df_long[df_long['date'] == date]
                    df_date = df_date.sort_values(by='cases', ascending=False)  # Sort by cases
                    max_cases = df_date['cases'].max()  # Maximum cases for dynamic scaling

                    # Highlight the top state dynamically
                    top_state = df_date.iloc[0]['state']
                    top_cases = df_date.iloc[0]['cases']

                    frames.append(go.Frame(
                        data=[go.Bar(
                            x=df_date['cases'],
                            y=df_date['state'],
                            orientation='h',
                            text=df_date['cases'],
                            hoverinfo='x+y+text',
                            marker=dict(color=df_date['cases'], colorscale='Cividis')  # Uniform color scale
                        )],
                        name=str(date.date()),  # Frame name for slider
                        layout=go.Layout(
                            xaxis=dict(range=[0, max_cases * 1.1]),  # Dynamically set x-axis range
                            annotations=[
                                dict(
                                    x=0.5, y=1.05, xref="paper", yref="paper",  # Place annotation within the paper coordinate system
                                    text=f"Leading State: {top_state} ({top_cases} cases)",
                                    showarrow=False,
                                    font=dict(size=16, color='darkblue'),
                                    align="center",
                                    bgcolor="white",  # Add a background to avoid overlap
                                    bordercolor="black",
                                    borderwidth=1,
                                ),
                                dict(
                                    x=0.5, y=-0.1, xref="paper", yref="paper",
                                    text=f"Date: {date.strftime('%Y-%m-%d')}",  # Dynamically update the date
                                    showarrow=False,
                                    font=dict(size=16, color='black'),
                                    align="center",
                                    bgcolor="white",  # Add a background to avoid overlap
                                    bordercolor="black",
                                    borderwidth=1,
                                )
                            ]
                        )
                    ))

                # Create the initial figure for the first frame
                initial_df = df_long[df_long['date'] == dates[0]].sort_values(by='cases', ascending=False)
                initial_max_cases = initial_df['cases'].max()  # Max cases for the first frame

                fig = go.Figure(
                    data=[go.Bar(
                        x=initial_df['cases'],
                        y=initial_df['state'],
                        orientation='h',
                        text=initial_df['cases'],
                        hoverinfo='x+y+text',
                        marker=dict(color=initial_df['cases'], colorscale='Cividis')
                    )],
                    layout=go.Layout(
                        title="COVID-19 Confirmed Cases by State",
                        xaxis=dict(title="Confirmed Cases", range=[0, initial_max_cases * 1.1]),
                        yaxis=dict(title="State", autorange='reversed'),  # Reversed to have the highest on top
                        showlegend=False,
                        height=600,
                        plot_bgcolor='lightgray',
                        margin=dict(t=50, b=80, l=50, r=50),
                        annotations=[
                            dict(
                                x=0.5, y=1.05, xref="paper", yref="paper",
                                text=f"Leading State: {initial_df.iloc[0]['state']} ({initial_df.iloc[0]['cases']} cases)",
                                showarrow=False,
                                font=dict(size=16, color='darkblue'),
                                align="center",
                                bgcolor="white",
                                bordercolor="black",
                                borderwidth=1,
                            ),
                            dict(
                                x=0.5, y=-0.1, xref="paper", yref="paper",
                                text=f"Date: {dates[0].strftime('%Y-%m-%d')}",  # Initially display the first date
                                showarrow=False,
                                font=dict(size=16, color='black'),
                                align="center",
                                bgcolor="white",  # Add a background to avoid overlap
                                bordercolor="black",
                                borderwidth=1,
                            )
                        ],
                        sliders=[{
                            'steps': [
                                {
                                    'args': [
                                        [str(date.date())],  # Select the frame corresponding to the date
                                        {
                                            'frame': {'duration': 1000, 'redraw': True},  # Slow frame duration (1000 ms)
                                            'mode': 'immediate'
                                        }
                                    ],
                                    'label': date.strftime('%Y-%m-%d'),
                                    'method': 'animate'
                                } for date in dates
                            ],
                            'transition': {'duration': 500},  # Smooth transition duration (500ms)
                            'x': 0.1,
                            'len': 0.9,
                            'currentvalue': {
                                'font': {'size': 16},
                                'prefix': 'Date: ',
                                'visible': True,
                                'xanchor': 'center'
                            },
                            'pad': {'b': 10, 't': 50}
                        }],
                        updatemenus=[{
                            'buttons': [
                                {
                                    'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}],  # Slower playback
                                    'label': 'Play',
                                    'method': 'animate'
                                },
                                {
                                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                                    'label': 'Pause',
                                    'method': 'animate'
                                }
                            ],
                            'direction': 'left',
                            'pad': {'r': 10, 't': 70},
                            'showactive': False,
                            'type': 'buttons',
                            'x': 0.1,
                            'xanchor': 'right',
                            'y': 0,
                            'yanchor': 'top',
                        }]
                    ),
                    frames=frames
                )

                # Display the plot using Streamlit
                st.plotly_chart(fig)

        elif category == "Comparisons":
            st.markdown("""
            <div class="section">
                <h3 style="color: #bb86fc;">COVID-19 State Comparisons</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Compare COVID-19 metrics between two states to identify trends, patterns, and disparities in case management.
                    This section enables a side-by-side analysis to uncover key insights.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Radio button for comparison visualizations
            india_option = st.radio(
                label="Select a Comparison Visualization:",
                options=[
                    "Covid19 Daily Cases Comparison Between Two States"
                ],
                index=0,
                help="Analyze the daily case trends for two states to observe similarities or differences."
            )

            # Dynamic display of the selected option
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Visualization:</strong> 
                <span style="color: #bb86fc;">{india_option}</span>
            </div>
            """, unsafe_allow_html=True)
            if india_option == "Covid19 Daily Cases Comparison Between Two States":
                st.markdown("""
                <div class="description">
                    <strong>Daily Cases Comparison:</strong> Compare the daily new COVID-19 cases between two states 
                    using an interactive line chart. This visualization highlights differences in outbreak trends and response measures.
                </div>
                """, unsafe_allow_html=True)

                # Dropdowns for state selection with Indian states
                state_options = [
                    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", 
                    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", 
                    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", 
                    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
                    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", 
                    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Lakshadweep", "Delhi", 
                    "Puducherry"
                ]
                
                state1 = st.selectbox(
                    "Select First State:",
                    options=state_options,  # List of actual Indian states
                    index=0
                )
                
                state2 = st.selectbox(
                    "Select Second State:",
                    options=state_options,  # List of actual Indian states
                    index=1
                )

                # Display user selections
                st.markdown(f"""
                <div class="description" style="margin-top: 20px;">
                    <strong>Selected States:</strong> 
                    <span style="color: #bb86fc;">{state1}</span> vs. <span style="color: #bb86fc;">{state2}</span>
                </div>
                """, unsafe_allow_html=True)

                # Placeholder for comparison line chart
                st.write("📊 [Line Chart Placeholder: Daily Cases Comparison]")
                
                # Call to function that compares the daily cases (Replace with your actual function)
                if state1 and state2:
                    compare_daily_cases_with_slider(state1, state2, df11)

        elif category == "Heat Maps":
            st.markdown("""
            <div class="section">
                <h3 style="color: #bb86fc;">COVID-19 Heat Maps</h3>
                <p style="color: #d1d5db; font-size: 1.1rem;">
                    Visualize COVID-19 data distribution across India using heat maps. These interactive visualizations 
                    highlight regional trends and case densities, providing a clear understanding of the pandemic's spread.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Radio button for heat map visualizations
            india_option = st.radio(
                label="Select a Heat Map Visualization:",
                options=[
                    "Geographical Heat Map of COVID-19 Confirmed Cases in India",
                    "Total Covid19 Confirmed Cases HEATMAP"
                ],
                index=0,
                help="Choose between a geographical heat map or a temporal heatmap of confirmed cases."
            )

            # Display user-selected option dynamically
            st.markdown(f"""
            <div class="description" style="margin-top: 20px;">
                <strong>Selected Visualization:</strong> 
                <span style="color: #bb86fc;">{india_option}</span>
            </div>
            """, unsafe_allow_html=True)

            if india_option == "Geographical Heat Map of COVID-19 Confirmed Cases in India":
                st.markdown("""
                <div class="description">
                    <strong>Geographical Heat Map:</strong> This map displays the distribution of confirmed COVID-19 cases across India's states and union territories.
                    It provides an overview of hotspots and regions with higher case counts.
                </div>
                """, unsafe_allow_html=True)

                # Placeholder for geographical heat map
                st.write("🗺️ [Geographical Heat Map Placeholder]")
                st.markdown("""
                <p style="color: #d1d5db; font-size: 1rem;">
                    Note: The heat map is generated using real-time data from reliable sources. Use the controls to zoom in for 
                    detailed regional insights.
                </p>
                """, unsafe_allow_html=True)
                cases_by_state = df.groupby('State/UnionTerritory').agg({
                    'Confirmed': 'sum',
                    'Cured': 'sum',
                    'Deaths': 'sum'
                }).reset_index()
                india_geo = gpd.read_file('/Users/ayyalashriyatha/Desktop/Indian_States.geojson')
                
                # Merge the geographical data with the cases data
                merged = india_geo.set_index('NAME_1').join(
                    cases_by_state.set_index('State/UnionTerritory'),
                    how='left'  # Ensure all geographic data shows, even with missing cases data
                )

                # Fill NaN values with 0 for better visualization
                merged = merged.fillna(0)

                # Create the plot
                fig, ax = plt.subplots(1, 1, figsize=(15, 10))
                merged.plot(
                    column='Confirmed',
                    ax=ax,
                    legend=True,
                    legend_kwds={'label': "Number of Confirmed Cases", 'orientation': "horizontal"},
                    cmap='OrRd'  # Colormap for heat intensity
                )
                ax.set_title('Geographical Heat Map of COVID-19 Confirmed Cases in India')
                ax.set_axis_off()

                # Show the figure in Streamlit
                st.pyplot(fig)
            elif india_option == "Total Covid19 Confirmed Cases HEATMAP":
                st.markdown("""
                <div class="description">
                    <strong>Temporal Heat Map:</strong> This heat map represents the progression of confirmed COVID-19 cases over time. 
                    It helps identify trends, spikes, and regional variations in case counts.
                </div>
                """, unsafe_allow_html=True)

                # Placeholder for temporal heat map
                st.write("📊 [Temporal Heat Map Placeholder]")
                st.markdown("""
                <p style="color: #d1d5db; font-size: 1rem;">
                    Note: The temporal heat map uses a color gradient to represent case density, with darker colors indicating higher counts.
                </p>
                """, unsafe_allow_html=True)
                latest_data = df11.sort_values('Date').groupby('Name of State / UT').last().reset_index()

                # Ensure the hover data includes state names explicitly
                fig = px.scatter_geo(
                    latest_data,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total Confirmed cases',
                    color='Total Confirmed cases',
                    color_continuous_scale='Viridis',
                    title='Total Confirmed COVID-19 Cases by State in India (Latest Data)',
                    projection='natural earth',
                    size_max=100,
                    template='plotly_dark',
                    hover_data={
                        'Name of State / UT': True,  # Ensures state name is shown
                        'Total Confirmed cases': True,  # Explicitly include Total Confirmed Cases in hover
                        'Latitude': False,  # Optionally exclude Latitude from hover
                        'Longitude': False  # Optionally exclude Longitude from hover
                    }
                )

                # Update hover template for additional customization
                fig.update_traces(
                    hovertemplate="<b>%{customdata[0]}</b><br>Total Confirmed Cases: %{marker.size}<extra></extra>"
                )

                # Set map scope and restrict to India's region
                fig.update_geos(
                    scope='asia',
                    lataxis_range=[5, 37],
                    lonaxis_range=[67, 97],
                    showcountries=True,
                    countrycolor="Black",
                    showland=True,
                    landcolor="rgb(250, 250, 250)"
                )

                # Layout adjustments
                fig.update_layout(
                    geo=dict(showcoastlines=True, coastlinecolor="Black"),
                    title_font=dict(size=20, color='white', family='Arial'),
                    margin={"r":0, "t":40, "l":0, "b":0}
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig)
    
if __name__ == "__main__":
    main()
