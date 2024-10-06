import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import os
import plotly.express as px



DATABASE_URL = os.getenv('DATABASE_URL')

# Create the engine using the DATABASE_URL
engine = create_engine(DATABASE_URL)

# Load data from the PostgreSQL database
def load_data():
    query = "SELECT * FROM public.repositories;"
    df = pd.read_sql(query, engine)
    
    df.index = df.index + 1 
    df.index.name = 'ID'  

    return df

# Function to display image and description for the selected topic
def img_desc(selected_topic):
    # Folder where images are stored
    

    # Dictionary to map topics to descriptions
    topic_descriptions = {
    "machine learning": "Machine learning is the study of computer algorithms that improve automatically through experience. It enables systems to learn from data patterns and make predictions or decisions without explicit programming. Applications range from recommendation systems to image recognition.",
    
    "data visualization": "Data visualization is the graphical representation of information and data, allowing complex data sets to be communicated clearly and efficiently. By using visual elements like charts and maps, it helps users understand trends, outliers, and patterns in data. Effective visualizations enhance decision-making and storytelling.",
    
    "deep learning": "Deep learning is a subset of machine learning involving neural networks with three or more layers, which simulate the way the human brain operates. It excels in processing unstructured data such as images, sound, and text, driving advancements in fields like natural language processing and computer vision.",
    
    "natural language processing": "Natural Language Processing (NLP) is the branch of AI that enables computers to understand, interpret, and generate human language. It encompasses a range of tasks, from sentiment analysis and language translation to chatbots and voice recognition. NLP aims to bridge the gap between human communication and computer understanding.",
    
    "data engineering": "Data engineering focuses on the practical application of data collection, storage, and transformation processes to prepare data for analytical and operational purposes. It involves building data pipelines, designing database systems, and ensuring data quality and integrity, enabling data scientists and analysts to access reliable data for analysis.",
    
    "data science": "Data science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines expertise from statistics, computer science, and domain knowledge, playing a critical role in decision-making across various industries.",
    
    "python": "Python is a versatile and powerful programming language widely used in various domains, particularly in data science, web development, and automation. Known for its readability and simplicity, Python boasts a rich ecosystem of libraries and frameworks, such as Pandas and NumPy, making it a favorite among data professionals.",
    
    "sql": "SQL (Structured Query Language) is a domain-specific language used in programming and managing relational databases. It enables users to create, read, update, and delete data efficiently, allowing for complex queries and data manipulation. SQL is essential for data analysis and database management.",
    
    "cloud computing": "Cloud computing refers to the delivery of computing services over the internet, including storage, processing, and networking. It allows organizations to access and manage their data and applications remotely, providing scalability, flexibility, and cost-effectiveness. Cloud services can be categorized into public, private, and hybrid clouds.",
    
    "big data": "Big data refers to extremely large datasets that may be analyzed computationally to reveal patterns, trends, and associations. These datasets can be structured, semi-structured, or unstructured, requiring specialized tools and techniques for processing. Big data analytics helps organizations gain insights that drive strategic decision-making."
        }


    image_path = f'Images/{selected_topic.lower()}.jpg'

    try:
        selected_image = Image.open(image_path)  # Load the image
        st.image(selected_image, caption=selected_topic.title(), use_column_width=True)  # Display the image
    except FileNotFoundError:
        st.write(f"Image for {selected_topic.title()} not found.")
        
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
    filtered_by_topic = data[data['Topic'] == selected_topic] if selected_topic else data
    languages = ['Default'] + list(filtered_by_topic['Programming_Language'].unique())
    
    selected_language = st.sidebar.selectbox("Select Programming Language", languages)

    # Filter by creation and last updated date
    creation_dates = ['Default'] + sorted(list(pd.to_datetime(filtered_by_topic['Creation_Date']).dt.year.unique()))
    selected_creation_date = st.sidebar.selectbox("Select Creation Year", creation_dates)

    last_updated_dates = ['Default'] + sorted(list(pd.to_datetime(filtered_by_topic['Last_Updated_Date']).dt.year.unique()),reverse=True)
    selected_last_updated_date = st.sidebar.selectbox("Select Last Updated Year", last_updated_dates)

    # Apply filters
    filtered_data = filtered_by_topic.copy()
    
    if selected_language != 'Default':
        filtered_data = filtered_data[filtered_data['Programming_Language'] == selected_language]

    if selected_creation_date != 'Default':
        filtered_data = filtered_data[pd.to_datetime(filtered_data['Creation_Date']).dt.year == int(selected_creation_date)]

    if selected_last_updated_date != 'Default':
        filtered_data = filtered_data[pd.to_datetime(filtered_data['Last_Updated_Date']).dt.year == int(selected_last_updated_date)]

   # Activity level filter
    if not filtered_data.empty:
        min_stars, max_stars = filtered_data['Number_of_Stars'].min(), filtered_data['Number_of_Stars'].max()
        unique_stars = filtered_data['Number_of_Stars'].unique()

        if len(unique_stars) > 1:
            activity_level = st.sidebar.slider("Select Minimum Number of Stars", min_stars, max_stars, min_stars, int((min_stars + max_stars) / 10))
            filtered_data = filtered_data[filtered_data['Number_of_Stars'] >= activity_level]
        else:
            st.sidebar.write("Only one unique star count available. Using that value for filtering.")
            filtered_data = filtered_data[filtered_data['Number_of_Stars'] == unique_stars[0]]
    else:
        st.sidebar.write("No data available to filter.")

    return selected_topic, selected_creation_date, filtered_data

