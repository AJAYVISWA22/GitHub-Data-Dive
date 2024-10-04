import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# Create the PostgreSQL engine
engine = create_engine('postgresql+psycopg2://postgres:Ajay@localhost:5432/github_data')

# Load data from the PostgreSQL database

def load_data():
    query = "SELECT * FROM public.repositories;"
    df = pd.read_sql(query, engine)
    return df

# Load the dataset
data = load_data()

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


def streamlit():

# Streamlit app title
    st.title("GitHub Repositories Explorer")

    # Filter by topic
    topics = data['Topic'].unique()
    selected_topic = st.sidebar.selectbox("Select Topic", topics)

    # Display image and description for the selected topic
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

    # Filter by programming language
    languages = data['Programming_Language'].unique()
    selected_language = st.sidebar.selectbox("Select Programming Language", languages)


    # Filter by activity level (based on number of stars, forks, or issues)
    activity_level = st.sidebar.slider("Select Minimum Number of Stars", 0, int(data['Number_of_Stars'].max()), 0)

    # Apply filters
    filtered_data = data[(data['Topic'] == selected_topic) & 
                        (data['Programming_Language'] == selected_language) & 
                        (data['Number_of_Stars'] >= activity_level)]

    # Display the filtered data
    st.subheader("Filtered Repositories")
    st.dataframe(filtered_data)

    # Visualizations
    st.subheader("Visual Insights")

    # Plotting a bar chart of the number of stars by repository
    if not filtered_data.empty:
        st.bar_chart(filtered_data.set_index('Repository_Name')['Number_of_Stars'])

    # Show additional metrics
    st.subheader("Additional Metrics")
    st.write(f"Total Repositories Found: {len(filtered_data)}")




streamlit()