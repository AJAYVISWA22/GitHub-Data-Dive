import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px

# Create the PostgreSQL engine
engine = create_engine('postgresql+psycopg2://postgres:Ajay@localhost:5432/github_data')

# Load data from the PostgreSQL database
def load_data():
    query = "SELECT * FROM public.repositories;"
    df = pd.read_sql(query, engine)
    return df

# Function to display image and description for the selected topic
def img_desc(selected_topic):
    # Folder where images are stored
    image_folder = 'Images'

    # Dictionary to map topics to descriptions
    topic_descriptions = {
        "machine learning": "Machine learning is the study of computer algorithms that improve automatically through experience.",
        "data visualization": "Data visualization is the graphical representation of information and data.",
        "deep learning": "Deep learning is a subset of machine learning involving neural networks with three or more layers.",
        "natural language processing": "NLP is the branch of AI that helps computers understand, interpret, and manipulate human language.",
        "data engineering": "Data engineering focuses on the practical application of data collection and data pipelining.",
        "data science": "Data science is an interdisciplinary field that uses scientific methods, processes, and systems to extract knowledge from data.",
        "python": "Python is a versatile and powerful programming language widely used in various domains, especially data science and AI.",
        "sql": "SQL is a domain-specific language used in programming and managing relational databases.",
        "cloud computing": "Cloud computing is the delivery of computing services over the internet, including storage, processing, and networking.",
        "big data": "Big data refers to extremely large datasets that may be analyzed computationally to reveal patterns, trends, and associations."
    }

    image_path = os.path.join(image_folder, f'{selected_topic.lower()}.jpg')
    if os.path.exists(image_path):
        st.image(image_path, caption=selected_topic.title(), use_column_width=True)
        
    # Display description
    description = topic_descriptions.get(selected_topic.lower(), "No description available for this topic.")
    st.write(description)


def filters(data):
    # Filter by topic
    topics = data['Topic'].unique()
    selected_topic = st.sidebar.selectbox("Select Topic", topics)

    # Display image and description for the selected topic
    img_desc(selected_topic)



    # Filter programming languages dynamically based on the selected topic
    if selected_topic:
        filtered_by_topic = data[data['Topic'] == selected_topic]
        languages = ['Default'] + list(filtered_by_topic['Programming_Language'].unique())
    else:
        filtered_by_topic = data
        languages = ['Default'] + list(data['Programming_Language'].unique())

    selected_language = st.sidebar.selectbox("Select Programming Language", languages)



    # Filter by creation date dynamically based on the selected topic
    if selected_topic:
        creation_dates = ['Default'] + list(pd.to_datetime(filtered_by_topic['Creation_Date']).dt.year.unique())
    else:
        creation_dates = ['Default'] + list(pd.to_datetime(data['Creation_Date']).dt.year.unique())

    selected_creation_date = st.sidebar.selectbox("Select Creation Year", creation_dates)

    # Filter by last updated date dynamically based on the selected topic
    if selected_topic:
        last_updated_dates = ['Default'] + list(pd.to_datetime(filtered_by_topic['Last_Updated_Date']).dt.year.unique())
    else:
        last_updated_dates = ['Default'] + list(pd.to_datetime(data['Last_Updated_Date']).dt.year.unique())

    selected_last_updated_date = st.sidebar.selectbox("Select Last Updated Year", last_updated_dates)

    
    

    # Apply filters: filter only if a non-default option is selected
    filtered_data = filtered_by_topic.copy()

    if selected_language != 'Default':
        filtered_data = filtered_data[filtered_data['Programming_Language'] == selected_language]

    if selected_creation_date != 'Default':
        filtered_data = filtered_data[pd.to_datetime(filtered_data['Creation_Date']).dt.year == int(selected_creation_date)]

    if selected_last_updated_date != 'Default':
        filtered_data = filtered_data[pd.to_datetime(filtered_data['Last_Updated_Date']).dt.year == int(selected_last_updated_date)]
     
    # Filter by activity level (based on number of stars) dynamically based on the selected topic
    if selected_topic and selected_language:
        min_stars = int(filtered_data['Number_of_Stars'].min())
        max_stars = int(filtered_data['Number_of_Stars'].max())
    else:
        min_stars = int(data['Number_of_Stars'].min())
        max_stars = int(data['Number_of_Stars'].max())

    if min_stars==max_stars:
        activity_level=st.sidebar.write("X",min_stars)
    else:
        activity_level = st.sidebar.slider("Select Minimum Number of Stars", min_stars, max_stars, min_stars, int((min_stars+ max_stars) / 10))


    filtered_data = filtered_data[filtered_data['Number_of_Stars'] >= activity_level]

    return selected_topic,selected_creation_date,filtered_data

