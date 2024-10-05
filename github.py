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

    return selected_topic,filtered_data


# Main Streamlit app function
def run_app():
    # Streamlit app title
    st.title("GitHub Repositories Explorer")

    # Load the dataset
    data = load_data()

    selected_topic,filtered_data=filters(data)

   

   
    st.write(f"Filtered Repositories under Topic:", selected_topic.upper() )
    st.write(f"Total Repositories Found: {len(filtered_data)}")


    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.write("No repositories found with the selected filters.")

    # Visualizations
    st.subheader("Visual Insights")

    # Plotting a bar chart of the number of stars by repository
    if not filtered_data.empty:
        st.bar_chart(filtered_data.set_index('Repository_Name')['Number_of_Stars'])

    
    

# Run the app
if __name__ == "__main__":
    run_app()
