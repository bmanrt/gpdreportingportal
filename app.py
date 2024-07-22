import streamlit as st
import mysql.connector
import pandas as pd
import bcrypt
from datetime import datetime
from io import BytesIO
import os

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'church_reports'

# Admin credentials (These should be hashed and stored securely in a real application)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')  # This should be hashed

# SQL statements
SQL_CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    password VARBINARY(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    zone VARCHAR(255) NOT NULL,
    privileges VARCHAR(255) DEFAULT 'View Reports,Submit Reports,Manage Reports'
);
"""

SQL_CREATE_CHURCH_TABLE = """
CREATE TABLE IF NOT EXISTS church_reports (
    id VARCHAR(255) PRIMARY KEY,
    ministry_year VARCHAR(255),
    month VARCHAR(255),
    zone VARCHAR(255),
    region VARCHAR(255),
    num_groups INT,
    num_achieved_1m_copies INT,
    num_hit_500k_copies INT,
    num_hit_250k_copies INT,
    num_hit_100k INT,
    wonder_alerts INT,
    sytk_alerts INT,
    rrm INT,
    total_copies_distribution INT,
    num_souls_won INT,
    num_rhapsody_outreaches INT,
    rhapsody_cells INT,
    num_new_churches INT,
    num_partners_enlisted INT,
    num_lingual_cells INT,
    num_language_churches INT,
    num_languages_sponsored INT,
    num_distribution_centers INT,
    num_prayer_programs INT,
    num_external_ministers INT,
    num_i_seed_daily INT,
    num_language_ambassadors INT,
    full_name VARCHAR(255),
    submission_timestamp VARCHAR(255)
);
"""

SQL_CREATE_ZONES_TABLE = """
CREATE TABLE IF NOT EXISTS zones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(255) NOT NULL,
    zone VARCHAR(255) NOT NULL
);
"""

SQL_CREATE_ID_TRACKER_TABLE = """
CREATE TABLE IF NOT EXISTS id_tracker (
    year VARCHAR(255) PRIMARY KEY,
    last_id INT NOT NULL
);
"""

# Regions and zones configuration
REGIONS = [
    "Region 1",
    "Region 2",
    "Region 3",
    "Region 4",
    "Region 5",
    "Region 6"
]

# List of years for ministry year selector
MINISTRY_YEARS = [str(year) for year in range(2023, datetime.now().year + 1)]

# Function to create a connection to a MySQL database
def create_connection():
    """ create a database connection to a MySQL database """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        raise Exception(f"Error: {e}")

# Function to create tables
def create_tables(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
    except mysql.connector.Error as e:
        raise Exception(f"Error creating table: {e}")

# Function to add a user to the database
def add_user(conn, user):
    sql = ''' INSERT INTO users(username, password, full_name, region, zone, privileges)
              VALUES(%s, %s, %s, %s, %s, %s) '''
    cursor = conn.cursor()
    cursor.execute(sql, user)
    conn.commit()
    return cursor.lastrowid

# Function to fetch a user from the database
def fetch_user(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    return cursor.fetchone()

# Function to check if a user exists
def user_exists(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username=%s", (username,))
    return cursor.fetchone() is not None

# Function to insert zones into the database
def insert_zones(conn, region, zones):
    sql = ''' INSERT INTO zones(region, zone)
              VALUES(%s, %s) '''
    cursor = conn.cursor()
    for zone in zones:
        cursor.execute(sql, (region, zone))
    conn.commit()

# Function to fetch zones by region from the database
def fetch_zones_by_region(conn, region):
    cursor = conn.cursor()
    cursor.execute("SELECT zone FROM zones WHERE region=%s", (region,))
    return [row[0] for row in cursor.fetchall()]

# Function to initialize zones data
def initialize_zones_data():
    conn = create_connection()
    create_tables(conn, SQL_CREATE_ZONES_TABLE)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM zones")
    count = cursor.fetchone()[0]

    if count == 0:  # Only insert if the table is empty
        # Region 1
        insert_zones(conn, "Region 1", [
            "SA Zone 1", "Cape Town Zone 1", "SA Zone 5", "Cape Town Zone 2",
            "SA Zone 2", "BLW Southern Africa Region", "Middle East Asia", "CE India",
            "SA Zone 3", "Durban", "BLW Asia & North Africa Region"
        ])

        # Region 2
        insert_zones(conn, "Region 2", [
            "UK Zone 3 Region 2", "CE Amsterdam DSP", "BLW Europe Region", "Western Europe Zone 4",
            "UK Zone 3 Region 1", "USA Zone 2 Region 1", "Eastern Europe", "Australia Zone",
            "Toronto Zone", "Western Europe Zone 2", "USA Zone 1 Region 2/Pacific Islands Region/New Zealand",
            "USA Region 3", "BLW Canada Sub-Region", "Western Europe Zone 3", "Dallas Zone USA Region 2",
            "UK Zone 4 Region 1", "Western Europe Zone 1", "UK Zone 1 (Region 2)", "UK Zone 2 Region 1",
            "UK Zone 1 Region 1", "USA Zone 1 Region 1", "BLW USA Region 2", "Ottawa Zone",
            "UK Zone 4 Region 2", "Quebec Zone", "BLW USA Region 1"
        ])

        # Region 3
        insert_zones(conn, "Region 3", [
            "Kenya Zone", "Lagos Zone 1", "EWCA Zone 4", "CE Chad", "EWCA Zone 2",
            "Ministry Center Warri", "Mid-West Zone", "South West Zone 2", "South West Zone 1",
            "Lagos Zone 4", "Ibadan Zone 1", "Ibadan Zone 2", "Accra Zone", "South West Zone 3",
            "EWCA Zone 5", "EWCA Zone 3", "MC Abeokuta", "EWCA Zone 6"
        ])

        # Region 4
        insert_zones(conn, "Region 4", [
            "Abuja Zone 2", "CELVZ", "Lagos Zone 2", "South South Zone 3", "South-South Zone 2",
            "Lagos Zone 3", "EWCA Zone 1", "South-South Zone 1", "DSC Sub Zone Warri", "Ministry Center Abuja",
            "Ministry Center Calabar"
        ])

        # Region 5
        insert_zones(conn, "Region 5", [
            "Middle Belt Region Zone 2", "North East Zone 1", "PH Zone 1", "Lagos Zone 6",
            "Lagos Sub Zone B", "Middle Belt Region Zone 1", "PH Zone 3", "Lagos Sub Zone A",
            "South West Zone 5", "Onitsha Zone", "Abuja Zone", "PH Zone 2", "North West Zone 2",
            "Lagos Zone 5", "Northwest Zone 1", "Ministry Center Ibadan", "South West Zone 4",
            "North Central Zone 1", "North Central Zone 2"
        ])

        # Region 6
        insert_zones(conn, "Region 6", [
            "Lagos Sub Zone C", "Benin Zone 2", "Aba Zone", "Benin Zone 1", "Loveworld Church Zone",
            "South East Zone 1", "BLW West Africa Region", "BLW East & Central Africa Region", "South East Zone 3",
            "Edo North & Central", "BLW Nigeria Region"
        ])

initialize_zones_data()

def generate_unique_id(conn, ministry_year):
    cursor = conn.cursor()
    cursor.execute("SELECT last_id FROM id_tracker WHERE year=%s", (ministry_year,))
    row = cursor.fetchone()
    if row:
        last_id = row[0] + 1
        cursor.execute("UPDATE id_tracker SET last_id=%s WHERE year=%s", (last_id, ministry_year))
    else:
        last_id = 1
        cursor.execute("INSERT INTO id_tracker (year, last_id) VALUES (%s, %s)", (ministry_year, last_id))
    conn.commit()
    unique_id = f"GPD{ministry_year}-{last_id:04d}"
    return unique_id

# Insert data into the church_reports table
def insert_church_report(conn, report):
    try:
        sql = '''INSERT INTO church_reports(
                    id, ministry_year, month, zone, region, num_groups, 
                    num_achieved_1m_copies, num_hit_500k_copies, num_hit_250k_copies, 
                    num_hit_100k, wonder_alerts, sytk_alerts, rrm, 
                    total_copies_distribution, num_souls_won, num_rhapsody_outreaches, 
                    rhapsody_cells, num_new_churches, num_partners_enlisted, num_lingual_cells, 
                    num_language_churches, num_languages_sponsored, num_distribution_centers, 
                    num_prayer_programs, num_external_ministers, num_i_seed_daily, 
                    num_language_ambassadors, full_name, submission_timestamp
                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor = conn.cursor()
        cursor.execute(sql, report)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        raise Exception(f"Error inserting report: {e}")


# Fetch all reports
def fetch_reports(conn):
    try:
        return pd.read_sql_query("SELECT * FROM church_reports ORDER BY region", conn)
    except Exception as e:
        raise Exception(f"Error fetching reports: {e}")

# Update a report
def update_report(conn, report_id, data):
    try:
        sql = '''UPDATE church_reports
                 SET ministry_year = %s, month = %s, zone = %s, region = %s, num_groups = %s, num_achieved_1m_copies = %s, num_hit_500k_copies = %s, num_hit_250k_copies = %s, num_hit_100k = %s, wonder_alerts = %s, sytk_alerts = %s, rrm = %s, total_copies_distribution = %s, num_souls_won = %s, num_rhapsody_outreaches = %s, rhapsody_cells = %s, num_new_churches = %s, num_partners_enlisted = %s, num_lingual_cells = %s, num_language_churches = %s, num_languages_sponsored = %s, num_distribution_centers = %s, num_prayer_programs = %s, num_external_ministers = %s, num_i_seed_daily = %s, num_language_ambassadors = %s, full_name = %s
                 WHERE id = %s'''
        cursor = conn.cursor()
        cursor.execute(sql, data + (report_id,))
        conn.commit()
    except Exception as e:
        raise Exception(f"Error updating report: {e}")

# Delete a report
def delete_report(conn, report_id):
    try:
        sql = '''DELETE FROM church_reports WHERE id = %s'''
        cursor = conn.cursor()
        cursor.execute(sql, (report_id,))
        conn.commit()
    except Exception as e:
        raise Exception(f"Error deleting report: {e}")

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# Generate Excel
def generate_excel(report_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        report_df.to_excel(writer, index=False, sheet_name='Reports')
    output.seek(0)
    return output

# User Authentication and Session Management
def login_page():
    st.title("Login")
    try:
        conn = create_connection()
        create_tables(conn, SQL_CREATE_USERS_TABLE)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            user = fetch_user(conn, username)
            if user and check_password(password, bytes(user[1])):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['full_name'] = user[2]
                st.session_state['region'] = user[3]
                st.session_state['zone'] = user[4]
                st.session_state['privileges'] = user[5].split(',')
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    except Exception as e:
        st.error(f"Error: {e}")

def create_account_page():
    st.title("Create Account")
    try:
        conn = create_connection()
        create_tables(conn, SQL_CREATE_USERS_TABLE)
        
        full_name = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        region = st.selectbox('Region', REGIONS)
        zones_conn = create_connection()
        zones = fetch_zones_by_region(zones_conn, region)
        zone = st.selectbox('Zone', zones)
        
        if st.button("Create Account"):
            if password != password_confirm:
                st.error("Passwords do not match")
            elif user_exists(conn, username):
                st.error("Username already exists")
            elif not region or not zone:
                st.error("Please select a region and a zone")
            else:
                hashed_password = hash_password(password)
                add_user(conn, (username, hashed_password, full_name, region, zone, 'View Reports,Submit Reports,Manage Reports'))
                st.success("Account created successfully! You can now log in.")
    except Exception as e:
        st.error(f"Error: {e}")

def forgot_password_page():
    st.title("Forgot Password")
    try:
        conn = create_connection()
        create_tables(conn, SQL_CREATE_USERS_TABLE)
        
        username = st.text_input("Username")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        new_password_confirm = st.text_input("Confirm New Password", type="password")
        
        if st.button("Reset Password"):
            user = fetch_user(conn, username)
            if not user:
                st.error("Username does not exist")
            elif not check_password(current_password, user[1]):
                st.error("Current password is incorrect")
            elif new_password != new_password_confirm:
                st.error("New passwords do not match")
            else:
                hashed_password = hash_password(new_password)
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (hashed_password, username))
                conn.commit()
                st.success("Password reset successfully! You can now log in.")
    except Exception as e:
        st.error(f"Error: {e}")



def admin_login_page():
    st.title("Admin Login")
    try:
        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")
        
        if st.button("Login"):
            if username == ADMIN_USERNAME and check_password(password, hash_password(ADMIN_PASSWORD)):
                st.session_state['admin_logged_in'] = True
                st.experimental_rerun()
            else:
                st.error("Invalid admin username or password")
    except Exception as e:
        st.error(f"Error: {e}")

def admin_dashboard():
    st.title("Admin Dashboard")
    try:
        conn = create_connection()
        create_tables(conn, SQL_CREATE_USERS_TABLE)

        # Toggle dark/light mode
        if 'theme' not in st.session_state:
            st.session_state['theme'] = 'light'

        if st.button("Toggle Dark Mode"):
            if st.session_state['theme'] == 'light':
                st.session_state['theme'] = 'dark'
            else:
                st.session_state['theme'] = 'light'
            st.experimental_rerun()

        # Apply CSS for dark/light mode
        if st.session_state['theme'] == 'dark':
            st.markdown("""
            <style>
            body {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            .stButton>button {
                background-color: #6C757D;
                color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <style>
            body {
                background-color: #FFFFFF;
                color: #000000;
            }
            .stButton>button {
                background-color: #007BFF;
                color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)

        # Admin logout button
        if st.button("Logout"):
            st.session_state['admin_logged_in'] = False
            st.experimental_rerun()

        # Fetch all users
        users_df = pd.read_sql_query("SELECT * FROM users", conn)
        
        # Display users
        st.subheader("Manage Users")
        st.write(users_df)

        # Select user to manage
        selected_user = st.selectbox("Select User", users_df['username'])
        action = st.radio("Action", ["Edit", "Delete"])

        if action == "Edit":
            user_data = users_df[users_df['username'] == selected_user].iloc[0]
            with st.form(key='edit_user_form'):
                full_name = st.text_input('Full Name', user_data['full_name'])
                region = st.selectbox('Region', REGIONS, index=REGIONS.index(user_data['region']))
                zones_conn = create_connection()
                zones = fetch_zones_by_region(zones_conn, region)
                zone = st.selectbox('Zone', zones, index=zones.index(user_data['zone']))
                privileges = st.multiselect('Privileges', ["View Reports", "Submit Reports", "Manage Reports", "Download Reports"], default=user_data['privileges'].split(','))
                if st.form_submit_button(label='Update'):
                    privileges_str = ','.join(privileges)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET full_name=%s, region=%s, zone=%s, privileges=%s WHERE username=%s", (full_name, region, zone, privileges_str, selected_user))
                    conn.commit()
                    st.success("User updated successfully!")
                    st.experimental_rerun()

        elif action == "Delete":
            if st.button("Delete User"):
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username=%s", (selected_user,))
                conn.commit()
                st.success("User deleted successfully!")
                st.experimental_rerun()

        st.subheader("All Reports")
        reports_conn = create_connection()
        reports_df = fetch_reports(reports_conn)
        
        if reports_df.empty:
            st.warning("No reports available.")
        else:
            year = st.selectbox('Select Year', MINISTRY_YEARS)
            reports_df = reports_df[reports_df['ministry_year'] == year]

            filter_by = st.selectbox('Filter by', ['Monthly', 'Quarterly', 'Mid-Year', 'Annual', 'User Defined'])

            if filter_by == 'Monthly':
                month = st.selectbox('Select Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                filtered_df = reports_df[reports_df['month'] == month]
            elif filter_by == 'Quarterly':
                quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
                if quarter == 'Q1':
                    filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March'])]
                elif quarter == 'Q2':
                    filtered_df = reports_df[reports_df['month'].isin(['April', 'May', 'June'])]
                elif quarter == 'Q3':
                    filtered_df = reports_df[reports_df['month'].isin(['July', 'August', 'September'])]
                elif quarter == 'Q4':
                    filtered_df = reports_df[reports_df['month'].isin(['October', 'November', 'December'])]
            elif filter_by == 'Mid-Year':
                filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March', 'April', 'May', 'June'])]
            elif filter_by == 'Annual':
                filtered_df = reports_df
            elif filter_by == 'User Defined':
                start_month = st.selectbox('Start Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                end_month = st.selectbox('End Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                months_order = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
                start_index = months_order.index(start_month)
                end_index = months_order.index(end_month)
                if start_index <= end_index:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:end_index + 1])]
                else:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:] + months_order[:end_index + 1])]

            st.write(filtered_df)

            if not filtered_df.empty:
                if st.button("Download as Excel"):
                    excel_content = generate_excel(filtered_df)
                    st.download_button(label="Download Excel", data=excel_content, file_name="reports.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("No reports found for the selected filter.")
    except Exception as e:
        st.error(f"Error: {e}")

# Dashboard
def dashboard(conn):
    st.title('Dashboard')
    try:
        reports_df = fetch_reports(conn)
        
        if reports_df.empty:
            st.warning("No reports available.")
        else:
            reports_df = reports_df[(reports_df['region'] == st.session_state['region']) & (reports_df['zone'] == st.session_state['zone'])]

            year = st.selectbox('Select Year', MINISTRY_YEARS)
            reports_df = reports_df[reports_df['ministry_year'] == year]

            # Calculate total copies
            reports_df['total_copies'] = (
                reports_df['num_achieved_1m_copies'] * 1e6 +
                reports_df['num_hit_500k_copies'] * 5e5 +
                reports_df['num_hit_250k_copies'] * 2.5e5 +
                reports_df['num_hit_100k'] * 1e5
            )

            total_copies = reports_df['total_copies'].sum()

            # Calculate progress percentage
            progress_percentage = min((total_copies / 4e6) * 100, 100)

            # Display progress bar
            st.title("Total Copies Progress Bar")
            st.progress(progress_percentage / 100)
           

            filter_by = st.selectbox('Filter by', ['Monthly', 'Quarterly', 'Mid-Year', 'Annual', 'User Defined'])
            
            if filter_by == 'Monthly':
                month = st.selectbox('Select Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                filtered_df = reports_df[reports_df['month'] == month]
            elif filter_by == 'Quarterly':
                quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
                if quarter == 'Q1':
                    filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March'])]
                elif quarter == 'Q2':
                    filtered_df = reports_df[reports_df['month'].isin(['April', 'May', 'June'])]
                elif quarter == 'Q3':
                    filtered_df = reports_df[reports_df['month'].isin(['July', 'August', 'September'])]
                elif quarter == 'Q4':
                    filtered_df = reports_df[reports_df['month'].isin(['October', 'November', 'December'])]
            elif filter_by == 'Mid-Year':
                filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March', 'April', 'May', 'June'])]
            elif filter_by == 'Annual':
                filtered_df = reports_df
            elif filter_by == 'User Defined':
                start_month = st.selectbox('Start Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                end_month = st.selectbox('End Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                months_order = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
                start_index = months_order.index(start_month)
                end_index = months_order.index(end_month)
                if start_index <= end_index:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:end_index + 1])]
                else:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:] + months_order[:end_index + 1])]

            if not filtered_df.empty:
                st.subheader("Key Metrics")

                metrics = {
                    "Total Reports": len(filtered_df),
                    "Total Groups in the Champions League": filtered_df['num_groups'].sum(),
                    "Total Achieved 1M Copies": filtered_df['num_achieved_1m_copies'].sum(),
                    "Total Hit 500K Copies": filtered_df['num_hit_500k_copies'].sum(),
                    "Total Hit 250K Copies": filtered_df['num_hit_250k_copies'].sum(),
                    "Total Hit 100K Copies": filtered_df['num_hit_100k'].sum(),
                    "Total Wonder Alerts": filtered_df['wonder_alerts'].sum(),
                    "Total SYTK Alerts": filtered_df['sytk_alerts'].sum(),
                    "Total RRM": filtered_df['rrm'].sum(),
                    "Total Copies Distribution": filtered_df['total_copies_distribution'].sum(),
                    "Total Souls Won": filtered_df['num_souls_won'].sum(),
                    "Total Rhapsody Outreaches": filtered_df['num_rhapsody_outreaches'].sum(),
                    "Total Rhapsody Cells": filtered_df['rhapsody_cells'].sum(),
                    "Total New Churches": filtered_df['num_new_churches'].sum(),
                    "Total Partners Enlisted": filtered_df['num_partners_enlisted'].sum(),
                    "Total Lingual Cells": filtered_df['num_lingual_cells'].sum(),
                    "Total Language Churches": filtered_df['num_language_churches'].sum(),
                    "Total Languages Sponsored": filtered_df['num_languages_sponsored'].sum(),
                    "Total Distribution Centers": filtered_df['num_distribution_centers'].sum(),
                    "Total Prayer Programs": filtered_df['num_prayer_programs'].sum(),
                    "Total External Ministers": filtered_df['num_external_ministers'].sum(),
                    "Total I-SEED Daily": filtered_df['num_i_seed_daily'].sum(),
                    "Total Language Ambassadors": filtered_df['num_language_ambassadors'].sum()
                }

                cols = st.columns(6)
                for idx, (metric, value) in enumerate(metrics.items()):
                    cols[idx % 6].metric(metric, value)

                st.subheader('Data Table')
                st.dataframe(filtered_df)

                if st.button("Download Excel"):
                    excel_content = generate_excel(filtered_df)
                    st.download_button(label="Download Excel", data=excel_content, file_name="reports.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("No reports found for the selected filter.")
    except Exception as e:
        st.error(f"Error: {e}")

# Submit Report
def submit_report(conn):
    st.title('Submit Report')
    try:
        with st.form(key='church_report_form'):
            full_name = st.session_state['full_name']
            st.write(f"Full Name: {full_name}")
            ministry_year = st.selectbox('Ministry Year', MINISTRY_YEARS)
            month = st.selectbox('Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
            
            num_groups = st.number_input('Number of Groups currently in the Champions League', min_value=0)
            num_achieved_1m_copies = st.number_input('Number of Groups that have achieved their 1M copies', min_value=0)
            num_hit_500k_copies = st.number_input('Number of Groups who have hit 500,000 copies', min_value=0)
            num_hit_250k_copies = st.number_input('Number of Groups who have hit 250,000 copies', min_value=0)
            num_hit_100k = st.number_input('Number of Groups who have hit 100,000 copies', min_value=0)
            
            wonder_alerts = st.number_input('Number of Wonder Alerts', min_value=0)
            sytk_alerts = st.number_input('Number of SYTK Alerts', min_value=0)
            rrm = st.number_input('Rhapsody Redemption Missions (RRM)', min_value=0)
            total_copies_distribution = st.number_input('Total Copies Distribution', min_value=0)
            num_souls_won = st.number_input('Number of Souls Won', min_value=0)
            num_rhapsody_outreaches = st.number_input('Number of Rhapsody Outreaches', min_value=0)
            rhapsody_cells = st.number_input('Rhapsody Cells', min_value=0)
            num_new_churches = st.number_input('Number of New Churches', min_value=0)
            num_partners_enlisted = st.number_input('Number of Partners Enlisted', min_value=0)
            num_lingual_cells = st.number_input('Number of Lingual Cells', min_value=0)
            num_language_churches = st.number_input('Number of Language Churches', min_value=0)
            num_languages_sponsored = st.number_input('Number of Languages Sponsored', min_value=0)
            num_distribution_centers = st.number_input('Number of Distribution Centers', min_value=0)
            num_prayer_programs = st.number_input('Number of Prayer Programs', min_value=0)
            num_external_ministers = st.number_input('Number of External Ministers', min_value=0)
            num_i_seed_daily = st.number_input('Number of I-SEED Daily', min_value=0)
            num_language_ambassadors = st.number_input('Number of Language Ambassadors', min_value=0)

            if st.form_submit_button(label='Submit'):
                if ministry_year and month:
                    submission_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    unique_id = generate_unique_id(conn, ministry_year)
                    report = (
                        unique_id, ministry_year, month, st.session_state['zone'], st.session_state['region'], 
                        num_groups, num_achieved_1m_copies, num_hit_500k_copies, num_hit_250k_copies, 
                        num_hit_100k, wonder_alerts, sytk_alerts, rrm, total_copies_distribution, 
                        num_souls_won, num_rhapsody_outreaches, rhapsody_cells, num_new_churches, 
                        num_partners_enlisted, num_lingual_cells, num_language_churches, num_languages_sponsored, 
                        num_distribution_centers, num_prayer_programs, num_external_ministers, num_i_seed_daily, 
                        num_language_ambassadors, full_name, submission_timestamp
                    )
                    insert_church_report(conn, report)
                    st.success("Report submitted successfully!")
                else:
                    st.error("Please fill in all required fields.")
    except Exception as e:
        st.error(f"Error: {e}")


# Manage Reports
def manage_reports(conn):
    st.title('Manage Reports')
    try:
        reports_df = fetch_reports(conn)
        
        if reports_df.empty:
            st.warning("No reports available to manage.")
        else:
            reports_df = reports_df[(reports_df['region'] == st.session_state['region']) & (reports_df['zone'] == st.session_state['zone'])]

            year = st.selectbox('Select Year', MINISTRY_YEARS)
            reports_df = reports_df[reports_df['ministry_year'] == year]

            filter_by = st.selectbox('Filter by', ['Monthly', 'Quarterly', 'Mid-Year', 'Annual', 'User Defined'])

            if filter_by == 'Monthly':
                month = st.selectbox('Select Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                filtered_df = reports_df[reports_df['month'] == month]
            elif filter_by == 'Quarterly':
                quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
                if quarter == 'Q1':
                    filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March'])]
                elif quarter == 'Q2':
                    filtered_df = reports_df[reports_df['month'].isin(['April', 'May', 'June'])]
                elif quarter == 'Q3':
                    filtered_df = reports_df[reports_df['month'].isin(['July', 'August', 'September'])]
                elif quarter == 'Q4':
                    filtered_df = reports_df[reports_df['month'].isin(['October', 'November', 'December'])]
            elif filter_by == 'Mid-Year':
                filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March', 'April', 'May', 'June'])]
            elif filter_by == 'Annual':
                filtered_df = reports_df
            elif filter_by == 'User Defined':
                start_month = st.selectbox('Start Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                end_month = st.selectbox('End Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                months_order = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
                start_index = months_order.index(start_month)
                end_index = months_order.index(end_month)
                if start_index <= end_index:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:end_index + 1])]
                else:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:] + months_order[:end_index + 1])]

            st.write(filtered_df)

            if not filtered_df.empty:
                report_id = st.selectbox("Select Report ID to Edit/Delete", filtered_df['id'])
                action = st.radio("Action", ["Edit", "Delete"])
                
                if action == "Edit":
                    report_to_edit = filtered_df[filtered_df['id'] == report_id].iloc[0]
                    with st.form(key='edit_report_form'):
                        full_name = st.text_input('Full Name', report_to_edit['full_name'])
                        ministry_year = st.selectbox('Ministry Year', MINISTRY_YEARS, index=MINISTRY_YEARS.index(report_to_edit['ministry_year']))
                        month = st.selectbox('Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)], index=[datetime(2000, i, 1).strftime('%B') for i in range(1, 13)].index(report_to_edit['month']))
                        
                        num_groups = st.number_input('Number of Groups currently in the Champions League', min_value=0, value=report_to_edit['num_groups'])
                        num_achieved_1m_copies = st.number_input('Number of Groups that have achieved their 1M copies', min_value=0, value=report_to_edit['num_achieved_1m_copies'])
                        num_hit_500k_copies = st.number_input('Number of Groups who have hit 500,000 copies', min_value=0, value=report_to_edit['num_hit_500k_copies'])
                        num_hit_250k_copies = st.number_input('Number of Groups who have hit 250,000 copies', min_value=0, value=report_to_edit['num_hit_250k_copies'])
                        num_hit_100k = st.number_input('Number of Groups who have hit 100,000 copies', min_value=0, value=report_to_edit['num_hit_100k'])
                        
                        wonder_alerts = st.number_input('Number of Wonder Alerts', min_value=0, value=report_to_edit['wonder_alerts'])
                        sytk_alerts = st.number_input('Number of SYTK Alerts', min_value=0, value=report_to_edit['sytk_alerts'])
                        rrm = st.number_input('Rhapsody Redemption Missions (RRM)', min_value=0, value=report_to_edit['rrm'])
                        total_copies_distribution = st.number_input('Total Copies Distribution', min_value=0, value=report_to_edit['total_copies_distribution'])
                        num_souls_won = st.number_input('Number of Souls Won', min_value=0, value=report_to_edit['num_souls_won'])
                        num_rhapsody_outreaches = st.number_input('Number of Rhapsody Outreaches', min_value=0, value=report_to_edit['num_rhapsody_outreaches'])
                        rhapsody_cells = st.number_input('Rhapsody Cells', min_value=0, value=report_to_edit['rhapsody_cells'])
                        num_new_churches = st.number_input('Number of New Churches', min_value=0, value=report_to_edit['num_new_churches'])
                        num_partners_enlisted = st.number_input('Number of Partners Enlisted', min_value=0, value=report_to_edit['num_partners_enlisted'])
                        num_lingual_cells = st.number_input('Number of Lingual Cells', min_value=0, value=report_to_edit['num_lingual_cells'])
                        num_language_churches = st.number_input('Number of Language Churches', min_value=0, value=report_to_edit['num_language_churches'])
                        num_languages_sponsored = st.number_input('Number of Languages Sponsored', min_value=0, value=report_to_edit['num_languages_sponsored'])
                        num_distribution_centers = st.number_input('Number of Distribution Centers', min_value=0, value=report_to_edit['num_distribution_centers'])
                        num_prayer_programs = st.number_input('Number of Prayer Programs', min_value=0, value=report_to_edit['num_prayer_programs'])
                        num_external_ministers = st.number_input('Number of External Ministers', min_value=0, value=report_to_edit['num_external_ministers'])
                        num_i_seed_daily = st.number_input('Number of I-SEED Daily', min_value=0, value=report_to_edit['num_i_seed_daily'])
                        num_language_ambassadors = st.number_input('Number of Language Ambassadors', min_value=0, value=report_to_edit['num_language_ambassadors'])
                        
                        if st.form_submit_button(label='Update'):
                            update_report(conn, report_id, (ministry_year, month, st.session_state['zone'], st.session_state['region'], num_groups, num_achieved_1m_copies, num_hit_500k_copies, num_hit_250k_copies, num_hit_100k, wonder_alerts, sytk_alerts, rrm, total_copies_distribution, num_souls_won, num_rhapsody_outreaches, rhapsody_cells, num_new_churches, num_partners_enlisted, num_lingual_cells, num_language_churches, num_languages_sponsored, num_distribution_centers, num_prayer_programs, num_external_ministers, num_i_seed_daily, num_language_ambassadors, full_name))
                            st.success("Report updated successfully!")

                elif action == "Delete":
                    if st.button("Delete"):
                        delete_report(conn, report_id)
                        st.success("Report deleted successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# Download Reports
def download_reports(conn):
    st.title('Download Reports')
    try:
        reports_df = fetch_reports(conn)
        
        if reports_df.empty:
            st.warning("No reports available to download.")
        else:
            reports_df = reports_df[(reports_df['region'] == st.session_state['region']) & (reports_df['zone'] == st.session_state['zone'])]

            year = st.selectbox('Select Year', MINISTRY_YEARS)
            reports_df = reports_df[reports_df['ministry_year'] == year]

            filter_by = st.selectbox('Filter by', ['Monthly', 'Quarterly', 'Mid-Year', 'Annual', 'User Defined'])

            if filter_by == 'Monthly':
                month = st.selectbox('Select Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                filtered_df = reports_df[reports_df['month'] == month]
            elif filter_by == 'Quarterly':
                quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
                if quarter == 'Q1':
                    filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March'])]
                elif quarter == 'Q2':
                    filtered_df = reports_df[reports_df['month'].isin(['April', 'May', 'June'])]
                elif quarter == 'Q3':
                    filtered_df = reports_df[reports_df['month'].isin(['July', 'August', 'September'])]
                elif quarter == 'Q4':
                    filtered_df = reports_df[reports_df['month'].isin(['October', 'November', 'December'])]
            elif filter_by == 'Mid-Year':
                filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March', 'April', 'May', 'June'])]
            elif filter_by == 'Annual':
                filtered_df = reports_df
            elif filter_by == 'User Defined':
                start_month = st.selectbox('Start Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                end_month = st.selectbox('End Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                months_order = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
                start_index = months_order.index(start_month)
                end_index = months_order.index(end_month)
                if start_index <= end_index:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:end_index + 1])]
                else:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:] + months_order[:end_index + 1])]

            st.write(filtered_df)

            if not filtered_df.empty:
                excel_content = generate_excel(filtered_df)
                st.download_button(label="Download Excel", data=excel_content, file_name="reports.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("No reports found for the selected filter.")
    except Exception as e:
        st.error(f"Error: {e}")

def download_reports(conn):
    st.title('Download Reports')
    try:
        reports_df = fetch_reports(conn)
        
        if reports_df.empty:
            st.warning("No reports available to download.")
        else:
            reports_df = reports_df[(reports_df['region'] == st.session_state['region']) & (reports_df['zone'] == st.session_state['zone'])]

            year = st.selectbox('Select Year', MINISTRY_YEARS)
            reports_df = reports_df[reports_df['ministry_year'] == year]

            filter_by = st.selectbox('Filter by', ['Monthly', 'Quarterly', 'Mid-Year', 'Annual', 'User Defined'])

            if filter_by == 'Monthly':
                month = st.selectbox('Select Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                filtered_df = reports_df[reports_df['month'] == month]
            elif filter_by == 'Quarterly':
                quarter = st.selectbox('Select Quarter', ['Q1', 'Q2', 'Q3', 'Q4'])
                if quarter == 'Q1':
                    filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March'])]
                elif quarter == 'Q2':
                    filtered_df = reports_df[reports_df['month'].isin(['April', 'May', 'June'])]
                elif quarter == 'Q3':
                    filtered_df = reports_df[reports_df['month'].isin(['July', 'August', 'September'])]
                elif quarter == 'Q4':
                    filtered_df = reports_df[reports_df['month'].isin(['October', 'November', 'December'])]
            elif filter_by == 'Mid-Year':
                filtered_df = reports_df[reports_df['month'].isin(['January', 'February', 'March', 'April', 'May', 'June'])]
            elif filter_by == 'Annual':
                filtered_df = reports_df
            elif filter_by == 'User Defined':
                start_month = st.selectbox('Start Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                end_month = st.selectbox('End Month', [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)])
                months_order = [datetime(2000, i, 1).strftime('%B') for i in range(1, 13)]
                start_index = months_order.index(start_month)
                end_index = months_order.index(end_month)
                if start_index <= end_index:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:end_index + 1])]
                else:
                    filtered_df = reports_df[reports_df['month'].isin(months_order[start_index:] + months_order[:end_index + 1])]

            st.write(filtered_df)

            if not filtered_df.empty:
                if st.button("Download as Excel"):
                    excel_content = generate_excel(filtered_df)
                    st.download_button(label="Download Excel", data=excel_content, file_name="reports.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("No reports found for the selected filter.")
    except Exception as e:
        st.error(f"Error: {e}")

# Set page configuration
st.set_page_config(layout="wide")

# Main application function
def main():
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if st.session_state['admin_logged_in']:
        admin_dashboard()
    elif st.session_state['logged_in']:
        st.sidebar.title("Navigation")

        # Determine which pages to show based on user privileges
        privileges = st.session_state['privileges']
        pages = ["Dashboard", "Submit Report", "Manage Reports", "Download Reports", "Logout"]
        if "View Reports" not in privileges:
            pages.remove("Dashboard")
        if "Submit Reports" not in privileges:
            pages.remove("Submit Report")
        if "Manage Reports" not in privileges:
            pages.remove("Manage Reports")
        if "Download Reports" not in privileges:
            pages.remove("Download Reports")

        page = st.sidebar.radio("Go to", pages, index=0)

        if page == "Logout":
            st.session_state['logged_in'] = False
            st.experimental_rerun()

        conn = create_connection()
        create_tables(conn, SQL_CREATE_CHURCH_TABLE)
        create_tables(conn, SQL_CREATE_ID_TRACKER_TABLE)

        if page == "Dashboard":
            dashboard(conn)
        elif page == "Submit Report":
            submit_report(conn)
        elif page == "Manage Reports":
            manage_reports(conn)
        elif page == "Download Reports":
            download_reports(conn)
    else:
        auth_page = st.selectbox("Select Authentication Page", ["Login", "Create Account", "Forgot Password", "Admin Login"])
        if auth_page == "Login":
            login_page()
        elif auth_page == "Create Account":
            create_account_page()
        elif auth_page == "Forgot Password":
            forgot_password_page()
        elif auth_page == "Admin Login":
            admin_login_page()

if __name__ == '__main__':
    main()