def Topic_Visuals(selected_topic,selected_creation_date,filtered_data):

        
        st.markdown(f"<h2 style='text-align: LEFT;'>Filtered Repositories under Topic: {selected_topic.upper()}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: LEFT;'>Total Repositories Found: {len(filtered_data)}</h3>", unsafe_allow_html=True)


        if not filtered_data.empty:
            st.dataframe(filtered_data)
        else:
            st.write("No repositories found with the selected filters.")

        # Visualizations
        st.subheader("Visual Insights over Repository")

    

        # Pie chart: Distribution of repositories by programming language
        if not filtered_data.empty and 'Programming_Language' in filtered_data.columns:
            st.subheader(" Distribution by Programming Language")

            # Group by Programming_Language to get the count of repositories for each language
            lang_data = filtered_data.groupby('Programming_Language').size().reset_index(name='Repository_Count')

            # Create pie chart
            fig = px.pie(lang_data, names='Programming_Language', values='Repository_Count', 
                        title='Repositories by Programming Language', 
                        labels={'Repository_Count': 'Repository Count'})

            # Display the pie chart
            st.plotly_chart(fig)


        # Line chart: Number of repositories created per year
        if not filtered_data.empty and 'Creation_Date' in filtered_data.columns:
            
            if selected_creation_date == 'Default':
                # Default behavior: Show repository counts by year
                st.subheader(" Repositories Created Over Time (Yearly)")
                filtered_data['Creation_Year'] = pd.to_datetime(filtered_data['Creation_Date']).dt.year
                year_data = filtered_data.groupby('Creation_Year').size().reset_index(name='Repository_Count')
                fig = px.line(year_data, x='Creation_Year', y='Repository_Count', title='Repository Creation Trend (Yearly)')
                st.plotly_chart(fig)

            else:
                # If a specific year is selected: Show repository counts by month for that year
                st.subheader(f" Repositories Created in {selected_creation_date} (Monthly)")
                filtered_data['Creation_Month'] = pd.to_datetime(filtered_data['Creation_Date']).dt.month
                month_data = filtered_data.groupby('Creation_Month').size().reset_index(name='Repository_Count')
                fig = px.line(month_data, x='Creation_Month', y='Repository_Count', title=f'Repository Creation Trend for {selected_creation_date} (Monthly)')
                st.plotly_chart(fig)


        # Plotting a bar chart of the number of stars by repository
        if not filtered_data.empty and 'Number_of_Stars' in filtered_data.columns:
            st.subheader("Number of Stars by Repository")
            
            # Create the bar chart using Plotly
            fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Stars', 
                        title='Number of Stars per Repository',
                        labels={'Repository_Name': 'Repository', 'Number_of_Stars': 'Stars'},
                        text='Number_of_Stars')  # Display the number of stars on the bars
            
            # Customize the chart appearance
            fig.update_traces(textposition='outside', marker_color='blue')
            fig.update_layout(xaxis_title="Repository", yaxis_title="Number of Stars")
            
            # Display the chart in Streamlit
            st.plotly_chart(fig)


        # Bar chart: Number of forks per repository
        if not filtered_data.empty and 'Number_of_Forks' in filtered_data.columns:
            st.subheader(" Number of Forks per Repository")
            fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Forks', 
                        title='Number of Forks per Repository', 
                        labels={'Repository_Name': 'Repository', 'Number_of_Forks': 'Forks'})
            st.plotly_chart(fig)

        # Bar chart: Number of open issues per repository
        if not filtered_data.empty and 'Number_of_Open_Issues' in filtered_data.columns:
            st.subheader(" Number of Open Issues per Repository")
            fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Open_Issues', 
                        title='Number of Open Issues per Repository', 
                        labels={'Repository_Name': 'Repository', 'Number_of_Open_Issues': 'Open Issues'})
            st.plotly_chart(fig)


        # Pie chart: Distribution of repositories by license type
        if not filtered_data.empty and 'License_Type' in filtered_data.columns:
            st.subheader(" Distribution by License Type")

            # Group by License_Type to get the count of repositories for each license
            license_data = filtered_data.groupby('License_Type').size().reset_index(name='Repository_Count')

            # Create pie chart
            fig = px.pie(license_data, names='License_Type', values='Repository_Count', 
                        title='Repositories by License Type', 
                        labels={'Repository_Count': 'Repository Count'})

            # Display the pie chart
            st.plotly_chart(fig)

        
            # Bar chart: Comparison of stars and forks
        if not filtered_data.empty and 'Number_of_Stars' in filtered_data.columns and 'Number_of_Forks' in filtered_data.columns:
            st.subheader(" Comparison of Stars and Forks")
            
            # Create a new DataFrame for stars and forks comparison
            comparison_data = filtered_data[['Repository_Name', 'Number_of_Stars', 'Number_of_Forks']].melt(id_vars='Repository_Name', 
                                                                                                        value_vars=['Number_of_Stars', 'Number_of_Forks'],
                                                                                                        var_name='Metric', value_name='Count')

            fig = px.bar(comparison_data, x='Repository_Name', y='Count', color='Metric', barmode='group',
                        title='Comparison of Stars and Forks per Repository')
            st.plotly_chart(fig)

        if not filtered_data.empty:
            st.dataframe(filtered_data)
        else:
            st.write("No repositories found with the selected filters.")

def repo_visuals(filtered_data):
      # Allow user to select a repository index
    repo_index = st.sidebar.number_input("Select Repository Index", min_value=0, max_value=len(filtered_data)-1, step=1)

    # Display details of the selected repository
    if not filtered_data.empty:
        selected_repo = filtered_data.iloc[repo_index]
        st.subheader(f"Details of Repository: {selected_repo['Repository_Name']}")
        st.write(f"**Owner:** {selected_repo['Owner']}")
        st.write(f"**Description:** {selected_repo['Description']}")
        st.write(f"**Programming Language:** {selected_repo['Programming_Language']}")
        st.write(f"**Stars:** {selected_repo['Number_of_Stars']}")
        st.write(f"**Forks:** {selected_repo['Number_of_Forks']}")
        st.write(f"**Open Issues:** {selected_repo['Number_of_Open_Issues']}")
        st.write(f"**License Type:** {selected_repo['License_Type']}")
        st.write(f"**Creation Date:** {selected_repo['Creation_Date']}")
        st.write(f"**Last Updated Date:** {selected_repo['Last_Updated_Date']}")






# Main Streamlit app function
def run_app():
    # Streamlit app title
    st.title("GitHub Repositories Explorer")

    # Load the dataset
    data = load_data()

    selected_topic,selected_creation_date,filtered_data=filters(data)

    Topic_Visuals(selected_topic,selected_creation_date,filtered_data)
    repo_visuals(data)


# Run the app
if __name__ == "__main__":
    run_app()
