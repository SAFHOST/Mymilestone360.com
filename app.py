import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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

# Sample data - No external dependencies
def get_sample_data():
    users = [
        {"Email": "field@demo.com", "Name": "Amir Khan", "Role": "Field TL", "Team": "Team A"},
        {"Email": "im@demo.com", "Name": "Ali Raza", "Role": "IM", "Team": "Management"},
        {"Email": "pm@demo.com", "Name": "Sara Ahmed", "Role": "PM", "Team": "Management"},
        {"Email": "billing@demo.com", "Name": "Bilal Khan", "Role": "Billing Team", "Team": "Finance"},
        {"Email": "gm@demo.com", "Name": "General Manager", "Role": "GM", "Team": "Executive"}
    ]
    
    sites = [
        {"Site ID": "MDN2176", "Site Name": "Site Alpha", "Region": "North", "Customer": "Zain", "Status": "Active"},
        {"Site ID": "MDN2177", "Site Name": "Site Beta", "Region": "South", "Customer": "Mobily", "Status": "Active"},
        {"Site ID": "MDN2178", "Site Name": "Site Gamma", "Region": "Central", "Customer": "STC", "Status": "Planning"}
    ]
    
    daily_plans = [
        {"Plan ID": "PLAN001", "Site ID": "MDN2176", "Field TL": "Amir Khan", "Activity": "Installation", "Status": "Assigned"},
        {"Plan ID": "PLAN002", "Site ID": "MDN2177", "Field TL": "Amir Khan", "Activity": "QC Check", "Status": "In Progress"},
        {"Plan ID": "PLAN003", "Site ID": "MDN2178", "Field TL": "Amir Khan", "Activity": "Survey", "Status": "Overdue"}
    ]
    
    activities = [
        {"Activity ID": "ACT001", "Site ID": "MDN2176", "Status": "Completed", "Progress": "100%"},
        {"Activity ID": "ACT002", "Site ID": "MDN2177", "Status": "In Progress", "Progress": "60%"},
        {"Activity ID": "ACT003", "Site ID": "MDN2178", "Status": "Not Started", "Progress": "0%"}
    ]
    
    return users, sites, daily_plans, activities

# Status highlighting
def get_status_color(status):
    if status in ["Overdue", "Cancelled"]:
        return "🔴"
    elif status in ["In Progress", "At Risk"]:
        return "🟡"
    else:
        return "🟢"

# Login page
def login_page():
    st.title("🏗️ Telecom Project Manager")
    st.markdown("**Demo Version - No Login Required**")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("🎯 **Select your role to continue**")
    
    with col2:
        role = st.selectbox("Choose Dashboard", 
                           ["Field TL", "IM", "PM", "Billing Team", "GM"])
        
        if st.button("Enter Dashboard", type="primary"):
            st.session_state.user_role = role
            st.session_state.current_user = f"{role}@demo.com"
            st.rerun()

# Field TL Dashboard
def field_tl_dashboard():
    st.title("👷 Field Team Lead Dashboard")
    
    users, sites, daily_plans, activities = get_sample_data()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Assigned Sites", "3")
    with col2:
        st.metric("Completed", "1")
    with col3:
        st.metric("In Progress", "1")
    with col4:
        st.metric("Overdue", "1")
    
    # Daily Plans with colors
    st.subheader("📋 Daily Plans")
    for plan in daily_plans:
        status_color = get_status_color(plan["Status"])
        with st.expander(f"{status_color} {plan['Site ID']} - {plan['Activity']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Site:** {plan['Site ID']}")
                st.write(f"**Activity:** {plan['Activity']}")
                st.write(f"**Status:** {plan['Status']}")
            with col2:
                if st.button(f"Update Status", key=f"btn_{plan['Plan ID']}"):
                    st.success("Status updated successfully!")

# IM Dashboard
def im_dashboard():
    st.title("📋 Inventory Manager Dashboard")
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sites", "15")
    with col2:
        st.metric("Pending Approval", "3")
    with col3:
        st.metric("Active Teams", "5")
    
    # Site creation
    with st.form("create_site"):
        st.subheader("🏗️ Create New Site")
        site_id = st.text_input("Site ID")
        site_name = st.text_input("Site Name")
        region = st.selectbox("Region", ["North", "South", "Central"])
        
        if st.form_submit_button("Create Site"):
            st.success(f"Site {site_id} created successfully!")

