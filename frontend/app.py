import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduTrack Pro - Student Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# MODERN SAAS THEME
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,102,241,0.08),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(14,165,233,0.07),
            transparent 30%
        ),
        #f5f7fb;

    color: #172033;
    font-family: "Inter", "Segoe UI", sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Hide Streamlit menu/footer */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =========================================================
   HERO
========================================================= */

.hero-header {

    background:
        linear-gradient(
            135deg,
            #111827 0%,
            #1e293b 45%,
            #312e81 100%
        );

    padding: 48px 40px;

    border-radius: 28px;

    text-align: center;

    margin-bottom: 35px;

    position: relative;

    overflow: hidden;

    box-shadow:
        0 20px 50px rgba(15,23,42,0.20);

    border: 1px solid rgba(255,255,255,0.08);
}

.hero-header::before {

    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    top: -230px;
    right: -100px;

    background: rgba(99,102,241,0.25);

    border-radius: 50%;

    filter: blur(15px);
}

.hero-header::after {

    content: "";

    position: absolute;

    width: 320px;
    height: 320px;

    bottom: -200px;
    left: -80px;

    background: rgba(14,165,233,0.18);

    border-radius: 50%;

    filter: blur(15px);
}

.hero-header h1 {

    color: white;

    font-size: 50px;

    font-weight: 800;

    letter-spacing: -1.5px;

    margin-bottom: 10px;

    position: relative;

    z-index: 2;
}

.hero-header p {

    color: #cbd5e1;

    font-size: 20px;

    margin-bottom: 12px;

    position: relative;

    z-index: 2;
}

.hero-subtitle {

    color: #93c5fd;

    font-size: 14px;

    position: relative;

    z-index: 2;
}


/* =========================================================
   TABS
========================================================= */

.stTabs {
    margin-top: 15px;
}

.stTabs [data-baseweb="tab-list"] {

    background: white;

    padding: 8px;

    gap: 6px;

    border-radius: 16px;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 4px 15px rgba(15,23,42,0.06);
}

.stTabs [data-baseweb="tab"] {

    color: #64748b;

    font-weight: 600;

    font-size: 14px;

    padding: 12px 20px;

    border-radius: 10px;

    transition: all 0.2s ease;
}

.stTabs [data-baseweb="tab"]:hover {

    background: #f1f5f9;

    color: #334155;
}

.stTabs [aria-selected="true"] {

    background: #4f46e5;

    color: white !important;

    box-shadow:
        0 4px 12px rgba(79,70,229,0.25);
}


/* =========================================================
   SECTION HEADERS
========================================================= */

.section-header {

    color: #111827;

    font-size: 30px;

    font-weight: 800;

    letter-spacing: -0.7px;

    margin: 25px 0;
}


/* =========================================================
   INFO CARDS
========================================================= */

.info-card {

    background: white;

    border-radius: 18px;

    padding: 22px;

    margin: 18px 0;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}

.info-card h3 {

    color: #111827;

    margin-bottom: 8px;

    font-size: 19px;
}

.info-card p {

    color: #64748b;

    line-height: 1.6;

    font-size: 14px;
}


/* =========================================================
   FEATURE CARDS
========================================================= */

.feature-card {

    background: white;

    padding: 24px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    margin: 15px 0;

    transition: all 0.25s ease;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.05);
}

.feature-card:hover {

    transform: translateY(-4px);

    border-color: #c7d2fe;

    box-shadow:
        0 12px 30px rgba(79,70,229,0.12);
}

.feature-icon {

    font-size: 30px;

    margin-bottom: 10px;
}

.feature-title {

    color: #4338ca;

    font-size: 17px;

    font-weight: 700;

    margin-bottom: 8px;
}

.feature-desc {

    color: #64748b;

    font-size: 14px;

    line-height: 1.7;
}


/* =========================================================
   METRIC CARDS
========================================================= */

.metric-card {

    background: white;

    padding: 25px 20px;

    border-radius: 20px;

    text-align: center;

    border: 1px solid #e5e7eb;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);

    transition: all 0.25s ease;
}

