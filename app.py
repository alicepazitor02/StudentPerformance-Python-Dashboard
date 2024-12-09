import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import zipfile
from io import BytesIO

# Function to load and clean the dataset based on the selected course
def load_data(course_type='mat'):
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip"
    r = requests.get(url)
    with zipfile.ZipFile(BytesIO(r.content)) as z:
        # Select the appropriate course data file
        csv_file = 'student-mat.csv' if course_type == 'mat' else 'student-por.csv'
        with z.open(csv_file) as f:
            df = pd.read_csv(f, sep=";")
    
    # Data Cleaning
    df = df.dropna()  # Remove rows with missing values
    df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Ensure 'age' is numeric
    df = df[df['G3'] <= 20]  # Filter grades above 20
    df = df[df['G3'] >= 0]  # Filter grades below 0
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')  # Standardize column names
    
    return df

# Visualization Functions
def create_grade_histogram(df):
    fig = px.histogram(df, x='g3', title="Distribution of Final Grades")
    return fig

def create_grade_boxplot(df):
    fig = px.box(df, x='sex', y='g3', title="Final Grade Distribution by Gender")
    return fig

def create_famsup_pie_chart(df):
    fig = px.pie(df, names='famsup', title="Family Support Proportions")
    return fig

def create_age_grade_scatter(df):
    fig = px.scatter(df, x='age', y='g3', color='sex', title="Age vs Final Grade")
    return fig

def create_grade_by_absences(df):
    fig = px.scatter(df, x='absences', y='g3', title="Final Grade vs Absences")
    return fig

# Streamlit Dashboard
def main():
    st.title("Interactive Student Performance Dashboard")

    # Choose the course type (Math or Portuguese) using buttons
    course_type = st.radio('Select Course', ('Math', 'Portuguese'))

    # Load the dataset based on the selected course
    df = load_data('mat' if course_type == 'Math' else 'por')

    # Display dataset preview
    st.write("### Dataset Preview")
    st.write(df.head())

    # Sliders for selecting grade range (from 0 to 20)
    grade_range = st.slider("Select Grade Range", 0, 20, (0, 20))
    filtered_df = df[(df['g3'] >= grade_range[0]) & (df['g3'] <= grade_range[1])]
    st.write(f"### Filtered Dataset (Grades between {grade_range[0]} and {grade_range[1]})")
    st.write(filtered_df.head())

    # Dropdown for choosing visualization type
    visualization_type = st.selectbox('Choose a Visualization:', 
                                     ['Grade Distribution Histogram', 'Boxplot by Gender', 'Family Support Pie Chart', 
                                      'Age vs Grade Scatter', 'Grade vs Absences Scatter'])
    
    # Generate and display the selected visualization
    if visualization_type == 'Grade Distribution Histogram':
        fig = create_grade_histogram(filtered_df)
    elif visualization_type == 'Boxplot by Gender':
        fig = create_grade_boxplot(filtered_df)
    elif visualization_type == 'Family Support Pie Chart':
        fig = create_famsup_pie_chart(filtered_df)
    elif visualization_type == 'Age vs Grade Scatter':
        fig = create_age_grade_scatter(filtered_df)
    elif visualization_type == 'Grade vs Absences Scatter':
        fig = create_grade_by_absences(filtered_df)

    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