def Topic_Visuals(selected_topic, selected_creation_date, filtered_data):
    st.markdown(f"<h2 style='text-align: LEFT;'>Filtered Repositories under Topic: {selected_topic.upper()}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: LEFT;'>Total Repositories Found: {len(filtered_data)}</h3>", unsafe_allow_html=True)

    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.write("No repositories found with the selected filters.")

    # Visualizations
    st.subheader("Visual Insights over Repository")
    
    # Pie chart: Distribution of repositories by programming language
    if 'Programming_Language' in filtered_data.columns:
        lang_data = filtered_data.groupby('Programming_Language').size().reset_index(name='Repository_Count')
        fig = px.pie(lang_data, names='Programming_Language', values='Repository_Count', title='Repositories by Programming Language')
        st.plotly_chart(fig)

    # Line chart: Number of repositories created per year
    if 'Creation_Date' in filtered_data.columns:
        filtered_data['Creation_Year'] = pd.to_datetime(filtered_data['Creation_Date']).dt.year
        if selected_creation_date == 'Default':
            year_data = filtered_data.groupby('Creation_Year').size().reset_index(name='Repository_Count')
            fig = px.line(year_data, x='Creation_Year', y='Repository_Count', title='Repository Creation Trend (Yearly)')
            st.plotly_chart(fig)
        else:
            month_data = filtered_data[filtered_data['Creation_Year'] == int(selected_creation_date)].groupby(pd.to_datetime(filtered_data['Creation_Date']).dt.month).size().reset_index(name='Repository_Count')
            fig = px.line(month_data, x='Creation_Date', y='Repository_Count', title=f'Repository Creation Trend for {selected_creation_date} (Monthly)')
            st.plotly_chart(fig)

    # Bar charts
    if 'Number_of_Stars' in filtered_data.columns:
        fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Stars', title='Number of Stars per Repository', text='Number_of_Stars')
        fig.update_traces(textposition='outside', marker_color='blue')
        st.plotly_chart(fig)

    if 'Number_of_Forks' in filtered_data.columns:
        fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Forks', title='Number of Forks per Repository')
        st.plotly_chart(fig)

    if 'Number_of_Open_Issues' in filtered_data.columns:
        fig = px.bar(filtered_data, x='Repository_Name', y='Number_of_Open_Issues', title='Number of Open Issues per Repository')
        st.plotly_chart(fig)

    # Pie chart: Distribution of repositories by license type
    if 'License_Type' in filtered_data.columns:
        license_data = filtered_data.groupby('License_Type').size().reset_index(name='Repository_Count')
        fig = px.pie(license_data, names='License_Type', values='Repository_Count', title='Repositories by License Type')
        st.plotly_chart(fig)

    # Bar chart: Comparison of stars and forks
    if 'Number_of_Stars' in filtered_data.columns and 'Number_of_Forks' in filtered_data.columns:
        comparison_data = filtered_data[['Repository_Name', 'Number_of_Stars', 'Number_of_Forks']].melt(id_vars='Repository_Name', value_vars=['Number_of_Stars', 'Number_of_Forks'], var_name='Metric', value_name='Count')
        fig = px.bar(comparison_data, x='Repository_Name', y='Count', color='Metric', barmode='group', title='Comparison of Stars and Forks per Repository')
        st.plotly_chart(fig)

    st.markdown(f"<h2 style='text-align: LEFT;'>Filtered Repositories under Topic: {selected_topic.upper()}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: LEFT;'>Total Repositories Found: {len(filtered_data)}</h3>", unsafe_allow_html=True)

    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.write("No repositories found with the selected filters.")


def repo_visuals(filtered_data):
    st.markdown(f"<h2 style='text-align: center;'>Selected  Repository </h2>", unsafe_allow_html=True)
    repo_index = st.sidebar.number_input("Select Repository ID", min_value=1, max_value=len(filtered_data), step=1)

    if not filtered_data.empty:
        selected_repo = filtered_data.iloc[repo_index-1]
        
        st.markdown(f"""
            <div style='background-color: #f4f4f4; padding: 20px; border-radius: 10px;'>
                <h2 style='color: #2E86C1; text-align: center;'>{selected_repo['Repository_Name']}</h2>
                <p style='text-align: center; font-size: 16px; color: #566573;'>⭐ {selected_repo['Number_of_Stars']} | 🍴 {selected_repo['Number_of_Forks']} | 🐛 {selected_repo['Number_of_Open_Issues']}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>Owner: {selected_repo['Owner']}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>Description: {selected_repo['Description']}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>Language: {selected_repo['Programming_Language']}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>Created On: {pd.to_datetime(selected_repo['Creation_Date']).strftime('%B %d, %Y')}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>Last Updated: {pd.to_datetime(selected_repo['Last_Updated_Date']).strftime('%B %d, %Y')}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'>License: {selected_repo['License_Type']}</p>
                <p style='text-align: center; font-size: 14px; color: #7D3C98;'><a href="{selected_repo['URL']}" style="color: #E74C3C;">View Repository</a></p>
            </div>
        """, unsafe_allow_html=True)

# Main App
st.title("GitHub Repository Explorer")

# Load Data
df = load_data()

# Filter Repositories
selected_topic, selected_creation_date, filtered_data = filters(df)

# Topic Visuals
Topic_Visuals(selected_topic, selected_creation_date, filtered_data)

# Display selected repository information
repo_visuals(df)