.metric-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 15px 35px rgba(79,70,229,0.12);

    border-color: #c7d2fe;
}

.metric-icon {

    font-size: 30px;

    margin-bottom: 8px;
}

.metric-value {

    font-size: 38px;

    font-weight: 800;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #0284c7
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.metric-label {

    color: #64748b;

    font-size: 14px;

    font-weight: 600;

    margin-top: 5px;
}


/* =========================================================
   INPUTS
========================================================= */

.stTextInput input,
.stNumberInput input {

    background: white !important;

    color: #111827 !important;

    border: 1px solid #dbe2ea !important;

    border-radius: 12px !important;

    padding: 12px !important;

    font-size: 15px !important;

    transition: all 0.2s ease;
}

.stTextInput input:focus,
.stNumberInput input:focus {

    border-color: #6366f1 !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.12) !important;
}

.stTextInput input::placeholder {

    color: #94a3b8 !important;
}


/* =========================================================
   LABELS
========================================================= */

label {

    color: #334155 !important;

    font-weight: 600 !important;

    font-size: 14px !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #6366f1
        );

    color: white;

    border: none;

    border-radius: 12px;

    min-height: 45px;

    font-weight: 700;

    font-size: 14px;

    box-shadow:
        0 5px 15px rgba(79,70,229,0.20);

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(79,70,229,0.30);

    background:
        linear-gradient(
            135deg,
            #4338ca,
            #4f46e5
        );
}


/* =========================================================
   DOWNLOAD BUTTON
========================================================= */

.stDownloadButton > button {

    background:
        linear-gradient(
            135deg,
            #059669,
            #10b981
        );

    color: white;

    border: none;

    border-radius: 12px;

    font-weight: 700;

    padding: 10px 20px;

    box-shadow:
        0 5px 15px rgba(16,185,129,0.20);
}

.stDownloadButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(16,185,129,0.30);
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;

    border: 1px solid #e2e8f0;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.05);
}


/* =========================================================
   ALERTS
========================================================= */

.stSuccess {

    border-radius: 12px !important;

    border-left: 4px solid #10b981 !important;
}

.stError {

    border-radius: 12px !important;

    border-left: 4px solid #ef4444 !important;
}

.stWarning {

    border-radius: 12px !important;

    border-left: 4px solid #f59e0b !important;
}

.stInfo {

    border-radius: 12px !important;

    border-left: 4px solid #3b82f6 !important;
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {

    border: none;

    border-top: 1px solid #e2e8f0;

    margin: 30px 0;
}


/* =========================================================
   FOOTER
========================================================= */

.modern-footer {

    text-align: center;

    margin-top: 50px;

    padding: 30px;

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 20px;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.05);
}

.modern-footer .title {

    color: #4f46e5;

    font-size: 20px;

    font-weight: 800;
}

.modern-footer .subtitle {

    color: #64748b;

    font-size: 14px;

    margin-top: 8px;
}


/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f5f9;
}

