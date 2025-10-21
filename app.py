import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Telecom Project Manager",
    page_icon="🏗️",
    layout="wide"
)

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Login page
def login_page():
    st.title("🏗️ Telecom Project Manager")
    st.markdown("**Simple Demo - No Installation Required**")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🎯 Select Role")
    
    with col2:
        role = st.selectbox("Choose Dashboard", 
                           ["Field TL", "IM", "PM", "Billing Team", "GM"])
        
        if st.button("Enter Dashboard", type="primary"):
            st.session_state.user_role = role
            st.rerun()

# Status highlighting
def show_status(status, count, description):
    if status == "Normal":
        st.success(f"🟢 {status}: {count} - {description}")
    elif status == "Risk":
        st.warning(f"🟡 {status}: {count} - {description}")
    else:
        st.error(f"🔴 {status}: {count} - {description}")

# Field TL Dashboard
def field_tl_dashboard():
    st.title("👷 Field Team Lead Dashboard")
    
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
    
    # Daily Plans
    st.subheader("📋 Daily Plans")
    
    plans = [
        {"Site": "MDN2176", "Activity": "Installation", "Status": "Assigned", "Color": "🟢"},
        {"Site": "MDN2177", "Activity": "QC Check", "Status": "In Progress", "Color": "🟡"},
        {"Site": "MDN2178", "Activity": "Survey", "Status": "Overdue", "Color": "🔴"}
    ]
    
    for plan in plans:
        with st.expander(f"{plan['Color']} {plan['Site']} - {plan['Activity']}"):
            st.write(f"**Status:** {plan['Status']}")
            if st.button(f"Update {plan['Site']}", key=plan['Site']):
                st.success(f"{plan['Site']} updated!")

# IM Dashboard
def im_dashboard():
    st.title("📋 Inventory Manager Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sites", "15")
    with col2:
        st.metric("Pending Approval", "3")
    with col3:
        st.metric("Active Teams", "5")
    
    # Approval Queue
    st.subheader("✅ Approval Queue")
    
    approvals = [
        {"Activity": "Site Alpha Installation", "Status": "Pending", "Days": "1", "Color": "🟡"},
        {"Activity": "Site Beta QC", "Status": "Pending", "Days": "2", "Color": "🔴"},
        {"Activity": "Site Gamma Survey", "Status": "Approved", "Days": "0", "Color": "🟢"}
    ]
    
    for approval in approvals:
        with st.expander(f"{approval['Color']} {approval['Activity']}"):
            st.write(f"Status: {approval['Status']}")
            st.write(f"Days Pending: {approval['Days']}")
            if approval['Status'] == "Pending":
                if st.button(f"Approve {approval['Activity']}", key=f"app_{approval['Activity']}"):
                    st.success("Approved!")

# PM Dashboard
def pm_dashboard():
    st.title("💰 Project Manager Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Projects", "12")
    with col2:
        st.metric("On Track", "8")
    with col3:
        st.metric("At Risk", "4")
    
    # Billing Approval
    st.subheader("🧾 Billing Approval")
    
    projects = [
        {"Name": "Site Alpha", "Status": "Ready", "Docs": "Complete", "Color": "🟢"},
        {"Name": "Site Beta", "Status": "Docs Pending", "Docs": "Incomplete", "Color": "🟡"},
        {"Name": "Site Gamma", "Status": "Overdue", "Docs": "Missing", "Color": "🔴"}
    ]
    
    for project in projects:
        with st.expander(f"{project['Color']} {project['Name']}"):
            st.write(f"Status: {project['Status']}")
            st.write(f"Documents: {project['Docs']}")
            if st.button(f"Approve {project['Name']}", key=project['Name']):
                st.success(f"{project['Name']} approved for billing!")

# Billing Team Dashboard
def billing_dashboard():
    st.title("🧾 Billing Team Dashboard")
    
    st.subheader("📄 PO Processing Queue")
    
    pos = [
        {"PO": "PO-001", "Amount": "$1,500", "Status": "Ready", "Color": "🟢"},
        {"PO": "PO-002", "Amount": "$2,300", "Status": "Pending", "Color": "🟡"},
        {"PO": "PO-003", "Amount": "$3,100", "Status": "Overdue", "Color": "🔴"}
    ]
    
    for po in pos:
        with st.expander(f"{po['Color']} {po['PO']} - {po['Amount']}"):
            st.write(f"Status: {po['Status']}")
            if st.button(f"Process {po['PO']}", key=po['PO']):
                st.success(f"{po['PO']} processed!")

# GM Dashboard
def gm_dashboard():
    st.title("👑 General Manager Dashboard")
    
    # Executive Overview
    st.subheader("📊 Executive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Projects", "15")
    with col2:
        st.metric("Active", "12")
    with col3:
        st.metric("Completion", "75%")
    with col4:
        st.metric("Revenue", "$185K")
    
    # Status Overview
    st.subheader("🎯 Project Health Status")
    
    show_status("Normal", "10 projects", "All milestones on track")
    show_status("Risk", "3 projects", "Requires attention") 
    show_status("Overdue", "2 projects", "Immediate action needed")
    
    # Simple progress bars for departments
    st.subheader("📈 Department Performance")
    
    departments = [
        ("Field Teams", 85),
        ("IM Team", 70), 
        ("PM Team", 80),
        ("Billing", 75)
    ]
    
    for dept, score in departments:
        st.write(f"**{dept}:**")
        st.progress(score/100)
        st.write(f"{score}% efficiency")
        st.write("---")

# Main app
def main():
    if st.session_state.user_role is None:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.write(f"**Role:** {st.session_state.user_role}")
            st.write(f"**User:** {st.session_state.user_role}@company.com")
            
            if st.button("Switch Role"):
                st.session_state.user_role = None
                st.rerun()
            
            st.markdown("---")
            st.markdown("### Navigation")
            st.markdown("All features in main dashboard")
        
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