# PM Dashboard
def pm_dashboard():
    st.title("💰 Project Manager Dashboard")
    
    # Project metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Projects", "12")
    with col2:
        st.metric("On Track", "8 🟢")
    with col3:
        st.metric("At Risk", "4 🟡")
    
    # Billing approval
    st.subheader("🧾 Billing Approval")
    
    approval_data = [
        {"Project": "Site Alpha", "Status": "Ready", "Color": "🟢"},
        {"Project": "Site Beta", "Status": "Docs Pending", "Color": "🟡"},
        {"Project": "Site Gamma", "Status": "Overdue", "Color": "🔴"}
    ]
    
    for project in approval_data:
        with st.expander(f"{project['Color']} {project['Project']} - {project['Status']}"):
            if st.button("Approve for Billing", key=f"approve_{project['Project']}"):
                st.success(f"{project['Project']} approved for billing!")

# Billing Team Dashboard
def billing_dashboard():
    st.title("🧾 Billing Team Dashboard")
    
    st.subheader("📄 PO Processing Queue")
    
    po_queue = [
        {"PO Number": "PO-001", "Amount": "$1,500", "Status": "Ready", "Color": "🟢"},
        {"PO Number": "PO-002", "Amount": "$2,300", "Status": "Pending Docs", "Color": "🟡"},
        {"PO Number": "PO-003", "Amount": "$3,100", "Status": "Overdue", "Color": "🔴"}
    ]
    
    for po in po_queue:
        with st.expander(f"{po['Color']} {po['PO Number']} - {po['Amount']}"):
            st.write(f"**Status:** {po['Status']}")
            if st.button("Process PO", key=f"process_{po['PO Number']}"):
                st.success(f"{po['PO Number']} processed successfully!")

# GM Dashboard
def gm_dashboard():
    st.title("👑 General Manager Dashboard")
    
    # Executive overview
    st.subheader("📊 Executive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Projects", "15")
    with col2:
        st.metric("Active", "12")
    with col3:
        st.metric("Completion Rate", "75%")
    with col4:
        st.metric("Revenue", "$185K")
    
    # Status overview
    st.subheader("🎯 Project Health Status")
    
    health_data = pd.DataFrame({
        "Status": ["Normal", "At Risk", "Overdue"],
        "Count": [10, 3, 2],
        "Color": ["green", "orange", "red"]
    })
    
    # Display status cards
    cols = st.columns(3)
    status_info = [
        ("🟢 Normal", "10 projects", "All milestones on track"),
        ("🟡 At Risk", "3 projects", "Requires attention"),
        ("🔴 Overdue", "2 projects", "Immediate action needed")
    ]
    
    for idx, (title, count, desc) in enumerate(status_info):
        with cols[idx]:
            if "🟢" in title:
                st.info(f"**{title}**\n\n{count}\n\n{desc}")
            elif "🟡" in title:
                st.warning(f"**{title}**\n\n{count}\n\n{desc}")
            else:
                st.error(f"**{title}**\n\n{count}\n\n{desc}")
    
    # Simple chart
    st.subheader("📈 Department Performance")
    
    dept_data = pd.DataFrame({
        "Department": ["Field Teams", "IM", "PM", "Billing"],
        "Efficiency": [85, 70, 80, 75]
    })
    
    fig = px.bar(dept_data, x="Department", y="Efficiency", 
                 title="Department Efficiency",
                 color="Efficiency")
    st.plotly_chart(fig, use_container_width=True)

# Main app
def main():
    if st.session_state.user_role is None:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.write(f"**Role:** {st.session_state.user_role}")
            st.write(f"**User:** {st.session_state.current_user}")
            
            if st.button("Switch Role"):
                st.session_state.user_role = None
                st.rerun()
            
            st.markdown("---")
            st.markdown("### Navigation")
            st.markdown("Select different sections from main dashboard")
        
        # Route to dashboard
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