::-webkit-scrollbar-thumb {

    background: #cbd5e1;

    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================

current_time = datetime.now().strftime("%B %d, %Y")

st.markdown(f"""
<div class="hero-header">

    <h1>🎓 EduTrack Pro</h1>

    <p>
        Student Management & Analytics Platform
    </p>

    <div class="hero-subtitle">
        ☁️ Multicloud DevOps
        &nbsp; • &nbsp;
        🚀 Spring Boot API
        &nbsp; • &nbsp;
        📊 Streamlit Dashboard
        &nbsp; • &nbsp;
        📅 {current_time}
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = os.environ.get("API_URL", "").rstrip("/")

if not API_URL:

    st.warning(
        "⚠️ API_URL environment variable is not configured. "
        "The application cannot connect to the Spring Boot backend."
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ Add Student",
    "🔍 Search & Delete",
    "📋 All Students",
    "✏️ Update Records",
    "📊 Analytics"
])


# ============================================================
# TAB 1 - ADD STUDENT
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-header">➕ Register New Student</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    # --------------------------------------------------------
    # FORM
    # --------------------------------------------------------

    with col1:

        st.markdown("""
        <div class="info-card">

            <h3>📝 Student Registration</h3>

            <p>
                Enter student information below to create a
                new student record in the database.
            </p>

        </div>
        """, unsafe_allow_html=True)

        with st.form(
            "add_student_form",
            clear_on_submit=True
        ):

            name = st.text_input(
                "👤 Student Full Name",
                placeholder="e.g. John Doe"
            )

            age = st.number_input(
                "🎂 Age",
                min_value=1,
                max_value=100,
                value=18,
                step=1
            )

            col_btn1, col_btn2 = st.columns([1, 3])

            with col_btn1:

                submit_button = st.form_submit_button(
                    "🚀 Add Student",
                    use_container_width=True
                )

            if submit_button:

                if not API_URL:

                    st.error(
                        "❌ API_URL is not configured."
                    )

                elif name.strip():

                    try:

                        response = requests.post(
                            f"{API_URL}/student/post",
                            json={
                                "name": name.strip(),
                                "age": age
                            },
                            timeout=10
                        )

                        if response.status_code in [200, 201]:

                            st.success(
                                f"✅ Student '{name}' "
                                "has been added successfully!"
                            )

                            st.balloons()

                        else:

                            st.error(
                                f"❌ Backend Error: "
                                f"{response.text}"
                            )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            "🔌 Connection Error: "
                            f"{e}"
                        )

                else:

                    st.warning(
                        "⚠️ Please enter the student's name."
                    )

    # --------------------------------------------------------
    # SIDE INFORMATION
    # --------------------------------------------------------

    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                💡
            </div>

            <div class="feature-title">
                Quick Tips
            </div>

            <div class="feature-desc">

                • Use a valid student name<br>
                • Age must be between 1-100<br>
                • Data is stored in MySQL<br>
                • Changes are immediately available<br>
                • Use View All to verify records

            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                🚀
            </div>

            <div class="feature-title">
                Platform
            </div>

            <div class="feature-desc">

                ⚙️ Spring Boot REST API<br>
                🗄️ MySQL Database<br>
                ☁️ AWS Cloud Infrastructure<br>
                📊 Streamlit Dashboard<br>
                🐳 Docker & Kubernetes

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# TAB 2 - SEARCH & DELETE
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-header">🔍 Search & Manage Students</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:

        st.markdown("""
        <div class="info-card">

            <h3>🔎 Student Lookup</h3>

            <p>
                Search for a student by name or remove
                an existing record.
            </p>

        </div>
        """, unsafe_allow_html=True)

        search_name = st.text_input(
            "👤 Student Name",
            placeholder="Enter exact student name..."
        )

        col_btn1, col_btn2, col_btn3 = st.columns(
            [1, 1, 2]
        )

        with col_btn1:

            search_btn = st.button(
                "🔎 Search",
                use_container_width=True
            )

        with col_btn2:

            delete_btn = st.button(
                "🗑️ Delete",
                use_container_width=True,
                type="secondary"
            )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        if search_btn:

            if not search_name.strip():

                st.warning(
                    "⚠️ Please enter a student name."
                )

            elif not API_URL:

                st.error(
                    "❌ API_URL is not configured."
                )

            else:

                try:

                    response = requests.get(
                        f"{API_URL}/student/get/{search_name.strip()}",
                        timeout=10
                    )

                    if response.status_code == 200:

                        student = response.json()

                        st.markdown("""
                        <div class="info-card">

                            <h3>✅ Student Found</h3>

                            <p>
                                Student information retrieved
                                successfully.
                            </p>

                        </div>
                        """, unsafe_allow_html=True)

                        col_info1, col_info2 = st.columns(2)

                        with col_info1:

                            st.markdown(f"""
                            <div class="metric-card">

                                <div class="metric-icon">
                                    👤
                                </div>

                                <div class="metric-value"
                                     style="font-size:26px;">
                                    {student.get('name', 'N/A')}
                                </div>

                                <div class="metric-label">
                                    Student Name
                                </div>

                            </div>
                            """, unsafe_allow_html=True)

                        with col_info2:

                            st.markdown(f"""
                            <div class="metric-card">

                                <div class="metric-icon">
                                    🎂
                                </div>

                                <div class="metric-value">
                                    {student.get('age', 'N/A')}
                                </div>

                                <div class="metric-label">
                                    Age
                                </div>

                            </div>
                            """, unsafe_allow_html=True)

                    elif response.status_code == 404:

                        st.warning(
                            f"⚠️ No student found with "
                            f"the name '{search_name}'."
                        )

                    else:

                        st.error(
                            f"❌ Backend Error: "
                            f"{response.text}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"🔌 Connection Error: {e}"
                    )

        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        if delete_btn:

            if not search_name.strip():

                st.warning(
                    "⚠️ Enter the student name to delete."
                )

            elif not API_URL:

                st.error(
                    "❌ API_URL is not configured."
                )

            else:

                try:

                    response = requests.delete(
                        f"{API_URL}/student/delete/{search_name.strip()}",
                        timeout=10
                    )

                    if response.status_code in [200, 204]:

                        st.success(
                            f"✅ Student '{search_name}' "
                            "was deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"❌ Delete failed: "
                            f"{response.text}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"🔌 Connection Error: {e}"
                    )

    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                🔍
            </div>

            <div class="feature-title">
                Search Instructions
            </div>

            <div class="feature-desc">

                1️⃣ Enter the exact student name<br>
                2️⃣ Click Search<br>
                3️⃣ View student details<br>
                4️⃣ Use Delete when required

            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                ⚠️
            </div>

            <div class="feature-title">
                Important
            </div>

            <div class="feature-desc">

                • Names may be case-sensitive<br>
                • Deleted records cannot be recovered<br>
                • Verify the name before deleting<br>
                • Use All Students to verify records

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# TAB 3 - ALL STUDENTS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-header">📋 Student Directory</div>',
        unsafe_allow_html=True
    )

    col_refresh, col_count, col_space = st.columns(
        [1, 2, 2]
    )

    with col_refresh:

        if st.button(
            "🔄 Refresh",
            use_container_width=True
        ):

            st.rerun()

    try:

        if not API_URL:

            st.error(
                "❌ API_URL is not configured."
            )

        else:

            response = requests.get(
                f"{API_URL}/student/all",
                timeout=10
            )

            if response.status_code == 200:

                students = response.json()

                if students:

                    with col_count:

                        st.info(
                            f"📊 Total Students: "
                            f"**{len(students)}**"
                        )

                    student_data = [

                        {
                            "👤 Name": student.get(
                                "name",
                                "N/A"
                            ),

                            "🎂 Age": student.get(
                                "age",
                                "N/A"
                            )

                        }

                        for student in students
                    ]

                    df = pd.DataFrame(
                        student_data
                    )

                    st.markdown("""
                    <div class="info-card">

                        <h3>📊 Student Database</h3>

                        <p>
                            Complete list of students
                            registered in the system.
                        </p>

                    </div>
                    """, unsafe_allow_html=True)

                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=450,
                        hide_index=True
                    )

                    # ------------------------------------------------
                    # CSV DOWNLOAD
                    # ------------------------------------------------

                    st.markdown("---")

                    col_dl1, col_dl2 = st.columns(
                        [1, 3]
                    )

                    with col_dl1:

                        csv = df.to_csv(
                            index=False
                        ).encode("utf-8")

                        st.download_button(
                            label="📥 Export CSV",
                            data=csv,
                            file_name=(
                                "students_data_"
                                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                            ),
                            mime="text/csv",
                            use_container_width=True
                        )

                    with col_dl2:

                        st.markdown("""
                        <div style="
                            padding:12px;
                            color:#64748b;
                        ">

                            💾 Download the complete
                            student directory for
                            offline access.

                        </div>
                        """, unsafe_allow_html=True)

                else:

                    st.info(
                        "ℹ️ No students found. "
                        "Add your first student using "
                        "the Add Student tab."
                    )

            else:

                st.error(
                    f"❌ Failed to retrieve students. "
                    f"HTTP {response.status_code}"
                )

    except requests.exceptions.RequestException as e:

        st.error(
            f"🔌 Backend connection error: {e}"
        )


# ============================================================
# TAB 4 - UPDATE STUDENT
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-header">✏️ Update Student Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])

    with col1:

        st.markdown("""
        <div class="info-card">

            <h3>📝 Update Student Record</h3>

            <p>
                Enter the current student name and
                provide the updated information.
            </p>

        </div>
        """, unsafe_allow_html=True)

        with st.form(
            "update_student_form"
        ):

            old_name = st.text_input(
                "🔍 Current Student Name",
                placeholder="Enter existing name..."
            )

            st.markdown("---")

            st.markdown(
                "**New Information**"
            )

            new_name = st.text_input(
                "👤 New Name",
                placeholder="Enter updated name..."
            )

            new_age = st.number_input(
                "🎂 New Age",
                min_value=1,
                max_value=100,
                value=18,
                step=1
            )

            col_upd1, col_upd2 = st.columns(
                [1, 3]
            )

            with col_upd1:

                update_button = st.form_submit_button(
                    "🔄 Update",
                    use_container_width=True
                )

            if update_button:

                if not old_name.strip():

                    st.warning(
                        "⚠️ Enter the current student name."
                    )

                elif not new_name.strip():

                    st.warning(
                        "⚠️ Enter the new student name."
                    )

                elif not API_URL:

                    st.error(
                        "❌ API_URL is not configured."
                    )

                else:

                    try:

                        response = requests.put(
                            f"{API_URL}/student/update/{old_name.strip()}",
                            json={
                                "name": new_name.strip(),
                                "age": new_age
                            },
                            timeout=10
                        )

                        if response.status_code == 200:

                            st.success(
                                f"✅ '{old_name}' updated "
                                f"to '{new_name}' "
                                f"(Age: {new_age})"
                            )

                            st.balloons()

                        else:

                            st.error(
                                f"❌ Update failed: "
                                f"{response.text}"
                            )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"🔌 Connection Error: {e}"
                        )

    with col2:

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                📖
            </div>

            <div class="feature-title">
                Update Guide
            </div>

            <div class="feature-desc">

                1️⃣ Enter current name<br>
                2️⃣ Enter new name<br>
                3️⃣ Enter new age<br>
                4️⃣ Click Update

            </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">

            <div class="feature-icon">
                ⚡
            </div>

            <div class="feature-title">
                Pro Tips
            </div>

            <div class="feature-desc">

                • Current name must match<br>
                • Changes are saved immediately<br>
                • Verify using All Students<br>
                • Backend validates the request

            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# TAB 5 - ANALYTICS
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-header">📊 Student Analytics</div>',
        unsafe_allow_html=True
    )

    try:

        if not API_URL:

            st.error(
                "❌ API_URL is not configured."
            )

        else:

            response = requests.get(
                f"{API_URL}/student/all",
                timeout=10
            )

            if response.status_code == 200:

                students = response.json()

                if students:

                    df = pd.DataFrame(students)

                    # Ensure age is numeric
                    df["age"] = pd.to_numeric(
                        df["age"],
                        errors="coerce"
                    )

                    df = df.dropna(
                        subset=["age"]
                    )

                    # =================================================
                    # KPI SECTION
                    # =================================================

                    st.markdown(
                        "### 📈 Key Metrics"
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    # Total
                    with col1:

                        st.markdown(f"""
                        <div class="metric-card">

                            <div class="metric-icon">
                                👥
                            </div>

                            <div class="metric-value">
                                {len(df)}
                            </div>

                            <div class="metric-label">
                                Total Students
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                    # Average
                    with col2:

                        avg_age = df["age"].mean()

                        st.markdown(f"""
                        <div class="metric-card">

                            <div class="metric-icon">
                                📊
                            </div>

                            <div class="metric-value">
                                {avg_age:.1f}
                            </div>

                            <div class="metric-label">
                                Average Age
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                    # Youngest
                    with col3:

                        min_age = df["age"].min()

                        st.markdown(f"""
                        <div class="metric-card">

                            <div class="metric-icon">
                                🌱
                            </div>

                            <div class="metric-value">
                                {int(min_age)}
                            </div>

                            <div class="metric-label">
                                Youngest
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                    # Oldest
                    with col4:

                        max_age = df["age"].max()

                        st.markdown(f"""
                        <div class="metric-card">

                            <div class="metric-icon">
                                🎓
                            </div>

                            <div class="metric-value">
                                {int(max_age)}
                            </div>

                            <div class="metric-label">
                                Oldest
                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # =================================================
                    # CHARTS
                    # =================================================

                    st.markdown(
                        "### 📉 Visual Analytics"
                    )

                    col_chart1, col_chart2 = st.columns(2)

                    # -------------------------------------------------
                    # HISTOGRAM
                    # -------------------------------------------------

                    with col_chart1:

                        fig1 = px.histogram(
                            df,
                            x="age",
                            nbins=20,
                            title="📊 Age Distribution",
                            labels={
                                "age": "Age (Years)",
                                "count": "Students"
                            }
                        )

                        fig1.update_layout(

                            plot_bgcolor="white",

                            paper_bgcolor="white",

                            font=dict(
                                color="#334155",
                                size=12
                            ),

                            title_font=dict(
                                size=18,
                                color="#111827"
                            ),

                            xaxis=dict(
                                gridcolor="#e2e8f0"
                            ),

                            yaxis=dict(
                                gridcolor="#e2e8f0"
                            ),

                            margin=dict(
                                l=20,
                                r=20,
                                t=60,
                                b=20
                            )
                        )

                        st.plotly_chart(
                            fig1,
                            use_container_width=True
                        )

                    # -------------------------------------------------
                    # PIE CHART
                    # -------------------------------------------------

                    with col_chart2:

                        age_ranges = pd.cut(
                            df["age"],
                            bins=[
                                0,
                                18,
                                25,
                                35,
                                50,
                                100
                            ],
                            labels=[
                                "Under 18",
                                "18-25",
                                "26-35",
                                "36-50",
                                "50+"
                            ]
                        )

                        age_range_counts = (
                            age_ranges
                            .value_counts()
                            .sort_index()
                        )

                        fig2 = px.pie(
                            values=age_range_counts.values,
                            names=age_range_counts.index,
                            title="🎯 Age Group Distribution",
                            hole=0.45
                        )

                        fig2.update_layout(

                            plot_bgcolor="white",

                            paper_bgcolor="white",

                            font=dict(
                                color="#334155",
                                size=12
                            ),

                            title_font=dict(
                                size=18,
                                color="#111827"
                            ),

                            margin=dict(
                                l=20,
                                r=20,
                                t=60,
                                b=20
                            )
                        )

                        st.plotly_chart(
                            fig2,
                            use_container_width=True
                        )

                    # =================================================
                    # TOP STUDENTS
                    # =================================================

                    st.markdown(
                        "### 🏆 Oldest Students"
                    )

                    top_10 = (
                        df
                        .nlargest(
                            10,
                            "age"
                        )
                        [["name", "age"]]
                    )

                    fig3 = px.bar(
                        top_10,
                        x="name",
                        y="age",
                        title="📊 Top 10 Oldest Students",
                        labels={
                            "name": "Student",
                            "age": "Age"
                        }
                    )

                    fig3.update_layout(

                        plot_bgcolor="white",

                        paper_bgcolor="white",

                        font=dict(
                            color="#334155",
                            size=12
                        ),

                        title_font=dict(
                            size=18,
                            color="#111827"
                        ),

                        xaxis=dict(
                            gridcolor="#e2e8f0"
                        ),

                        yaxis=dict(
                            gridcolor="#e2e8f0"
                        ),

                        showlegend=False,

                        margin=dict(
                            l=20,
                            r=20,
                            t=60,
                            b=20
                        )
                    )

                    st.plotly_chart(
                        fig3,
                        use_container_width=True
                    )

                    # =================================================
                    # STATISTICS
                    # =================================================

                    st.markdown(
                        "### 📋 Statistical Summary"
                    )

                    col_stat1, col_stat2 = st.columns(2)

                    # -------------------------------------------------
                    # STATISTICS TABLE
                    # -------------------------------------------------

                    with col_stat1:

                        st.markdown("""
                        <div class="info-card">

                            <h3>
                                📊 Age Statistics
                            </h3>

                        </div>
                        """, unsafe_allow_html=True)

                        mode_value = (
                            df["age"].mode()[0]
                            if not df["age"].mode().empty
                            else "N/A"
                        )

                        stats_df = pd.DataFrame({

                            "Metric": [
                                "Mean",
                                "Median",
                                "Mode",
                                "Std Dev",
                                "Minimum",
                                "Maximum"
                            ],

                            "Value": [

                                f"{df['age'].mean():.2f}",

                                f"{df['age'].median():.2f}",

                                f"{mode_value}",

                                f"{df['age'].std():.2f}",

                                f"{df['age'].min():.0f}",

                                f"{df['age'].max():.0f}"
                            ]
                        })

                        st.dataframe(
                            stats_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    # -------------------------------------------------
                    # INSIGHTS
                    # -------------------------------------------------

                    with col_stat2:

                        st.markdown("""
                        <div class="info-card">

                            <h3>
                                🎯 Quick Insights
                            </h3>

                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="feature-card">

                            <div class="feature-desc">

                                👥 <b>Total Records:</b>
                                {len(df)} students

                                <br><br>

                                📅 <b>Age Range:</b>
                                {int(df["age"].min())}
                                -
                                {int(df["age"].max())} years

                                <br><br>

                                📊 <b>Average Age:</b>
                                {df["age"].mean():.1f} years

                                <br><br>

                                🔥 <b>Most Common Age:</b>
                                {mode_value} years

                                <br><br>

                                ✅ <b>Data Status:</b>
                                Complete

                            </div>

                        </div>
                        """, unsafe_allow_html=True)

                else:

                    st.info(
                        "ℹ️ No student data available "
                        "for analytics."
                    )

                    st.markdown("""
                    <div class="feature-card">

                        <div class="feature-icon">
                            📊
                        </div>

                        <div class="feature-title">
                            Analytics Awaiting Data
                        </div>

                        <div class="feature-desc">

                            Add students to the database
                            and this dashboard will
                            automatically generate:

                            <br><br>

                            📈 Age distribution<br>
                            🎯 Age groups<br>
                            📊 Statistics<br>
                            🏆 Student rankings

                        </div>

                    </div>
                    """, unsafe_allow_html=True)

            else:

                st.error(
                    "❌ Failed to retrieve analytics data."
                )

    except requests.exceptions.RequestException as e:

        st.error(
            f"🔌 Backend connection error: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(f"""
<div class="modern-footer">

    <div class="title">
        🎓 EduTrack Pro
    </div>

    <div class="subtitle">
        Student Management & Analytics Platform
    </div>

    <div class="subtitle">
        🚀 Multicloud DevOps by Chandra Shekhar
        &nbsp; | &nbsp;
        Spring Boot + Streamlit
        &nbsp; | &nbsp;
        {current_time}
    </div>

    <div style="
        color:#94a3b8;
        font-size:12px;
        margin-top:15px;
    ">
        Version 2.0 • © 2025 All Rights Reserved
    </div>

</div>
""", unsafe_allow_html=True)