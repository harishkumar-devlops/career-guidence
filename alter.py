import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Career Guidance Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 18px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .option-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s;
        cursor: pointer;
        margin: 10px;
    }
    .option-card h2 {
        color: #667eea;
    }
    .option-card h3 {
        color: #333333;
        font-weight: bold;
    }
    .option-card p {
        color: #666666;
    }
    .option-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
    }
    h1 {
        color: white;
        text-align: center;
        padding: 20px;
    }
    h2, h3 {
        color: #667eea;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .quiz-question {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .quiz-question h4 {
        color: #333;
        margin-bottom: 15px;
    }
    .analysis-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Skill Test Questions Database (same as before)
SKILL_TESTS = {
    'Python': [
        {'q': 'What is the output of: print(type([]))?', 'options': ['<class "list">', '<class "dict">', '<class "tuple">', '<class "set">'], 'answer': 0},
        # ... (rest of your skill tests remain the same)
    ],
    # ... (other skills remain the same)
}

# Add generic tests for skills not in database
def generate_generic_test(skill_name):
    return [
        {'q': f'What is the primary purpose of {skill_name} in professional settings?', 'options': ['Entertainment', 'Problem solving and value creation', 'Time wasting', 'Random activity'], 'answer': 1},
        # ... (rest of generic tests remain the same)
    ]

# Load and cache data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/harishkumar-devlops/career-guidence/refs/heads/main/FINAL%20DATASET.csv"
    df = pd.read_csv(url)
    return df

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'certified_skills' not in st.session_state:
    st.session_state.certified_skills = []

if 'test_in_progress' not in st.session_state:
    st.session_state.test_in_progress = False

if 'current_test_skill' not in st.session_state:
    st.session_state.current_test_skill = None

if 'test_answers' not in st.session_state:
    st.session_state.test_answers = {}

