# GitHub Repositories Explorer

This project is a **Streamlit** application for exploring GitHub repositories stored in a PostgreSQL database. It allows users to filter repositories by **topics**, **programming languages**, **creation and update dates**, and **activity level** (based on the number of stars). Additionally, it provides rich visual insights into the repositories and detailed information about individual repositories. 

The project includes the following key features:
- Interactive filtering and searching of repositories by various criteria.
- Dynamic visualizations such as bar charts, pie charts, and line charts based on repository data.
- Display of repository details including owner, programming language, description, license, and more.
- Auto-incrementing **id** column for repository records in the database.
- Seamless integration with a **PostgreSQL** database to load and store repository data.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [License](#license)

## Features

1. **Filter GitHub Repositories**:
   - Filter by **topic** (e.g., Machine Learning, Data Science).
   - Filter by **programming language** (Python, JavaScript, etc.).
   - Filter by **creation date** and **last updated date**.
   - Filter by **activity level** (based on the number of stars).
  
2. **Repository Visualizations**:
   - **Pie charts** showing distribution by programming languages and license types.
   - **Bar charts** showing stars, forks, and open issues per repository.
   - **Line charts** showing repository creation trends over time.

3. **Detailed Repository Information**:
   - View detailed repository information such as owner, description, stars, forks, open issues, creation date, last updated date, and license type.

4. **Database Integration**:
   - The application uses a **PostgreSQL** database to store and load GitHub repository data.
   - The `id` column is set as an **auto-incrementing primary key** in the database.
   - Data can be appended or replaced in the database.

## Technologies

- **Python**: Core programming language for backend and data manipulation.
- **Streamlit**: Web framework for building interactive user interfaces.
- **PostgreSQL**: Database for storing and querying repository data.
- **SQLAlchemy**: ORM (Object Relational Mapping) for connecting to the PostgreSQL database.
- **Pandas**: Library for data manipulation and analysis.
- **Plotly**: Library for creating interactive charts and visualizations.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/github-repositories-explorer.git
    cd github-repositories-explorer
    ```

2. **Install the required Python libraries**:
    Use the `requirements.txt` file to install the dependencies.
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up PostgreSQL Database**:
   - Install **PostgreSQL** on your local machine (if not already installed).
   - Create a PostgreSQL database:
     ```sql
     CREATE DATABASE github_data;
     ```
   - Update the connection string in the `app.py` or your Python code with your PostgreSQL credentials:
     ```python
     engine = create_engine('postgresql+psycopg2://<username>:<password>@localhost:5432/github_data')
     ```

4. **Run the Streamlit app**:
    To launch the application locally, use the following command:
    ```bash
    streamlit run app.py
    ```

5. **Access the app**:
   - After running the app, open your browser and navigate to `http://localhost:8501/` to interact with the GitHub Repositories Explorer.

## Database Schema

The **repositories** table in the PostgreSQL database contains the following columns:

| Column Name            | Data Type   | Description                                                     |
|------------------------|-------------|-----------------------------------------------------------------|
| `id`                   | INT         | Primary Key (Auto-incremented)                                  |
| `Repository_Name`       | TEXT        | The name of the GitHub repository                               |
| `Owner`                | TEXT        | The owner of the GitHub repository                              |
| `Description`          | TEXT        | A brief description of the repository                           |
| `Programming_Language` | TEXT        | The primary programming language used in the repository          |
| `Creation_Date`         | DATE        | The date when the repository was created (Date only, no time)   |
| `Last_Updated_Date`     | DATE        | The date when the repository was last updated                   |
| `Number_of_Stars`       | INT         | The number of stars the repository has received                 |
| `Number_of_Forks`       | INT         | The number of forks for the repository                          |
| `Number_of_Open_Issues` | INT         | The number of open issues in the repository                     |
| `License_Type`          | TEXT        | The license type of the repository (e.g., MIT, Apache)          |

### Example Schema:

```sql
CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    Repository_Name TEXT,
    Owner TEXT,
    Description TEXT,
    Programming_Language TEXT,
    Creation_Date DATE,
    Last_Updated_Date DATE,
    Number_of_Stars INT,
    Number_of_Forks INT,
    Number_of_Open_Issues INT,
    License_Type TEXT
);
```


## Usage

The application allows users to explore GitHub repository data with the following steps:

1. **Filtering**: Use the sidebar to filter repositories based on:
   - **Topic**: Choose from topics such as machine learning, data science, cloud computing, etc.
   - **Programming Language**: Filter repositories by programming languages like Python, JavaScript, etc.
   - **Creation Year**: Filter repositories based on the year they were created.
   - **Last Updated Year**: Filter repositories based on the year they were last updated.
   - **Activity Level**: Filter repositories by the number of stars they have received, reflecting their popularity.

2. **Visual Insights**: View various interactive visualizations such as:
   - Distribution of repositories by **programming language** and **license type**.
   - Trends in repository creation over time.
   - Number of stars, forks, and open issues per repository.

3. **Repository Details**: Select individual repositories from the list to view detailed information, including:
   - Repository **owner** and **description**.
   - The number of **stars**, **forks**, and **open issues**.
   - **Creation date**, **last updated date**, and the **license type** of the repository.

## Visualizations

The application provides several types of visualizations:

- **Pie Chart**:
  - Distribution of repositories by **programming language**.
  - Distribution by **license type**.

- **Bar Charts**:
  - Number of stars, forks, and open issues per repository.
  - Comparison of stars and forks.

- **Line Chart**:
  - Yearly and monthly trends in repository creation.
