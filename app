import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Telecom Project Manager",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Google Sheets setup (you'll replace with your credentials)
def init_google_sheets():
    try:
        # For demo - we'll use sample data
        # In production, you'll add Google Sheets API credentials
        return None
    except:
        return None

# Sample data for demo
def get_sample_data():
    users = pd.DataFrame([
        {"Email": "amir@company.com", "Name": "Amir Khan", "Role": "Field TL", "Team": "Team A", "Phone": "+1234567890"},
        {"Email": "im@company.com", "Name": "Ali Raza", "Role": "IM", "Team": "Management", "Phone": "+1234567891"},
        {"Email": "pm@company.com", "Name": "Sara Ahmed", "Role": "PM", "Team": "Management", "Phone": "+1234567892"},
        {"Email": "billing@company.com", "Name": "Bilal Khan", "Role": "Billing Team", "Team": "Finance", "Phone": "+1234567893"},
        {"Email": "gm@company.com", "Name": "General Manager", "Role": "GM", "Team": "Executive", "Phone": "+1234567894"}
    ])
    
    sites = pd.DataFrame([
        {"Site ID": "MDN2176", "Site Name": "Site Alpha", "Region": "North", "Customer": "Zain", "Status": "Active", "Created Date": "2024-01-15"},
        {"Site ID": "MDN2177", "Site Name": "Site Beta", "Region": "South", "Customer": "Mobily", "Status": "Active", "Created Date": "2024-01-16"},
        {"Site ID": "MDN2178", "Site Name": "Site Gamma", "Region": "Central", "Customer": "STC", "Status": "Planning", "Created Date": "2024-01-17"}
    ])
    
    daily_plans = pd.DataFrame([
        {"Plan ID": "PLAN001", "Site ID": "MDN2176", "Field TL": "Amir Khan", "Activity": "Installation", "Plan Date": "2024-01-20", "Status": "Assigned"},
        {"Plan ID": "PLAN002", "Site ID": "MDN2177", "Field TL": "Amir Khan", "Activity": "QC Check", "Plan Date": "2024-01-21", "Status": "In Progress"},
        {"Plan ID": "PLAN003", "Site ID": "MDN2178", "Field TL": "Amir Khan", "Activity": "Survey", "Plan Date": "2024-01-19", "Status": "Overdue"}
    ])
    
    activities = pd.DataFrame([
        {"Activity ID": "ACT001", "Site ID": "MDN2176", "Field TL": "Amir Khan", "Punch In": "09:00 AM", "Punch Out": "05:00 PM", "Status": "Completed", "Photos": ""},
        {"Activity ID": "ACT002", "Site ID": "MDN2177", "Field TL": "Amir Khan", "Punch In": "08:30 AM", "Punch Out": "", "Status": "In Progress", "Photos": ""},
        {"Activity ID": "ACT003", "Site ID": "MDN2178", "Field TL": "Amir Khan", "Punch In": "", "Punch Out": "", "Status": "Not Started", "Photos": ""}
    ])
    
    approvals = pd.DataFrame([
        {"Approval ID": "APR001", "Activity ID": "ACT001", "IM Status": "Approved", "PM Status": "Pending", "Billing Status": "Pending"},
        {"Approval ID": "APR002", "Activity ID": "ACT002", "IM Status": "Pending", "PM Status": "Pending", "Billing Status": "Pending"}
    ])
    
    return users, sites, daily_plans, activities, approvals

# Status highlighting functions
def get_status_color(status, days_pending=0):
    if status == "Overdue" or days_pending >= 2:
        return "🔴"  # Red
    elif status == "In Progress" or days_pending >= 1:
        return "🟡"  # Yellow
    else:
        return "🟢"  # Green

# Login page
def login_page():
    st.title("🏗️ Telecom Project Manager")
    st.subheader("Login to Your Dashboard")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995543.png", width=150)
    
    with col2:
        role = st.selectbox("Select Your Role", 
                           ["Field TL", "IM", "PM", "Billing Team", "GM"])
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            # Simple authentication for demo
            if email and password:
                st.session_state.user_role = role
                st.session_state.current_user = email
                st.success(f"Welcome {role}!")
                st.rerun()
            else:
                st.error("Please enter email and password")

# Field TL Dashboard
def field_tl_dashboard():
    st.title("👷 Field Team Lead Dashboard")
    
    users, sites, daily_plans, activities, approvals = get_sample_data()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Assigned Sites", len(daily_plans))
    with col2:
        completed = len(activities[activities["Status"] == "Completed"])
        st.metric("Completed", completed)
    with col3:
        in_progress = len(activities[activities["Status"] == "In Progress"])
        st.metric("In Progress", in_progress)
    with col4:
        overdue = len(daily_plans[daily_plans["Status"] == "Overdue"])
        st.metric("Overdue", overdue)
    
    # Daily Plans
    st.subheader("📋 Daily Plans")
    for _, plan in daily_plans.iterrows():
        status_color = get_status_color(plan["Status"])
        with st.expander(f"{status_color} {plan['Site ID']} - {plan['Activity']} - {plan['Plan Date']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Site:** {plan['Site ID']}")
                st.write(f"**Activity:** {plan['Activity']}")
                st.write(f"**Plan Date:** {plan['Plan Date']}")
            with col2:
                if plan["Status"] == "Assigned":
                    if st.button(f"Start Work", key=f"start_{plan['Plan ID']}"):
                        st.success("Work started! Punch-in recorded.")
                elif plan["Status"] == "In Progress":
                    if st.button(f"Complete Work", key=f"complete_{plan['Plan ID']}"):
                        st.success("Work completed! Punch-out recorded.")
    
    # Activity Log
    st.subheader("📝 Activity Log")
    st.dataframe(activities, use_container_width=True)

