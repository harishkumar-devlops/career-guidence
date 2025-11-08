import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="Career Guidance Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with modern, attractive styling
st.markdown("""
<style>
    /* Main Background with animated gradient */
    .main {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism effect for containers */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 45px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Modern Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 18px 40px;
        font-size: 18px;
        font-weight: 600;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Option Cards with modern design */
    .option-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.8) 100%);
        padding: 40px 30px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        margin: 15px 0;
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .option-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        transition: left 0.5s;
    }
    
    .option-card:hover::before {
        left: 100%;
    }
    
    .option-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
        border: 2px solid #667eea;
    }
    
    .option-card h2 {
        font-size: 60px;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .option-card h3 {
        color: #2d3748;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 12px;
    }
    
    .option-card p {
        color: #4a5568;
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Header Styling */
    h1 {
        color: white;
        text-align: center;
        padding: 30px;
        font-size: 56px;
        font-weight: 800;
        text-shadow: 0 5px 15px rgba(0,0,0,0.3);
        letter-spacing: 2px;
        margin-bottom: 20px;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    h2 {
        color: #667eea;
        font-weight: 700;
        font-size: 32px;
    }
    
    h3 {
        color: #764ba2;
        font-weight: 600;
        font-size: 24px;
    }
    
    /* Prediction Card with gradient */
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 35px;
        border-radius: 25px;
        margin: 15px 0;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.6);
    }
    
    .prediction-card h1 {
        font-size: 48px;
        margin: 10px 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Quiz Question Card */
    .quiz-question {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .quiz-question:hover {
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        transform: translateX(5px);
    }
    
    .quiz-question h4 {
        color: #2d3748;
        margin-bottom: 15px;
        font-size: 20px;
        font-weight: 600;
    }
    
    /* Metric styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Select box and input styling */
    .stSelectbox, .stMultiSelect {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        font-weight: 600;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Hero section */
    .hero-text {
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: 300;
        margin-bottom: 50px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    .stats-number {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .stats-label {
        font-size: 16px;
        color: #4a5568;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Download button special styling */
    .download-btn {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Back button styling */
    div[data-testid="column"]:first-child .stButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.4);
    }
    
    div[data-testid="column"]:first-child .stButton>button:hover {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# Skill Test Questions Database
SKILL_TESTS = {
    'Python': [
        {'q': 'What is the output of: print(type([]))?', 'options': ['<class "list">', '<class "dict">', '<class "tuple">', '<class "set">'], 'answer': 0},
        {'q': 'Which keyword is used to define a function in Python?', 'options': ['function', 'def', 'func', 'define'], 'answer': 1},
        {'q': 'What does "len([1,2,3])" return?', 'options': ['2', '3', '4', 'Error'], 'answer': 1},
        {'q': 'Which of these is a mutable data type?', 'options': ['tuple', 'string', 'list', 'int'], 'answer': 2},
        {'q': 'What is the correct syntax for a for loop?', 'options': ['for i in range(10)', 'for (i=0; i<10; i++)', 'for i to 10', 'loop i in 10'], 'answer': 0},
        {'q': 'Which operator is used for exponentiation?', 'options': ['^', '**', 'exp', 'pow'], 'answer': 1},
        {'q': 'What is used to handle exceptions?', 'options': ['catch-throw', 'try-except', 'error-handle', 'exception-catch'], 'answer': 1},
        {'q': 'How do you create a dictionary?', 'options': ['[]', '()', '{}', '<>'], 'answer': 2},
        {'q': 'What does "import" keyword do?', 'options': ['Export module', 'Load external module', 'Delete module', 'Create module'], 'answer': 1},
        {'q': 'Which method adds an element to a list?', 'options': ['add()', 'append()', 'insert()', 'push()'], 'answer': 1}
    ],
    'Java': [
        {'q': 'Which keyword is used to create a class?', 'options': ['class', 'Class', 'struct', 'object'], 'answer': 0},
        {'q': 'What is the main method signature?', 'options': ['void main()', 'public static void main(String[] args)', 'static main()', 'main()'], 'answer': 1},
        {'q': 'Which is not a primitive data type?', 'options': ['int', 'String', 'boolean', 'char'], 'answer': 1},
        {'q': 'What does JVM stand for?', 'options': ['Java Virtual Machine', 'Java Variable Method', 'Just Virtual Machine', 'Java Version Manager'], 'answer': 0},
        {'q': 'Which keyword is used for inheritance?', 'options': ['inherits', 'extends', 'implements', 'derive'], 'answer': 1},
        {'q': 'What is encapsulation?', 'options': ['Data hiding', 'Multiple inheritance', 'Method overloading', 'Polymorphism'], 'answer': 0},
        {'q': 'Which collection allows duplicate elements?', 'options': ['Set', 'Map', 'List', 'Queue'], 'answer': 2},
        {'q': 'What is the default value of boolean?', 'options': ['true', 'false', 'null', '0'], 'answer': 1},
        {'q': 'Which access modifier is most restrictive?', 'options': ['public', 'protected', 'private', 'default'], 'answer': 2},
        {'q': 'What is used to handle exceptions?', 'options': ['try-catch', 'if-else', 'switch', 'loop'], 'answer': 0}
    ],
    'Data Analysis': [
        {'q': 'Which measure represents the middle value?', 'options': ['Mean', 'Median', 'Mode', 'Range'], 'answer': 1},
        {'q': 'What does SQL stand for?', 'options': ['Structured Query Language', 'Simple Query Language', 'Standard Query Language', 'System Query Language'], 'answer': 0},
        {'q': 'Which chart is best for showing trends over time?', 'options': ['Pie chart', 'Bar chart', 'Line chart', 'Scatter plot'], 'answer': 2},
        {'q': 'What is the purpose of data cleaning?', 'options': ['Delete data', 'Remove errors and inconsistencies', 'Encrypt data', 'Backup data'], 'answer': 1},
        {'q': 'Which correlation coefficient indicates strong positive correlation?', 'options': ['-0.9', '0.1', '0.95', '0'], 'answer': 2},
        {'q': 'What does ETL stand for?', 'options': ['Extract, Transform, Load', 'Execute, Test, Launch', 'Evaluate, Test, Log', 'Export, Transfer, Link'], 'answer': 0},
        {'q': 'Which is a measure of data dispersion?', 'options': ['Mean', 'Standard Deviation', 'Median', 'Mode'], 'answer': 1},
        {'q': 'What is a pivot table used for?', 'options': ['Data entry', 'Data summarization', 'Data deletion', 'Data encryption'], 'answer': 1},
        {'q': 'Which type of data has categories?', 'options': ['Numerical', 'Categorical', 'Continuous', 'Interval'], 'answer': 1},
        {'q': 'What is the first step in data analysis?', 'options': ['Visualization', 'Data collection', 'Modeling', 'Reporting'], 'answer': 1}
    ],
    'Machine Learning': [
        {'q': 'What type of learning uses labeled data?', 'options': ['Unsupervised', 'Supervised', 'Reinforcement', 'Transfer'], 'answer': 1},
        {'q': 'Which algorithm is used for classification?', 'options': ['Linear Regression', 'Decision Tree', 'K-means', 'PCA'], 'answer': 1},
        {'q': 'What is overfitting?', 'options': ['Model too simple', 'Model too complex', 'Perfect model', 'No training'], 'answer': 1},
        {'q': 'Which metric evaluates classification?', 'options': ['MSE', 'R-squared', 'Accuracy', 'MAE'], 'answer': 2},
        {'q': 'What does CNN stand for?', 'options': ['Convolutional Neural Network', 'Continuous Neural Network', 'Complex Neural Network', 'Circular Neural Network'], 'answer': 0},
        {'q': 'Which is an unsupervised learning task?', 'options': ['Classification', 'Regression', 'Clustering', 'Prediction'], 'answer': 2},
        {'q': 'What is feature engineering?', 'options': ['Creating new features', 'Deleting features', 'Visualizing features', 'Testing features'], 'answer': 0},
        {'q': 'Which activation function is commonly used?', 'options': ['Linear', 'ReLU', 'Square', 'Cubic'], 'answer': 1},
        {'q': 'What is cross-validation used for?', 'options': ['Data cleaning', 'Model evaluation', 'Feature selection', 'Data collection'], 'answer': 1},
        {'q': 'What does SGD stand for?', 'options': ['Simple Gradient Descent', 'Stochastic Gradient Descent', 'Standard Gradient Descent', 'Smooth Gradient Descent'], 'answer': 1}
    ],
    'Communication': [
        {'q': 'What is active listening?', 'options': ['Talking loudly', 'Fully concentrating on speaker', 'Interrupting frequently', 'Multitasking'], 'answer': 1},
        {'q': 'What percentage of communication is non-verbal?', 'options': ['20%', '50%', '70%', '90%'], 'answer': 2},
        {'q': 'What is the best way to handle conflict?', 'options': ['Avoid it', 'Escalate it', 'Address it constructively', 'Ignore it'], 'answer': 2},
        {'q': 'What is empathy in communication?', 'options': ['Sympathy', 'Understanding others feelings', 'Agreeing always', 'Judging others'], 'answer': 1},
        {'q': 'What is feedback?', 'options': ['Criticism only', 'Response to communication', 'Ignoring message', 'Delaying response'], 'answer': 1},
        {'q': 'What is assertive communication?', 'options': ['Aggressive', 'Passive', 'Clear and respectful', 'Silent'], 'answer': 2},
        {'q': 'What is the purpose of body language?', 'options': ['Confuse others', 'Convey non-verbal messages', 'Replace words', 'Hide feelings'], 'answer': 1},
        {'q': 'What is paraphrasing?', 'options': ['Copying exactly', 'Restating in own words', 'Ignoring', 'Changing meaning'], 'answer': 1},
        {'q': 'What is the best meeting practice?', 'options': ['No agenda', 'Clear objectives', 'Long duration', 'No preparation'], 'answer': 1},
        {'q': 'What is professional email etiquette?', 'options': ['All caps', 'Clear subject line', 'No greeting', 'Informal language'], 'answer': 1}
    ],
    'Leadership': [
        {'q': 'What defines a good leader?', 'options': ['Authority', 'Inspiring others', 'Being bossy', 'Working alone'], 'answer': 1},
        {'q': 'What is delegation?', 'options': ['Doing everything yourself', 'Assigning tasks to others', 'Avoiding responsibility', 'Ignoring team'], 'answer': 1},
        {'q': 'What is emotional intelligence?', 'options': ['IQ level', 'Understanding and managing emotions', 'Being emotional', 'Hiding feelings'], 'answer': 1},
        {'q': 'What is transformational leadership?', 'options': ['Maintaining status quo', 'Inspiring change and innovation', 'Micromanaging', 'Authoritarian'], 'answer': 1},
        {'q': 'What is team motivation?', 'options': ['Threats', 'Inspiration and encouragement', 'Pressure', 'Competition only'], 'answer': 1},
        {'q': 'What is strategic thinking?', 'options': ['Short-term focus', 'Long-term planning', 'Random decisions', 'Following blindly'], 'answer': 1},
        {'q': 'What is conflict resolution?', 'options': ['Avoiding conflicts', 'Addressing and solving disputes', 'Escalating issues', 'Ignoring problems'], 'answer': 1},
        {'q': 'What is mentorship?', 'options': ['Bossing around', 'Guiding and developing others', 'Criticizing only', 'Competing'], 'answer': 1},
        {'q': 'What is accountability?', 'options': ['Blaming others', 'Taking responsibility', 'Avoiding tasks', 'Delegation only'], 'answer': 1},
        {'q': 'What is vision in leadership?', 'options': ['Eyesight', 'Clear future direction', 'Past focus', 'Confusion'], 'answer': 1}
    ],
    'Excel': [
        {'q': 'What function adds numbers?', 'options': ['ADD()', 'SUM()', 'TOTAL()', 'PLUS()'], 'answer': 1},
        {'q': 'What is a cell reference?', 'options': ['Cell color', 'Cell address (A1)', 'Cell size', 'Cell content'], 'answer': 1},
        {'q': 'What does VLOOKUP do?', 'options': ['Delete data', 'Search vertically', 'Sort data', 'Format cells'], 'answer': 1},
        {'q': 'What is a pivot table?', 'options': ['Data summary tool', 'Chart type', 'Formula', 'Cell format'], 'answer': 0},
        {'q': 'What symbol starts a formula?', 'options': ['#', '@', '=', '+'], 'answer': 2},
        {'q': 'What is conditional formatting?', 'options': ['Cell borders', 'Format based on conditions', 'Font style', 'Cell merge'], 'answer': 1},
        {'q': 'What does IF function do?', 'options': ['Add numbers', 'Logical test', 'Format text', 'Delete cells'], 'answer': 1},
        {'q': 'What is a macro?', 'options': ['Large cell', 'Automated task', 'Formula error', 'Chart type'], 'answer': 1},
        {'q': 'What does CONCATENATE do?', 'options': ['Divide', 'Join text', 'Sum', 'Average'], 'answer': 1},
        {'q': 'What is data validation?', 'options': ['Data backup', 'Control input values', 'Delete data', 'Format cells'], 'answer': 1}
    ],
    'SQL': [
        {'q': 'What does SELECT do?', 'options': ['Delete data', 'Retrieve data', 'Update data', 'Create table'], 'answer': 1},
        {'q': 'Which clause filters rows?', 'options': ['SELECT', 'FROM', 'WHERE', 'ORDER BY'], 'answer': 2},
        {'q': 'What is a primary key?', 'options': ['First column', 'Unique identifier', 'Last column', 'Any column'], 'answer': 1},
        {'q': 'What does JOIN do?', 'options': ['Combine tables', 'Delete rows', 'Create table', 'Update data'], 'answer': 0},
        {'q': 'What is GROUP BY used for?', 'options': ['Sorting', 'Aggregating data', 'Filtering', 'Joining'], 'answer': 1},
        {'q': 'What does COUNT() return?', 'options': ['Sum', 'Number of rows', 'Average', 'Maximum'], 'answer': 1},
        {'q': 'What is an index?', 'options': ['Table name', 'Performance optimizer', 'Data type', 'Column name'], 'answer': 1},
        {'q': 'What does UPDATE do?', 'options': ['Retrieve data', 'Modify existing data', 'Delete data', 'Create table'], 'answer': 1},
        {'q': 'What is a foreign key?', 'options': ['Primary key', 'Reference to another table', 'First column', 'Last column'], 'answer': 1},
        {'q': 'What does DISTINCT do?', 'options': ['Show all rows', 'Remove duplicates', 'Sort data', 'Join tables'], 'answer': 1}
    ],
    'Project Management': [
        {'q': 'What is a project?', 'options': ['Ongoing operation', 'Temporary endeavor', 'Daily routine', 'Permanent activity'], 'answer': 1},
        {'q': 'What is a stakeholder?', 'options': ['Project member only', 'Anyone affected by project', 'Manager only', 'Customer only'], 'answer': 1},
        {'q': 'What is scope creep?', 'options': ['Planned changes', 'Uncontrolled expansion', 'Budget increase', 'Time extension'], 'answer': 1},
        {'q': 'What is a Gantt chart?', 'options': ['Budget tool', 'Timeline visualization', 'Risk matrix', 'Org chart'], 'answer': 1},
        {'q': 'What is critical path?', 'options': ['Longest task sequence', 'Shortest path', 'Most expensive tasks', 'Easiest tasks'], 'answer': 0},
        {'q': 'What is agile methodology?', 'options': ['Rigid planning', 'Iterative approach', 'No planning', 'Sequential'], 'answer': 1},
        {'q': 'What is a sprint?', 'options': ['Long project', 'Short iteration', 'Full project', 'Annual review'], 'answer': 1},
        {'q': 'What is risk management?', 'options': ['Ignoring risks', 'Identifying and mitigating risks', 'Taking all risks', 'Avoiding projects'], 'answer': 1},
        {'q': 'What is a milestone?', 'options': ['Daily task', 'Significant point', 'Small task', 'Budget item'], 'answer': 1},
        {'q': 'What is resource allocation?', 'options': ['Spending money', 'Assigning resources', 'Firing people', 'Buying equipment'], 'answer': 1}
    ],
    'Public Speaking': [
        {'q': 'What is the fear of public speaking called?', 'options': ['Agoraphobia', 'Glossophobia', 'Claustrophobia', 'Acrophobia'], 'answer': 1},
        {'q': 'What is the ideal speech structure?', 'options': ['Random points', 'Introduction, Body, Conclusion', 'Only facts', 'Only stories'], 'answer': 1},
        {'q': 'What is eye contact important for?', 'options': ['Intimidation', 'Building connection', 'Showing superiority', 'Avoiding audience'], 'answer': 1},
        {'q': 'What is vocal variety?', 'options': ['Monotone speech', 'Changing pitch and pace', 'Loud voice only', 'Whispering'], 'answer': 1},
        {'q': 'What is body language in speaking?', 'options': ['Standing still', 'Non-verbal communication', 'Sitting down', 'Hiding'], 'answer': 1},
        {'q': 'What is audience analysis?', 'options': ['Ignoring audience', 'Understanding audience needs', 'Counting people', 'Criticizing audience'], 'answer': 1},
        {'q': 'What is a good opening?', 'options': ['Apology', 'Attention grabber', 'Long story', 'Complex jargon'], 'answer': 1},
        {'q': 'What should you do with nervousness?', 'options': ['Cancel speech', 'Channel into energy', 'Show panic', 'Run away'], 'answer': 1},
        {'q': 'What is visual aid purpose?', 'options': ['Distract audience', 'Enhance message', 'Replace speech', 'Fill time'], 'answer': 1},
        {'q': 'What is the 3-second rule?', 'options': ['Speak for 3 seconds', 'Pause for 3 seconds', 'Look at person for 3 seconds', 'Breathe for 3 seconds'], 'answer': 2}
    ],
    'HTML/CSS': [
        {'q': 'What does HTML stand for?', 'options': ['Hyper Text Markup Language', 'High Tech Modern Language', 'Home Tool Markup Language', 'Hyperlinks Text Mark Language'], 'answer': 0},
        {'q': 'Which tag creates a hyperlink?', 'options': ['<link>', '<a>', '<href>', '<url>'], 'answer': 1},
        {'q': 'What does CSS stand for?', 'options': ['Computer Style Sheets', 'Cascading Style Sheets', 'Creative Style System', 'Colorful Style Sheets'], 'answer': 1},
        {'q': 'How to select an element by ID in CSS?', 'options': ['.id', '#id', '@id', '*id'], 'answer': 1},
        {'q': 'Which property changes text color?', 'options': ['text-color', 'color', 'font-color', 'text-style'], 'answer': 1},
        {'q': 'What is the box model?', 'options': ['Container design', 'Content, Padding, Border, Margin', 'Square shape', 'Layout grid'], 'answer': 1},
        {'q': 'Which tag is for largest heading?', 'options': ['<h6>', '<heading>', '<h1>', '<head>'], 'answer': 2},
        {'q': 'What is flexbox used for?', 'options': ['Flexible layouts', 'Animations', 'Colors', 'Fonts'], 'answer': 0},
        {'q': 'How to make text bold?', 'options': ['<bold>', '<b> or <strong>', '<fat>', '<heavy>'], 'answer': 1},
        {'q': 'What is responsive design?', 'options': ['Fast loading', 'Adapts to screen sizes', 'Interactive', 'Modern look'], 'answer': 1}
    ],
    'React': [
        {'q': 'What is React?', 'options': ['Database', 'JavaScript library for UI', 'CSS framework', 'Backend language'], 'answer': 1},
        {'q': 'What are components in React?', 'options': ['Databases', 'Reusable UI pieces', 'Stylesheets', 'Server files'], 'answer': 1},
        {'q': 'What is JSX?', 'options': ['Java Extension', 'JavaScript XML', 'JSON Export', 'jQuery Syntax'], 'answer': 1},
        {'q': 'What is state in React?', 'options': ['Location', 'Component data', 'CSS style', 'HTML tag'], 'answer': 1},
        {'q': 'What hook manages state?', 'options': ['useEffect', 'useState', 'useContext', 'useRef'], 'answer': 1},
        {'q': 'What is props?', 'options': ['Properties passed to components', 'CSS properties', 'HTML attributes', 'Functions'], 'answer': 0},
        {'q': 'What does useEffect do?', 'options': ['Styling', 'Side effects and lifecycle', 'State management', 'Routing'], 'answer': 1},
        {'q': 'What is virtual DOM?', 'options': ['Real DOM', 'Lightweight DOM copy', 'Server DOM', 'Database'], 'answer': 1},
        {'q': 'How to handle events?', 'options': ['onClick={handler}', 'click="handler"', 'onclick=handler', 'on-click={handler}'], 'answer': 0},
        {'q': 'What is React Router?', 'options': ['Internet router', 'Navigation library', 'Database tool', 'CSS framework'], 'answer': 1}
    ],
    'Node.js': [
        {'q': 'What is Node.js?', 'options': ['Frontend framework', 'JavaScript runtime', 'Database', 'CSS preprocessor'], 'answer': 1},
        {'q': 'What is npm?', 'options': ['Node package manager', 'New programming method', 'Network protocol', 'Database'], 'answer': 0},
        {'q': 'What is Express.js?', 'options': ['Database', 'Web framework', 'Testing tool', 'CSS library'], 'answer': 1},
        {'q': 'What is callback?', 'options': ['Loop', 'Function passed as argument', 'Variable', 'Object'], 'answer': 1},
        {'q': 'What is middleware?', 'options': ['Database', 'Function in request-response cycle', 'Frontend code', 'HTML tag'], 'answer': 1},
        {'q': 'What is async/await?', 'options': ['Loop', 'Handling asynchronous code', 'CSS property', 'HTML attribute'], 'answer': 1},
        {'q': 'What is package.json?', 'options': ['Image file', 'Project configuration', 'CSS file', 'HTML template'], 'answer': 1},
        {'q': 'What is REST API?', 'options': ['Database', 'Web service architecture', 'CSS framework', 'HTML standard'], 'answer': 1},
        {'q': 'What is MongoDB commonly used with?', 'options': ['Only PHP', 'Node.js applications', 'Only Java', 'Only C++'], 'answer': 1},
        {'q': 'What port does HTTP use by default?', 'options': ['443', '80', '8080', '3000'], 'answer': 1}
    ],
    'Cloud Computing': [
        {'q': 'What is cloud computing?', 'options': ['Weather prediction', 'Internet-based computing', 'Desktop software', 'Mobile apps'], 'answer': 1},
        {'q': 'What is IaaS?', 'options': ['Internet as a Service', 'Infrastructure as a Service', 'Information as a Service', 'Interface as a Service'], 'answer': 1},
        {'q': 'What is AWS?', 'options': ['Amazon Web Services', 'Advanced Web System', 'Automated Work Service', 'American Web Standard'], 'answer': 0},
        {'q': 'What is virtualization?', 'options': ['Gaming', 'Creating virtual versions of resources', 'Internet browsing', 'Email service'], 'answer': 1},
        {'q': 'What is SaaS?', 'options': ['Server as a Service', 'Software as a Service', 'Storage as a Service', 'Security as a Service'], 'answer': 1},
        {'q': 'What is scalability?', 'options': ['Size measurement', 'Ability to handle growth', 'Speed test', 'Security feature'], 'answer': 1},
        {'q': 'What is a load balancer?', 'options': ['Weight scale', 'Distributes traffic', 'Power supply', 'Network cable'], 'answer': 1},
        {'q': 'What is Docker?', 'options': ['Ship worker', 'Containerization platform', 'Database', 'Programming language'], 'answer': 1},
        {'q': 'What is Kubernetes?', 'options': ['Database', 'Container orchestration', 'Programming language', 'Web browser'], 'answer': 1},
        {'q': 'What is object storage?', 'options': ['Furniture storage', 'Data storage as objects', 'File cabinet', 'Memory card'], 'answer': 1}
    ],
    'Cybersecurity': [
        {'q': 'What is a firewall?', 'options': ['Fire extinguisher', 'Network security system', 'Antivirus', 'Password'], 'answer': 1},
        {'q': 'What is encryption?', 'options': ['Deleting data', 'Converting data to code', 'Copying data', 'Moving data'], 'answer': 1},
        {'q': 'What is phishing?', 'options': ['Fishing hobby', 'Fraudulent attempt to obtain info', 'Programming', 'Testing'], 'answer': 1},
        {'q': 'What is malware?', 'options': ['Male software', 'Malicious software', 'Mail software', 'Main software'], 'answer': 1},
        {'q': 'What is two-factor authentication?', 'options': ['Two passwords', 'Two verification methods', 'Two users', 'Two devices'], 'answer': 1},
        {'q': 'What is a VPN?', 'options': ['Very Private Network', 'Virtual Private Network', 'Verified Public Network', 'Visual Private Network'], 'answer': 1},
        {'q': 'What is SQL injection?', 'options': ['Medical procedure', 'Code injection attack', 'Database creation', 'File upload'], 'answer': 1},
        {'q': 'What is a vulnerability?', 'options': ['Feature', 'Security weakness', 'Upgrade', 'Protocol'], 'answer': 1},
        {'q': 'What is penetration testing?', 'options': ['Breaking hardware', 'Authorized security testing', 'Software installation', 'Data backup'], 'answer': 1},
        {'q': 'What is ransomware?', 'options': ['Free software', 'Malware demanding payment', 'Antivirus', 'Operating system'], 'answer': 1}
    ]
}

# Add generic tests for skills not in database
def generate_generic_test(skill_name):
    return [
        {'q': f'What is the primary purpose of {skill_name} in professional settings?', 'options': ['Entertainment', 'Problem solving and value creation', 'Time wasting', 'Random activity'], 'answer': 1},
        {'q': f'Which industry commonly uses {skill_name}?', 'options': ['Agriculture only', 'Technology and Business', 'None', 'Entertainment only'], 'answer': 1},
        {'q': f'What level of expertise is typically required for {skill_name}?', 'options': ['No training needed', 'Formal education and practice', 'Natural talent only', 'Random guessing'], 'answer': 1},
        {'q': f'How would you start learning {skill_name}?', 'options': ['Ignore it', 'Study fundamentals and practice', 'Just wing it', 'Ask others to do it'], 'answer': 1},
        {'q': f'What is a key benefit of mastering {skill_name}?', 'options': ['Nothing', 'Career advancement and problem solving', 'Social media followers', 'Free time'], 'answer': 1},
        {'q': f'How often should professionals update their {skill_name} knowledge?', 'options': ['Never', 'Regularly to stay current', 'Once in lifetime', 'When forced'], 'answer': 1},
        {'q': f'What best describes {skill_name}?', 'options': ['Irrelevant skill', 'Valuable professional competency', 'Hobby only', 'Waste of time'], 'answer': 1},
        {'q': f'How can {skill_name} be applied in work?', 'options': ['Cannot be applied', 'Solving real business problems', 'Only for show', 'No practical use'], 'answer': 1},
        {'q': f'What is needed to become proficient in {skill_name}?', 'options': ['Nothing', 'Dedication and continuous practice', 'Luck only', 'Connections only'], 'answer': 1},
        {'q': f'Why is {skill_name} important in modern workplace?', 'options': ['Not important', 'Drives innovation and efficiency', 'Just a trend', 'Only for managers'], 'answer': 1}
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

if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Navigation function
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Home Page
def home_page():
    st.markdown("<h1>🎯 Career Guidance Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-text'>Your journey to the perfect career starts here - Discover, Learn, Grow</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='option-card'>
            <h2>🚀</h2>
            <h3>Find Career Path</h3>
            <p>Discover your perfect career based on skills and interests</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started", key="career_path"):
            navigate_to('career_path')
    
    with col2:
        st.markdown("""
        <div class='option-card'>
            <h2>💼</h2>
            <h3>Find Your Job</h3>
            <p>Search opportunities that match your profile</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Jobs", key="find_job"):
            navigate_to('find_job')
    
    with col3:
        st.markdown("""
        <div class='option-card'>
            <h2>📊</h2>
            <h3>Test Your Skills</h3>
            <p>Evaluate your level and get certified</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Take Test", key="test_skills"):
            navigate_to('test_skills')
    
    with col4:
        st.markdown("""
        <div class='option-card'>
            <h2>🎓</h2>
            <h3>View Skill Sets</h3>
            <p>Explore required skills for careers</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Skills", key="view_skills"):
            navigate_to('view_skills')
    
    # Add Data Analytics card in a new row
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col2:
        st.markdown("""
        <div class='option-card'>
            <h2>📈</h2>
            <h3>Data Analytics</h3>
            <p>Explore comprehensive insights and visualizations</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Analytics", key="data_analytics"):
            navigate_to('data_analytics')

# Career Path Prediction Page
def career_path_page():
    st.markdown("<h1>🚀 Find Your Career Path</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        navigate_to('home')
    
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Show certified skills
    if st.session_state.certified_skills:
        st.success(f"✅ You have {len(st.session_state.certified_skills)} certified skills: {', '.join(st.session_state.certified_skills)}")
    else:
        st.warning("⚠️ You haven't certified any skills yet. Take skill tests first!")
    
    # User input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.slider("Age", 18, 65, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        st.markdown("### 🎓 Education & Work")
        education = st.selectbox("Education Level", 
                                ['High School', 'Bachelors', 'Masters', 'PhD', 'Diploma'])
        workclass = st.selectbox("Work Class", 
                                ['Private', 'Self-employed', 'Government', 'Unemployed', 'Freelancer'])
    
    with col2:
        st.markdown("### 🛠️ Skills")
        
        # Only show certified skills for selection
        if st.session_state.certified_skills:
            selected_skills = st.multiselect(
                "Select Your Certified Skills", 
                st.session_state.certified_skills,
                help="These are your certified skills from skill tests"
            )
        else:
            st.info("📚 Please take skill tests first to certify your skills!")
            selected_skills = []
            
            # Button to go to test page
            if st.button("🎯 Go to Skill Tests"):
                navigate_to('test_skills')
        
        st.markdown("### 💡 Interests")
        interests_list = ['AI & Robotics', 'Art', 'Business', 'Design', 'Education', 
                         'Engineering', 'Entertainment', 'Entrepreneurship', 'Environment', 
                         'Finance', 'Health', 'Literature', 'Marketing', 'Politics', 
                         'Research', 'Science', 'Social Work', 'Sports', 'Technology', 'Travel']
        
        selected_interests = st.multiselect("Select Your Interests (Multiple)", interests_list)
    
    st.markdown("---")
    
    if st.button("🎯 Predict Career Path", type="primary"):
        if not selected_skills:
            st.error("❌ Please certify and select at least one skill!")
            if st.button("Take Skill Tests Now"):
                navigate_to('test_skills')
        elif not selected_interests:
            st.error("❌ Please select at least one interest!")
        else:
            st.session_state.user_data = {
                'age': age,
                'gender': gender,
                'education': education,
                'workclass': workclass,
                'skills': selected_skills,
                'interests': selected_interests
            }
            navigate_to('prediction')

# Skill Test Page
def test_skills_page():
    st.markdown("<h1>📊 Test Your Skills</h1>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.test_in_progress = False
        st.session_state.current_test_skill = None
        navigate_to('home')
    
    st.markdown("---")
    
    # Show certified skills
    if st.session_state.certified_skills:
        st.success(f"✅ **Your Certified Skills ({len(st.session_state.certified_skills)}):** {', '.join(st.session_state.certified_skills)}")
        st.markdown("---")
    
    # If test is in progress
    if st.session_state.test_in_progress and st.session_state.current_test_skill:
        conduct_skill_test(st.session_state.current_test_skill)
    else:
        st.markdown("### 🎯 Select a Skill to Test")
        st.info("💡 Pass the test with 70% or higher to certify your skill!")
        
        # Available skills
        all_skills = ['Artificial Intelligence', 'Blockchain', 'Business Analysis', 'C++', 
                      'Cloud Computing', 'Communication', 'Content Writing', 'Customer Support', 
                      'Cybersecurity', 'Data Analysis', 'Data Visualization', 'Database Management', 
                      'DevOps', 'Excel', 'Finance', 'Graphic Design', 'HTML/CSS', 'Java', 
                      'Leadership', 'Machine Learning', 'Marketing', 'Networking', 'Node.js', 
                      'Project Management', 'Public Speaking', 'Python', 'React', 'SQL',
                      'Software Engineering', 'Statistics', 'Testing', 'UI/UX Design']
        
        # Filter out already certified skills
        available_skills = [s for s in all_skills if s not in st.session_state.certified_skills]
        
        if available_skills:
            selected_test_skill = st.selectbox("Choose a skill to test", available_skills)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Test Details:**")
                st.write("- 10 questions")
                st.write("- Pass score: 70%")
                st.write("- Duration: ~10 minutes")
            with col2:
                if st.button("🚀 Start Test", type="primary"):
                    st.session_state.test_in_progress = True
                    st.session_state.current_test_skill = selected_test_skill
                    st.session_state.test_answers = {}
                    st.rerun()
        else:
            st.success("🎉 Congratulations! You have certified all available skills!")

# Conduct skill test function
def conduct_skill_test(skill_name):
    st.markdown(f"### 📝 Testing: {skill_name}")
    st.progress(0.5)
    
    # Get questions for the skill
    questions = SKILL_TESTS.get(skill_name, generate_generic_test(skill_name))
    
    # Display questions
    with st.form(f"test_form_{skill_name}"):
        user_answers = []
        
        for i, q_data in enumerate(questions):
            st.markdown(f"""
            <div class='quiz-question'>
                <h4>Question {i+1}</h4>
            </div>
            """, unsafe_allow_html=True)
            st.write(q_data['q'])
            answer = st.radio(
                f"Select your answer for Q{i+1}:",
                options=q_data['options'],
                key=f"q_{i}",
                label_visibility="collapsed"
            )
            user_answers.append(answer)
            st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("✅ Submit Test", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel Test", use_container_width=True)
    
    if cancel:
        st.session_state.test_in_progress = False
        st.session_state.current_test_skill = None
        st.rerun()
    
    if submit:
        # Calculate score
        correct = 0
        for i, q_data in enumerate(questions):
            if user_answers[i] == q_data['options'][q_data['answer']]:
                correct += 1
        
        score = (correct / len(questions)) * 100
        
        st.markdown("---")
        st.markdown("## 📊 Test Results")
        
        # Display score
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Your Score</div>
                <div class='stats-number'>{score:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Correct Answers</div>
                <div class='stats-number'>{correct}/{len(questions)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            status = "✅ PASSED" if score >= 70 else "❌ FAILED"
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Status</div>
                <div class='stats-number' style='font-size: 32px;'>{status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if score >= 70:
            st.success(f"🎉 Congratulations! You have successfully certified your {skill_name} skill!")
            if skill_name not in st.session_state.certified_skills:
                st.session_state.certified_skills.append(skill_name)
            st.balloons()
        else:
            st.error(f"Sorry, you need 70% to pass. You scored {score:.0f}%. Please try again!")
        
        # Reset test state
        st.session_state.test_in_progress = False
        st.session_state.current_test_skill = None
        
        st.info("👆 Click 'Back to Home' button at the top to continue")

# Prediction Results Page
def prediction_page():
    st.markdown("<h1>🎯 Your Career Prediction</h1>", unsafe_allow_html=True)
    
    if st.button("← Back to Form"):
        navigate_to('career_path')
    
    # Check if user_data exists
    if 'user_data' not in st.session_state:
        st.error("No prediction data found. Please fill out the form first.")
        if st.button("Go to Career Path Form"):
            navigate_to('career_path')
        return
    
    # Load data
    df = load_data()
    user_data = st.session_state.user_data
    
    # Convert user's skills and interests to match dataset format
    user_skills_str = ', '.join(user_data['skills'])
    user_interests_str = user_data['interests'][0] if user_data['interests'] else 'Technology'
    
    # Filter data based on user profile
    matching_jobs = df.copy()
    
    # Filter by education
    matching_jobs = matching_jobs[matching_jobs['education'] == user_data['education']]
    
    if len(matching_jobs) == 0:
        matching_jobs = df.copy()
    
    # Filter by workclass
    if user_data['workclass'] != 'Unemployed':
        workclass_matches = matching_jobs[matching_jobs['workclass'] == user_data['workclass']]
        if len(workclass_matches) > 0:
            matching_jobs = workclass_matches
    
    # Filter by interests
    interest_matches = matching_jobs[matching_jobs['interests'].isin(user_data['interests'])]
    if len(interest_matches) > 0:
        matching_jobs = interest_matches
    
    # Calculate skill match score
    def calculate_skill_match(job_skills):
        if pd.isna(job_skills):
            return 0
        job_skills_list = [s.strip() for s in str(job_skills).split(',')]
        matches = sum(1 for skill in user_data['skills'] if skill in job_skills_list)
        return matches
    
    matching_jobs['skill_match'] = matching_jobs['skills'].apply(calculate_skill_match)
    matching_jobs = matching_jobs.sort_values('skill_match', ascending=False)
    
    if len(matching_jobs) > 0:
        top_match = matching_jobs.iloc[0]
        predicted_job = top_match['occupation']
        predicted_income = top_match['income']
        required_skills = top_match['skills']
        job_interest = top_match['interests']
    else:
        predicted_job = df['occupation'].mode()[0]
        predicted_income = df['income'].median()
        required_skills = user_skills_str
        job_interest = user_interests_str
    
    # Display predictions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='prediction-card'>
            <h2>🎯 Predicted Job Title</h2>
            <h1>{predicted_job}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='prediction-card'>
            <h2>💰 Expected Income Range</h2>
            <h1>${predicted_income:,}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Required Skills
    st.markdown("### 🎓 Required Skills for Your Career Path")
    st.info(f"**Skills Needed:** {required_skills}")
    
    # Skills Gap Analysis
    st.markdown("### 📊 Your Profile Match")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success(f"**Your Certified Skills:** {', '.join(user_data['skills'])}")
    
    with col2:
        st.info(f"**Your Interests:** {', '.join(user_data['interests'])}")
    
    with col3:
        st.warning(f"**Job Category:** {job_interest}")
    
    # Available Jobs
    st.markdown("---")
    st.markdown("### 💼 Available Job Opportunities")
    
    job_opportunities = df[df['occupation'] == predicted_job].head(10)
    
    if len(job_opportunities) > 0:
        for idx, job in job_opportunities.iterrows():
            with st.expander(f"📍 {job['occupation']} - ${job['income']:,}/year | {job['workclass']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Education Required:** {job['education']}")
                    st.write(f"**Work Class:** {job['workclass']}")
                    st.write(f"**Experience Level:** {job['age']} years old average")
                with col2:
                    st.write(f"**Skills Required:** {job['skills']}")
                    st.write(f"**Industry:** {job['interests']}")
                    st.write(f"**Work Hours:** {job['hours-per-week']} hrs/week")
    
    # Income comparison chart
    st.markdown("---")
    st.markdown("### 💰 Income Comparison by Job")
    
    income_by_job = df.groupby('occupation')['income'].mean().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=income_by_job.values,
        y=income_by_job.index,
        orientation='h',
        labels={'x': 'Average Income ($)', 'y': 'Job Title'},
        title='Top 10 Highest Paying Jobs',
        color=income_by_job.values,
        color_continuous_scale='Viridis'
    )
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔄 Try Another Prediction", type="primary"):
        navigate_to('career_path')

# Find Job Page
def find_job_page():
    st.markdown("<h1>💼 Find Your Job</h1>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        navigate_to('home')
    
    df = load_data()
    
    st.markdown("### 🔍 Search Jobs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_occupation = st.selectbox("Select Job Title", ['All'] + sorted(df['occupation'].unique().tolist()))
        search_education = st.selectbox("Education Level", ['All'] + sorted(df['education'].unique().tolist()))
    
    with col2:
        search_workclass = st.selectbox("Work Class", ['All'] + sorted(df['workclass'].unique().tolist()))
        search_interest = st.selectbox("Industry/Interest", ['All'] + sorted(df['interests'].unique().tolist()))
    
    # Filter data
    filtered_df = df.copy()
    
    if search_occupation != 'All':
        filtered_df = filtered_df[filtered_df['occupation'] == search_occupation]
    if search_education != 'All':
        filtered_df = filtered_df[filtered_df['education'] == search_education]
    if search_workclass != 'All':
        filtered_df = filtered_df[filtered_df['workclass'] == search_workclass]
    if search_interest != 'All':
        filtered_df = filtered_df[filtered_df['interests'] == search_interest]
    
    st.markdown(f"### Found {len(filtered_df)} Jobs")
    
    for idx, job in filtered_df.head(20).iterrows():
        with st.expander(f"💼 {job['occupation']} - ${job['income']:,}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Education:** {job['education']}")
                st.write(f"**Work Type:** {job['workclass']}")
                st.write(f"**Industry:** {job['interests']}")
            with col2:
                st.write(f"**Skills:** {job['skills']}")
                st.write(f"**Hours/Week:** {job['hours-per-week']}")

# View Skills Page
def view_skills_page():
    st.markdown("<h1>🎓 View Skill Sets for Each Job</h1>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        navigate_to('home')
    
    df = load_data()
    
    job_titles = sorted(df['occupation'].unique())
    selected_job = st.selectbox("Select a Job Title", job_titles)
    
    if selected_job:
        job_data = df[df['occupation'] == selected_job]
        
        avg_income = job_data['income'].mean()
        avg_hours = job_data['hours-per-week'].mean()
        common_education = job_data['education'].mode()[0]
        common_workclass = job_data['workclass'].mode()[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📋 Job Overview")
            st.metric("Average Income", f"${avg_income:,.0f}")
            st.metric("Avg Hours/Week", f"{avg_hours:.0f}")
        
        with col2:
            st.markdown("### 🎓 Requirements")
            st.write(f"**Common Education:** {common_education}")
            st.write(f"**Work Type:** {common_workclass}")
            st.write(f"**Total Positions:** {len(job_data)}")
        
        with col3:
            st.markdown("### 🛠️ Key Skills")
            all_skills = []
            for skills in job_data['skills'].dropna():
                all_skills.extend([s.strip() for s in str(skills).split(',')])
            from collections import Counter
            top_skills = Counter(all_skills).most_common(5)
            for skill, count in top_skills:
                st.write(f"✓ {skill}")
        
        st.markdown("---")
        st.markdown("### 💼 Sample Job Listings")
        
        for idx, job in job_data.head(5).iterrows():
            with st.expander(f"Position {idx + 1}: ${job['income']:,}"):
                st.write(f"**Skills Required:** {job['skills']}")
                st.write(f"**Education:** {job['education']}")
                st.write(f"**Industry:** {job['interests']}")

# Data Analytics Page
def data_analytics_page():
    st.markdown("<h1>📈 Data Analytics Dashboard</h1>", unsafe_allow_html=True)
    if st.button("← Back to Home"):
        navigate_to('home')
    
    df = load_data()
    
    # Display dataset info first to understand columns
    st.sidebar.markdown("## ℹ️ Dataset Info")
    if st.sidebar.checkbox("Show Dataset Columns"):
        st.sidebar.write("**Available Columns:**")
        st.sidebar.write(list(df.columns))
        st.sidebar.write(f"**Dataset Shape:** {df.shape}")
    
    # Sidebar for analysis options
    st.sidebar.markdown("## 🎯 Analysis Options")
    analysis_type = st.sidebar.radio(
        "Select Analysis Type",
        ["Overview", "Income Analysis", "Education & Skills", "Work Distribution", "Advanced Insights"]
    )
    
    st.markdown("---")
    
    # OVERVIEW SECTION
    if analysis_type == "Overview":
        st.markdown("## 📊 Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Total Records</div>
                <div class='stats-number'>{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Unique Jobs</div>
                <div class='stats-number'>{df['occupation'].nunique():,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Avg Income</div>
                <div class='stats-number'>${df['income'].mean():,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class='stats-card'>
                <div class='stats-label'>Avg Age</div>
                <div class='stats-number'>{df['age'].mean():.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dataset Preview
        st.markdown("### 📋 Dataset Sample")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Dataset Statistics
        st.markdown("### 📈 Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)
        
        # Missing Values Analysis
        st.markdown("### 🔍 Data Quality Check")
        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            fig = px.bar(
                x=missing_data.values,
                y=missing_data.index,
                orientation='h',
                title='Missing Values by Column',
                labels={'x': 'Count', 'y': 'Column'},
                color=missing_data.values,
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No missing values found in the dataset!")
    
    # INCOME ANALYSIS SECTION
    elif analysis_type == "Income Analysis":
        st.markdown("## 💰 Income Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Income Distribution
            st.markdown("### 📊 Income Distribution")
            fig = px.histogram(
                df,
                x='income',
                nbins=50,
                title='Income Distribution',
                labels={'income': 'Income ($)', 'count': 'Frequency'},
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Income by Occupation (Top 15)
            st.markdown("### 💼 Top 15 Highest Paying Jobs")
            top_jobs = df.groupby('occupation')['income'].mean().sort_values(ascending=False).head(15)
            fig = px.bar(
                x=top_jobs.values,
                y=top_jobs.index,
                orientation='h',
                labels={'x': 'Average Income ($)', 'y': 'Occupation'},
                color=top_jobs.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        # Income by Education
        st.markdown("### 🎓 Income by Education Level")
        income_education = df.groupby('education')['income'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=income_education.index,
            y=income_education.values,
            title='Average Income by Education Level',
            labels={'x': 'Education Level', 'y': 'Average Income ($)'},
            color=income_education.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Income by Work Class
        st.markdown("### 💼 Income by Work Class")
        col1, col2 = st.columns(2)
        
        with col1:
            income_workclass = df.groupby('workclass')['income'].mean().sort_values(ascending=False)
            fig = px.pie(
                values=income_workclass.values,
                names=income_workclass.index,
                title='Average Income Distribution by Work Class',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box plot for income by work class
            fig = px.box(
                df,
                x='workclass',
                y='income',
                title='Income Range by Work Class',
                labels={'workclass': 'Work Class', 'income': 'Income ($)'},
                color='workclass'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Income vs Hours worked
        st.markdown("### ⏰ Income vs Hours Worked Per Week")
        # Use a smaller sample for better performance
        sample_df = df.sample(n=min(500, len(df)), random_state=42)
        fig = px.scatter(
            sample_df,
            x='hours-per-week',
            y='income',
            color='workclass',
            title='Income vs Hours Worked (Sample)',
            labels={'hours-per-week': 'Hours Per Week', 'income': 'Income ($)'},
            opacity=0.6
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # EDUCATION & SKILLS SECTION
    elif analysis_type == "Education & Skills":
        st.markdown("## 🎓 Education & Skills Analysis")
        
        # Education Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📚 Education Level Distribution")
            education_counts = df['education'].value_counts()
            fig = px.pie(
                values=education_counts.values,
                names=education_counts.index,
                title='Education Level Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Education Level Counts")
            fig = px.bar(
                x=education_counts.index,
                y=education_counts.values,
                title='Number of People by Education',
                labels={'x': 'Education Level', 'y': 'Count'},
                color=education_counts.values,
                color_continuous_scale='Teal'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Skills Analysis
        st.markdown("### 🛠️ Most In-Demand Skills")
        all_skills = []
        for skills in df['skills'].dropna():
            all_skills.extend([s.strip() for s in str(skills).split(',')])
        
        skill_counts = Counter(all_skills)
        top_20_skills = dict(skill_counts.most_common(20))
        
        fig = px.bar(
            x=list(top_20_skills.values()),
            y=list(top_20_skills.keys()),
            orientation='h',
            title='Top 20 Most Required Skills',
            labels={'x': 'Frequency', 'y': 'Skill'},
            color=list(top_20_skills.values()),
            color_continuous_scale='Sunset'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills by Education Level
        st.markdown("### 📊 Skills Distribution by Education")
        education_levels = df['education'].unique()
        selected_education = st.selectbox("Select Education Level", sorted(education_levels))
        
        edu_df = df[df['education'] == selected_education]
        edu_skills = []
        for skills in edu_df['skills'].dropna():
            edu_skills.extend([s.strip() for s in str(skills).split(',')])
        
        edu_skill_counts = Counter(edu_skills)
        top_edu_skills = dict(edu_skill_counts.most_common(15))
        
        fig = px.bar(
            x=list(top_edu_skills.keys()),
            y=list(top_edu_skills.values()),
            title=f'Top Skills for {selected_education}',
            labels={'x': 'Skill', 'y': 'Frequency'},
            color=list(top_edu_skills.values()),
            color_continuous_scale='Purp'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # WORK DISTRIBUTION SECTION
    elif analysis_type == "Work Distribution":
        st.markdown("## 💼 Work Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Work Class Distribution
            st.markdown("### 🏢 Work Class Distribution")
            workclass_counts = df['workclass'].value_counts()
            fig = px.pie(
                values=workclass_counts.values,
                names=workclass_counts.index,
                title='Work Class Distribution',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hours per week distribution
            st.markdown("### ⏰ Work Hours Distribution")
            fig = px.histogram(
                df,
                x='hours-per-week',
                nbins=30,
                title='Hours Worked Per Week',
                labels={'hours-per-week': 'Hours Per Week', 'count': 'Frequency'},
                color_discrete_sequence=['#764ba2']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Interests/Industry Distribution
        st.markdown("### 🎯 Industry/Interest Distribution")
        interests_counts = df['interests'].value_counts().head(15)
        fig = px.bar(
            x=interests_counts.values,
            y=interests_counts.index,
            orientation='h',
            title='Top 15 Industries/Interests',
            labels={'x': 'Count', 'y': 'Industry'},
            color=interests_counts.values,
            color_continuous_scale='Rainbow'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Occupation Distribution
        st.markdown("### 👔 Top Occupations")
        occupation_counts = df['occupation'].value_counts().head(20)
        fig = px.treemap(
            names=occupation_counts.index,
            parents=[''] * len(occupation_counts),
            values=occupation_counts.values,
            title='Top 20 Occupations (Treemap)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Average hours by work class
        st.markdown("### 📊 Average Hours by Work Class")
        avg_hours = df.groupby('workclass')['hours-per-week'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=avg_hours.index,
            y=avg_hours.values,
            title='Average Working Hours by Work Class',
            labels={'x': 'Work Class', 'y': 'Average Hours Per Week'},
            color=avg_hours.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ADVANCED INSIGHTS SECTION
    elif analysis_type == "Advanced Insights":
        st.markdown("## 🔬 Advanced Insights")
        
        # Correlation Analysis
        st.markdown("### 📊 Correlation Analysis")
        numerical_cols = ['age', 'income', 'hours-per-week']
        # Check which numerical columns exist in the dataset
        available_numerical = [col for col in numerical_cols if col in df.columns]
        
        if len(available_numerical) >= 2:
            corr_matrix = df[available_numerical].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                title='Correlation Heatmap',
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough numerical columns for correlation analysis")
        
        # Multi-dimensional Analysis
        st.markdown("### 🎯 Multi-Dimensional Analysis")
        
        # Check available columns for grouping
        available_group_cols = ['education', 'workclass']
        available_group_cols = [col for col in available_group_cols if col in df.columns]
        
        if len(available_group_cols) >= 2:
            st.write("Income by Education and Work Class")
            
            pivot_data = df.groupby(available_group_cols)['income'].mean().reset_index()
            
            fig = px.sunburst(
                pivot_data,
                path=available_group_cols,
                values='income',
                title=f'Income Hierarchy: {" → ".join(available_group_cols)}',
                color='income',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough categorical columns for multi-dimensional analysis")
        
        # Skills vs Income Analysis
        st.markdown("### 💼 Skills Impact on Income")
        
        # Calculate average income for each skill
        skill_income = {}
        for idx, row in df.iterrows():
            if pd.notna(row['skills']):
                skills = [s.strip() for s in str(row['skills']).split(',')]
                for skill in skills:
                    if skill not in skill_income:
                        skill_income[skill] = []
                    skill_income[skill].append(row['income'])
        
        avg_skill_income = {skill: np.mean(incomes) for skill, incomes in skill_income.items() if len(incomes) > 10}
        if avg_skill_income:
            top_income_skills = dict(sorted(avg_skill_income.items(), key=lambda x: x[1], reverse=True)[:15])
            
            fig = px.bar(
                x=list(top_income_skills.values()),
                y=list(top_income_skills.keys()),
                orientation='h',
                title='Top 15 Highest Paying Skills',
                labels={'x': 'Average Income ($)', 'y': 'Skill'},
                color=list(top_income_skills.values()),
                color_continuous_scale='Plasma'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough skill data for income analysis")
        
        # Education ROI Analysis
        st.markdown("### 🎓 Education Return on Investment")
        edu_stats = df.groupby('education').agg({
            'income': ['mean', 'median', 'std'],
            'age': 'mean'
        }).round(2)
        
        st.dataframe(edu_stats, use_container_width=True)
        
        # Statistical Insights
        st.markdown("### 📈 Key Statistical Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **Income Statistics**
            - Mean: ${df['income'].mean():,.0f}
            - Median: ${df['income'].median():,.0f}
            - Std Dev: ${df['income'].std():,.0f}
            - Range: ${df['income'].min():,.0f} - ${df['income'].max():,.0f}
            """)
        
        with col2:
            st.info(f"""
            **Age Statistics**
            - Mean Age: {df['age'].mean():.1f}
            - Median Age: {df['age'].median():.1f}
            - Std Dev: {df['age'].std():.1f}
            - Range: {df['age'].min()} - {df['age'].max()}
            """)
        
        with col3:
            st.info(f"""
            **Work Statistics**
            - Avg Hours/Week: {df['hours-per-week'].mean():.1f}
            - Median Hours/Week: {df['hours-per-week'].median():.1f}
            - Most Common: {df['hours-per-week'].mode()[0]:.0f} hrs
            """)
    
    # Download option
    st.markdown("---")
    st.markdown("### 💾 Download Analysis Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Dataset (CSV)",
            data=csv,
            file_name="career_guidance_data.csv",
            mime="text/csv"
        )
    
    with col2:
        summary_stats = df.describe().to_csv().encode('utf-8')
        st.download_button(
            label="📊 Download Statistics (CSV)",
            data=summary_stats,
            file_name="dataset_statistics.csv",
            mime="text/csv"
        )
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

# Main app routing
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
    elif st.session_state.page == 'data_analytics':
        data_analytics_page()

if __name__ == "__main__":
    main()