# Navigation function
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Home Page - UPDATED WITH NEW OPTION
def home_page():
    st.markdown("<h1>🎯 Welcome to Career Guidance Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 20px;'>Your path to the perfect career starts here</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)  # Added one more column
    
    with col1:
        st.markdown("""
        <div class='option-card'>
            <h2>🚀</h2>
            <h3>Find Your Career Path</h3>
            <p>Discover the perfect career based on your skills and interests</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started", key="career_path"):
            navigate_to('career_path')
    
    with col2:
        st.markdown("""
        <div class='option-card'>
            <h2>💼</h2>
            <h3>Find Your Job</h3>
            <p>Search for job opportunities that match your profile</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Jobs", key="find_job"):
            navigate_to('find_job')
    
    with col3:
        st.markdown("""
        <div class='option-card'>
            <h2>📊</h2>
            <h3>Test Your Skills</h3>
            <p>Evaluate your current skill level and get certified</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Take Test", key="test_skills"):
            navigate_to('test_skills')
    
    with col4:
        st.markdown("""
        <div class='option-card'>
            <h2>🎓</h2>
            <h3>View Skill Sets</h3>
            <p>Explore required skills for different career paths</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Skills", key="view_skills"):
            navigate_to('view_skills')
    
    with col5:
        st.markdown("""
        <div class='option-card'>
            <h2>📈</h2>
            <h3>Dataset Analysis</h3>
            <p>Explore insights and trends from our career dataset</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Analysis", key="dataset_analysis"):
            navigate_to('dataset_analysis')

# Dataset Analysis Page - NEW FUNCTION
def dataset_analysis_page():
    st.markdown("<h1>📈 Dataset Analysis & Insights</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    # Load data
    df = load_data()
    
    st.markdown("---")
    
    # Dataset Overview
    st.markdown("## 📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Number of Occupations", df['occupation'].nunique())
    with col3:
        st.metric("Number of Skills", df['skills'].nunique())
    with col4:
        st.metric("Average Income", f"${df['income'].mean():,.0f}")
    
    st.markdown("---")
    
    # Income Distribution
    st.markdown("## 💰 Income Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Income distribution histogram
        fig_income = px.histogram(df, x='income', nbins=50, 
                                title='Income Distribution',
                                labels={'income': 'Annual Income ($)'},
                                color_discrete_sequence=['#667eea'])
        fig_income.update_layout(showlegend=False)
        st.plotly_chart(fig_income, use_container_width=True)
    
    with col2:
        # Income by gender
        income_by_gender = df.groupby('sex')['income'].mean().reset_index()
        fig_gender = px.bar(income_by_gender, x='sex', y='income',
                          title='Average Income by Gender',
                          labels={'sex': 'Gender', 'income': 'Average Income ($)'},
                          color='sex')
        st.plotly_chart(fig_gender, use_container_width=True)
    
    st.markdown("---")
    
    # Education Analysis
    st.markdown("## 🎓 Education Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Education distribution
        education_counts = df['education'].value_counts()
        fig_edu = px.pie(education_counts, values=education_counts.values, 
                        names=education_counts.index,
                        title='Education Level Distribution')
        st.plotly_chart(fig_edu, use_container_width=True)
    
    with col2:
        # Income by education
        income_by_edu = df.groupby('education')['income'].mean().sort_values(ascending=False)
        fig_edu_income = px.bar(income_by_edu, x=income_by_edu.index, y=income_by_edu.values,
                              title='Average Income by Education Level',
                              labels={'x': 'Education Level', 'y': 'Average Income ($)'},
                              color=income_by_edu.values)
        st.plotly_chart(fig_edu_income, use_container_width=True)
    
    st.markdown("---")
    
    # Occupation Analysis
    st.markdown("## 💼 Occupation Analysis")
    
    # Top 10 highest paying occupations
    top_occupations = df.groupby('occupation')['income'].mean().sort_values(ascending=False).head(10)
    
    fig_occupations = px.bar(top_occupations, x=top_occupations.values, y=top_occupations.index,
                           orientation='h',
                           title='Top 10 Highest Paying Occupations',
                           labels={'x': 'Average Income ($)', 'y': 'Occupation'},
                           color=top_occupations.values)
    st.plotly_chart(fig_occupations, use_container_width=True)
    
    st.markdown("---")
    
    # Skills Analysis
    st.markdown("## 🛠️ Skills Analysis")
    
    # Extract all skills
    all_skills = []
    for skills in df['skills'].dropna():
        skill_list = [s.strip() for s in str(skills).split(',')]
        all_skills.extend(skill_list)
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(15))
    
    fig_skills = px.bar(x=list(top_skills.values()), y=list(top_skills.keys()),
                       orientation='h',
                       title='Top 15 Most Common Skills',
                       labels={'x': 'Frequency', 'y': 'Skills'},
                       color=list(top_skills.values()))
    st.plotly_chart(fig_skills, use_container_width=True)
    
    st.markdown("---")
    
    # Work Class Analysis
    st.markdown("## 🏢 Work Class Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        workclass_counts = df['workclass'].value_counts()
        fig_workclass = px.pie(workclass_counts, values=workclass_counts.values,
                             names=workclass_counts.index,
                             title='Work Class Distribution')
        st.plotly_chart(fig_workclass, use_container_width=True)
    
    with col2:
        income_by_workclass = df.groupby('workclass')['income'].mean().sort_values(ascending=False)
        fig_workclass_income = px.bar(income_by_workclass, x=income_by_workclass.index, y=income_by_workclass.values,
                                    title='Average Income by Work Class',
                                    labels={'x': 'Work Class', 'y': 'Average Income ($)'},
                                    color=income_by_workclass.values)
        st.plotly_chart(fig_workclass_income, use_container_width=True)
    
    st.markdown("---")
    
    # Age and Hours Analysis
    st.markdown("## 📅 Age & Hours Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        fig_age = px.histogram(df, x='age', nbins=20,
                             title='Age Distribution',
                             labels={'age': 'Age'},
                             color_discrete_sequence=['#764ba2'])
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # Hours per week distribution
        fig_hours = px.histogram(df, x='hours-per-week', nbins=20,
                               title='Weekly Hours Distribution',
                               labels={'hours-per-week': 'Hours per Week'},
                               color_discrete_sequence=['#f093fb'])
        st.plotly_chart(fig_hours, use_container_width=True)
    
    st.markdown("---")
    
    # Interests Analysis
    st.markdown("## 🎯 Interests Analysis")
    
    interests_counts = df['interests'].value_counts().head(10)
    fig_interests = px.bar(interests_counts, x=interests_counts.values, y=interests_counts.index,
                         orientation='h',
                         title='Top 10 Interests Distribution',
                         labels={'x': 'Count', 'y': 'Interests'},
                         color=interests_counts.values)
    st.plotly_chart(fig_interests, use_container_width=True)
    
    st.markdown("---")
    
    # Correlation Analysis
    st.markdown("## 🔗 Correlation Analysis")
    
    # Create numerical features for correlation
    df_numeric = df.copy()
    
    # Encode categorical variables
    le = LabelEncoder()
    categorical_columns = ['sex', 'education', 'workclass', 'marital-status', 'occupation', 'interests']
    
    for col in categorical_columns:
        df_numeric[col] = le.fit_transform(df[col].astype(str))
    
    # Calculate correlation matrix
    correlation_matrix = df_numeric.corr()
    
    fig_corr = px.imshow(correlation_matrix,
                       title='Correlation Matrix of Features',
                       color_continuous_scale='RdBu_r',
                       aspect="auto")
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive Filters for Detailed Analysis
    st.markdown("## 🔍 Interactive Data Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_occupation = st.selectbox("Select Occupation for Analysis", 
                                         ['All'] + sorted(df['occupation'].unique().tolist()))
        selected_education = st.selectbox("Filter by Education", 
                                        ['All'] + sorted(df['education'].unique().tolist()))
    
    with col2:
        selected_workclass = st.selectbox("Filter by Work Class", 
                                        ['All'] + sorted(df['workclass'].unique().tolist()))
        selected_interest = st.selectbox("Filter by Interest", 
                                       ['All'] + sorted(df['interests'].unique().tolist()))
    
    # Filter data based on selections
    filtered_data = df.copy()
    
    if selected_occupation != 'All':
        filtered_data = filtered_data[filtered_data['occupation'] == selected_occupation]
    if selected_education != 'All':
        filtered_data = filtered_data[filtered_data['education'] == selected_education]
    if selected_workclass != 'All':
        filtered_data = filtered_data[filtered_data['workclass'] == selected_workclass]
    if selected_interest != 'All':
        filtered_data = filtered_data[filtered_data['interests'] == selected_interest]
    
    # Display filtered statistics
    if len(filtered_data) > 0:
        st.markdown(f"### 📋 Filtered Dataset Statistics ({len(filtered_data)} records)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Income", f"${filtered_data['income'].mean():,.0f}")
        with col2:
            st.metric("Average Age", f"{filtered_data['age'].mean():.1f}")
        with col3:
            st.metric("Average Hours/Week", f"{filtered_data['hours-per-week'].mean():.1f}")
        with col4:
            st.metric("Gender Distribution", 
                     f"{(filtered_data['sex'] == 'Male').mean()*100:.1f}% Male")
    
    # Show sample of filtered data
    if st.checkbox("Show Sample Data"):
        st.dataframe(filtered_data.head(10))

# All other existing functions remain the same (career_path_page, test_skills_page, prediction_page, find_job_page, view_skills_page, conduct_skill_test)

# Career Path Prediction Page (unchanged)
def career_path_page():
    st.markdown("<h1>🚀 Find Your Career Path</h1>", unsafe_allow_html=True)
    # ... (rest of the function remains exactly the same)

# Skill Test Page (unchanged)
def test_skills_page():
    st.markdown("<h1>📊 Test Your Skills</h1>", unsafe_allow_html=True)
    # ... (rest of the function remains exactly the same)

# Prediction Results Page (unchanged)
def prediction_page():
    st.markdown("<h1>🎯 Your Career Prediction</h1>", unsafe_allow_html=True)
    # ... (rest of the function remains exactly the same)

# Find Job Page (unchanged)
def find_job_page():
    st.markdown("<h1>💼 Find Your Job</h1>", unsafe_allow_html=True)
    # ... (rest of the function remains exactly the same)

# View Skills Page (unchanged)
def view_skills_page():
    st.markdown("<h1>🎓 View Skill Sets for Each Job</h1>", unsafe_allow_html=True)
    # ... (rest of the function remains exactly the same)

# Conduct skill test function (unchanged)
def conduct_skill_test(skill_name):
    st.markdown(f"### 📝 Testing: {skill_name}")
    # ... (rest of the function remains exactly the same)

# Main app routing - UPDATED
def main():
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'career_path':
        career_path_page()
    elif st.session_state.page == 'prediction':
        prediction_page()
    elif st.session_state.page == 'find_job':
        find_job_page()
    elif st.session_state.page == 'test_skills':
        test_skills_page()
    elif st.session_state.page == 'view_skills':
        view_skills_page()
    elif st.session_state.page == 'dataset_analysis':  # NEW
        dataset_analysis_page()

if __name__ == "__main__":
    main()