# IM Dashboard
def im_dashboard():
    st.title("📋 Inventory Manager Dashboard")
    
    users, sites, daily_plans, activities, approvals = get_sample_data()
    
    # Create new site
    with st.form("create_site"):
        st.subheader("🏗️ Create New Site")
        col1, col2 = st.columns(2)
        with col1:
            site_id = st.text_input("Site ID")
            site_name = st.text_input("Site Name")
        with col2:
            region = st.selectbox("Region", ["North", "South", "Central", "East", "West"])
            customer = st.selectbox("Customer", ["Zain", "Mobily", "STC"])
        
        if st.form_submit_button("Create Site"):
            st.success(f"Site {site_id} created successfully!")
    
    # Approval Queue
    st.subheader("✅ Approval Queue")
    pending_approvals = approvals[approvals["IM Status"] == "Pending"]
    
    for _, approval in pending_approvals.iterrows():
        with st.expander(f"🟡 Approval Needed - Activity {approval['Activity ID']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Activity details and progress...")
            with col2:
                if st.button("Approve", key=f"im_approve_{approval['Approval ID']}"):
                    st.success("Activity approved!")
                if st.button("Reject", key=f"im_reject_{approval['Approval ID']}"):
                    st.error("Activity rejected!")

# PM Dashboard
def pm_dashboard():
    st.title("💰 Project Manager Dashboard")
    
    users, sites, daily_plans, activities, approvals = get_sample_data()
    
    # Project Overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Projects", len(sites))
    with col2:
        st.metric("Active Projects", len(sites[sites["Status"] == "Active"]))
    with col3:
        st.metric("Completion Rate", "65%")
    
    # Billing Approval
    st.subheader("🧾 Billing Approval Queue")
    ready_for_billing = approvals[approvals["IM Status"] == "Approved"]
    
    for _, billing in ready_for_billing.iterrows():
        status_color = "🟡" if billing["PM Status"] == "Pending" else "🟢"
        with st.expander(f"{status_color} Billing Ready - {billing['Activity ID']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Project completion details...")
                st.write("Documents: ✅ All submitted")
            with col2:
                if billing["PM Status"] == "Pending":
                    if st.button("Approve for Billing", key=f"pm_approve_{billing['Approval ID']}"):
                        st.success("Approved for billing!")
                else:
                    st.success("✅ Approved")

# Billing Team Dashboard
def billing_dashboard():
    st.title("🧾 Billing Team Dashboard")
    
    users, sites, daily_plans, activities, approvals = get_sample_data()
    
    # PO Processing
    st.subheader("📄 PO Processing Queue")
    ready_for_billing = approvals[approvals["PM Status"] == "Approved"]
    
    for _, po in ready_for_billing.iterrows():
        with st.expander(f"🟡 PO Ready - {po['Activity ID']}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write("PO Details: ...")
                st.write("Amount: $1,500.00")
            with col2:
                st.selectbox("Submission Status", 
                           ["Not Submitted", "Submitted", "Approved", "Paid"],
                           key=f"status_{po['Approval ID']}")
            with col3:
                if st.button("Process", key=f"process_{po['Approval ID']}"):
                    st.success("PO processed successfully!")

# GM Dashboard
def gm_dashboard():
    st.title("👑 General Manager Dashboard")
    
    users, sites, daily_plans, activities, approvals = get_sample_data()
    
    # Executive Overview
    st.subheader("📊 Executive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sites", len(sites))
    with col2:
        st.metric("Active Projects", len(sites[sites["Status"] == "Active"]))
    with col3:
        st.metric("Completion Rate", "65%")
    with col4:
        st.metric("Revenue Potential", "$150,000")
    
    # Status Overview with colors
    st.subheader("🎯 Project Health Status")
    
    health_data = pd.DataFrame({
        "Status": ["Normal", "At Risk", "Overdue"],
        "Count": [15, 5, 2],
        "Color": ["green", "yellow", "red"]
    })
    
    # Display status cards
    cols = st.columns(3)
    for idx, (_, row) in enumerate(health_data.iterrows()):
        with cols[idx]:
            if row["Status"] == "Normal":
                st.info(f"🟢 {row['Status']}: {row['Count']} projects")
            elif row["Status"] == "At Risk":
                st.warning(f"🟡 {row['Status']}: {row['Count']} projects")
            else:
                st.error(f"🔴 {row['Status']}: {row['Count']} projects")
    
    # Department Performance
    st.subheader("📈 Department Performance")
    dept_data = pd.DataFrame({
        "Department": ["Field Teams", "IM", "PM", "Billing"],
        "Efficiency": [85, 65, 75, 70]
    })
    
    fig = px.bar(dept_data, x="Department", y="Efficiency", 
                 title="Department Efficiency Scores",
                 color="Efficiency", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

# Main app logic
def main():
    if st.session_state.user_role is None:
        login_page()
    else:
        # Sidebar with user info and logout
        with st.sidebar:
            st.write(f"**Logged in as:** {st.session_state.current_user}")
            st.write(f"**Role:** {st.session_state.user_role}")
            if st.button("Logout"):
                st.session_state.user_role = None
                st.session_state.current_user = None
                st.rerun()
            
            st.sidebar.title("Navigation")
        
        # Route to appropriate dashboard
        if st.session_state.user_role == "Field TL":
            field_tl_dashboard()
        elif st.session_state.user_role == "IM":
            im_dashboard()
        elif st.session_state.user_role == "PM":
            pm_dashboard()
        elif st.session_state.user_role == "Billing Team":
            billing_dashboard()
        elif st.session_state.user_role == "GM":
            gm_dashboard()

if __name__ == "__main__":
    main()
