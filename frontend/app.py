import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="EduTrack Pro - Student Management System", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default menu and footer
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Dark Theme Custom CSS with modern design
st.markdown("""
    <style>
    /* Dark background with subtle gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Glass morphism card effect - Dark theme */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
    
    /* Hero Header with dark theme */
    .hero-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
        padding: 50px;
        border-radius: 25px;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-header h1 {
        color: #fff;
        font-size: 56px;
        font-weight: 800;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    
    .hero-header p {
        color: #e0e0e0;
        font-size: 24px;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        color: #a78bfa;
        font-size: 18px;
        margin-top: 10px;
    }

    /* Enhanced button styles - Dark theme */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        height: 3.5em;
        width: 100%;
        border-radius: 15px;
        border: none;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 4px 15px 0 rgba(99, 102, 241, 0.5);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(168, 85, 247, 0.7);
        background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%);
    }

    /* Input field styling - Dark theme */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: #00e5ff;
        font-size: 16px;
        padding: 14px;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }
    
    /* Labels */
    label {
        color: #e0e0e0 !important;
        font-weight: 500 !important;
        font-size: 16px !important;
    }

    /* Tab styling - Dark theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        color: #e0e0e0;
        font-weight: 600;
        padding: 14px 28px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
    }

    /* Metric cards - Dark theme */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px 0 rgba(99, 102, 241, 0.4);
    }
    
    .metric-value {
        font-size: 52px;
        font-weight: 800;
        color: #fff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 18px;
        color: #d1d5db;
        margin-top: 12px;
        font-weight: 500;
    }
    
    .metric-icon {
        font-size: 36px;
        margin-bottom: 10px;
    }

    /* Info card styling */
    .info-card {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366f1;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    .info-card h3 {
        color: #a855f7;
        margin-bottom: 10px;
        font-size: 20px;
    }
    
    .info-card p {
        color: #d1d5db;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Table styling - Dark theme */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(99, 102, 241, 0.2) !important;
    }
    
    .dataframe th {
        background: rgba(99, 102, 241, 0.3) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 10px;
        padding: 15px;
        color: #86efac;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 15px;
        color: #fca5a5;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.15);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 10px;
        padding: 15px;
        color: #fde68a;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 10px;
        padding: 15px;
        color: #93c5fd;
    }
    
    /* Feature card */
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    .feature-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #a855f7;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        color: #d1d5db;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Section headers */
    .section-header {
        color: #fff;
        font-size: 32px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(168, 85, 247, 0.3);
    }
    
    /* Download button custom style */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Hero Header with branding
current_time = datetime.now().strftime("%B %d, %Y")
st.markdown(f"""
<div class="hero-header">
    <h1>🎓 Multicloud Devops </h1>
    <p>Advanced Student Management & Cloud Platform</p>
    <div class="hero-subtitle">📅 {current_time} | 🌐 Powered by Spring Boot & Streamlit</div>
</div>
""", unsafe_allow_html=True)

# API URL
API_URL = os.environ.get("API_URL", "http://10.0.2.116:8080")

# Tabs with emojis and clear names
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add New Student", 
    "🔍 Search & Delete", 
    "📋 View All Students", 
    "✏️ Update Records", 
    "📊 Analytics Dashboard"
])

# --- Tab 1: Add Student ---
with tab1:
    st.markdown('<div class="section-header">➕ Register New Student</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📝 Student Registration Form</h3>
            <p>Enter the student's details below to add them to the database. All fields are required.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_student_form", clear_on_submit=True):
            name = st.text_input("👤 Student Full Name", placeholder="e.g., John Doe")
            age = st.number_input("🎂 Age", min_value=1, max_value=100, value=18, help="Enter age between 1-100")
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                submit_button = st.form_submit_button("🚀 Add Student", use_container_width=True)
            
            if submit_button:
                if name:
                    try:
                        response = requests.post(f"{API_URL}/student/post", json={"name": name, "age": age})
                        if response.status_code == 200:
                            st.success(f"✅ Success! Student '{name}' has been added to the database!")
                            st.balloons()
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"🔌 Connection Error: Unable to reach the server. Please check if the backend is running.\n\nDetails: {e}")
                else:
                    st.warning("⚠️ Please enter the student's name before submitting.")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Quick Tips</div>
            <div class="feature-desc">
                • Use unique student names<br>
                • Age must be between 1-100<br>
                • Form clears after successful submission<br>
                • Check the "View All" tab to see added students
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">System Features</div>
            <div class="feature-desc">
                • Real-time database updates<br>
                • Instant validation<br>
                • Automatic data backup<br>
                • Secure data storage
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: Search Student ---
with tab2:
    st.markdown('<div class="section-header">🔍 Search & Manage Students</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🔎 Student Lookup</h3>
            <p>Search for a student by their name to view details or remove them from the system.</p>
        </div>
        """, unsafe_allow_html=True)
        
        search_name = st.text_input("👤 Enter Student Name", placeholder="Type the exact student name...")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            search_btn = st.button("🔎 Search", use_container_width=True)
        with col_btn2:
            delete_btn = st.button("🗑️ Delete", use_container_width=True, type="secondary")
        
        if search_btn and search_name:
            try:
                response = requests.get(f"{API_URL}/student/get/{search_name}")
                if response.status_code == 200:
                    student = response.json()
                    st.markdown("""
                    <div class="info-card">
                        <h3>✅ Student Found!</h3>
                        <p>Here are the details for the student you searched:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-icon">👤</div>
                            <div class="metric-value">{student.get('name', 'N/A')}</div>
                            <div class="metric-label">Student Name</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_info2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-icon">🎂</div>
                            <div class="metric-value">{student.get('age', 'N/A')}</div>
                            <div class="metric-label">Age (Years)</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"⚠️ No student found with the name '{search_name}'. Please check the spelling and try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"🔌 Connection Error: {e}")
        
        if delete_btn and search_name:
            try:
                response = requests.delete(f"{API_URL}/student/delete/{search_name}")
                if response.status_code == 200:
                    st.success(f"✅ Student '{search_name}' has been successfully removed from the database!")
                    st.snow()
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"🔌 Connection Error: {e}")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">ℹ️</div>
            <div class="feature-title">Search Instructions</div>
            <div class="feature-desc">
                1️⃣ Enter the exact student name<br>
                2️⃣ Click "Search" to view details<br>
                3️⃣ Click "Delete" to remove student<br>
                4️⃣ Deletion is permanent - be careful!
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <div class="feature-title">Important Notes</div>
            <div class="feature-desc">
                • Names are case-sensitive<br>
                • Deleted records cannot be recovered<br>
                • Use "View All" to see available names<br>
                • Contact admin for bulk operations
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 3: List Students ---
with tab3:
    st.markdown('<div class="section-header">📋 Complete Student Directory</div>', unsafe_allow_html=True)
    
    col_refresh, col_count, col_empty = st.columns([1, 2, 2])
    with col_refresh:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    try:
        response = requests.get(f"{API_URL}/student/all")
        if response.status_code == 200:
            students = response.json()
            if students:
                with col_count:
                    st.info(f"📊 Total Students: **{len(students)}**")
                
                student_data = [{
                    "👤 Name": s.get("name", "N/A"), 
                    "🎂 Age": s.get("age", "N/A")
                } for s in students]
                df = pd.DataFrame(student_data)
                
                st.markdown("""
                <div class="info-card">
                    <h3>📊 Student Database</h3>
                    <p>Below is the complete list of all registered students in the system.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display with custom styling
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=450
                )
                
                # Download section
                st.markdown("---")
                col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 2])
                with col_dl1:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Export to CSV",
                        data=csv,
                        file_name=f"students_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                with col_dl2:
                    st.markdown("""
                    <div style="padding: 10px; color: #d1d5db;">
                        💾 Download the complete student list as a CSV file for offline access
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No students found in the database. Add some students using the 'Add New Student' tab!")
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">Getting Started</div>
                    <div class="feature-desc">
                        Navigate to the "Add New Student" tab to register your first student!
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Failed to retrieve student list from the server.")
    except requests.exceptions.RequestException as e:
        st.error(f"🔌 Connection Error: Unable to connect to the backend server.\n\nDetails: {e}")

# --- Tab 4: Update Student ---
with tab4:
    st.markdown('<div class="section-header">✏️ Update Student Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📝 Student Record Update Form</h3>
            <p>Modify existing student information. Enter the current name and provide new details.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("update_student_form"):
            old_name = st.text_input("🔍 Current Student Name", placeholder="Enter the existing name...")
            st.markdown("---")
            st.markdown("**New Information:**")
            new_name = st.text_input("👤 New Name", placeholder="Enter updated name...")
            new_age = st.number_input("🎂 New Age", min_value=1, max_value=100, value=18)
            
            col_upd1, col_upd2 = st.columns([1, 3])
            with col_upd1:
                update_button = st.form_submit_button("🔄 Update Record", use_container_width=True)
            
            if update_button:
                if old_name and new_name:
                    try:
                        response = requests.put(
                            f"{API_URL}/student/update/{old_name}", 
                            json={"name": new_name, "age": new_age}
                        )
                        if response.status_code == 200:
                            st.success(f"✅ Success! Student '{old_name}' has been updated to '{new_name}' (Age: {new_age})")
                            st.balloons()
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"🔌 Connection Error: {e}")
                else:
                    st.warning("⚠️ Please fill in all required fields (current name and new name).")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📖</div>
            <div class="feature-title">Update Guide</div>
            <div class="feature-desc">
                1️⃣ Enter the current student name<br>
                2️⃣ Provide the new name<br>
                3️⃣ Set the new age<br>
                4️⃣ Click "Update Record" to save
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Pro Tips</div>
            <div class="feature-desc">
                • Current name must match exactly<br>
                • You can update name, age, or both<br>
                • Changes are saved immediately<br>
                • Check "View All" to verify updates
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 5: Analytics ---
with tab5:
    st.markdown('<div class="section-header">📊 Student Analytics & Insights</div>', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_URL}/student/all")
        if response.status_code == 200:
            students = response.json()
            if students:
                df = pd.DataFrame(students)
                
                # Key Metrics Section
                st.markdown("### 📈 Key Performance Indicators")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">👥</div>
                        <div class="metric-value">{len(students)}</div>
                        <div class="metric-label">Total Students</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    avg_age = df['age'].mean()
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">📊</div>
                        <div class="metric-value">{avg_age:.1f}</div>
                        <div class="metric-label">Average Age</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    min_age = df['age'].min()
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🌱</div>
                        <div class="metric-value">{min_age}</div>
                        <div class="metric-label">Youngest Student</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    max_age = df['age'].max()
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-icon">🎓</div>
                        <div class="metric-value">{max_age}</div>
                        <div class="metric-label">Oldest Student</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Charts Section
                st.markdown("### 📉 Visual Analytics")
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    # Age Distribution Histogram
                    fig1 = px.histogram(
                        df, 
                        x='age', 
                        nbins=20,
                        title='📊 Age Distribution Analysis',
                        color_discrete_sequence=['#6366f1'],
                        labels={'age': 'Age (Years)', 'count': 'Number of Students'}
                    )
                    fig1.update_layout(
                        plot_bgcolor='rgba(15, 12, 41, 0.5)',
                        paper_bgcolor='rgba(255, 255, 255, 0.05)',
                        font=dict(color='#e0e0e0', size=12),
                        title_font=dict(size=18, color='#fff'),
                        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col_chart2:
                    # Age Range Distribution (Pie Chart)
                    age_ranges = pd.cut(df['age'], bins=[0, 18, 25, 35, 50, 100], 
                                       labels=['Under 18 👶', '18-25 🎓', '26-35 💼', '36-50 👔', '50+ 🏆'])
                    age_range_counts = age_ranges.value_counts()
                    
                    fig2 = px.pie(
                        values=age_range_counts.values,
                        names=age_range_counts.index,
                        title='🎯 Age Group Distribution',
                        color_discrete_sequence=px.colors.sequential.Purples_r,
                        hole=0.4
                    )
                    fig2.update_layout(
                        plot_bgcolor='rgba(15, 12, 41, 0.5)',
                        paper_bgcolor='rgba(255, 255, 255, 0.05)',
                        font=dict(color='#e0e0e0', size=12),
                        title_font=dict(size=18, color='#fff')
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Top Students Section
                st.markdown("### 🏆 Top 10 Oldest Students")
                top_10 = df.nlargest(10, 'age')[['name', 'age']]
                
                fig3 = px.bar(
                    top_10,
                    x='name',
                    y='age',
                    title='📊 Oldest Students Ranking',
                    color='age',
                    color_continuous_scale='Purples',
                    labels={'name': 'Student Name', 'age': 'Age (Years)'}
                )
                fig3.update_layout(
                    plot_bgcolor='rgba(15, 12, 41, 0.5)',
                    paper_bgcolor='rgba(255, 255, 255, 0.05)',
                    font=dict(color='#e0e0e0', size=12),
                    title_font=dict(size=18, color='#fff'),
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                    showlegend=False
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Statistics Summary
                st.markdown("### 📋 Statistical Summary")
                col_stat1, col_stat2 = st.columns(2)
                
                with col_stat1:
                    st.markdown("""
                    <div class="info-card">
                        <h3>📊 Age Statistics</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    stats_df = pd.DataFrame({
                        'Metric': ['Mean', 'Median', 'Mode', 'Std Dev'],
                        'Value': [
                            f"{df['age'].mean():.2f}",
                            f"{df['age'].median():.2f}",
                            f"{df['age'].mode()[0] if not df['age'].mode().empty else 'N/A'}",
                            f"{df['age'].std():.2f}"
                        ]
                    })
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
                
                with col_stat2:
                    st.markdown("""
                    <div class="info-card">
                        <h3>🎯 Quick Insights</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    insights = f"""
                    - **Total Records:** {len(students)} students
                    - **Age Range:** {min_age} - {max_age} years
                    - **Most Common Age:** {df['age'].mode()[0] if not df['age'].mode().empty else 'N/A'} years
                    - **Data Quality:** ✅ Complete
                    """
                    st.markdown(insights)
                
            else:
                st.info("ℹ️ No data available for analytics. Add some students first!")
                st.markdown("""
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Analytics Awaiting Data</div>
                    <div class="feature-desc">
                        Once you add students to the database, this dashboard will display:<br>
                        • Age distribution charts<br>
                        • Statistical analysis<br>
                        • Top student rankings<br>
                        • Demographic insights
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Failed to retrieve data for analytics.")
    except requests.exceptions.RequestException as e:
        st.error(f"🔌 Connection Error: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 30px; 
            background: rgba(255, 255, 255, 0.05); border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);">
    <p style="color: #a855f7; font-size: 20px; font-weight: 600; margin-bottom: 10px;">
        🎓 EduTrack Pro - Student Management System
    </p>
    <p style="color: rgba(255,255,255,0.6); font-size: 14px;">
        Made with ❤️ using Spring Boot & Streamlit | 
        🚀 MultiCloudDevOps by Veera NareshIT | 
        📅 {current_time}
    </p>
    <p style="color: rgba(255,255,255,0.4); font-size: 12px; margin-top: 10px;">
        Version 2.0 | © 2025 All Rights Reserved
    </p>
</div>
""".replace("{current_time}", current_time), unsafe_allow_html=True)
