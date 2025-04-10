import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import calendar
from database import Database
from utils.alerts import AlertManager

# Initialize database and alert manager
db = Database()
alert_manager = AlertManager()

def init_session_state():
    """Initialize session state variables"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'email' not in st.session_state:
        st.session_state.email = None

def login_signup():
    """Handle user authentication"""
    st.title("Expense Tracker - Login/Signup")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        if st.button("Login"):
            user = db.get_user(login_username)
            if user:
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.email = user[2]
                st.success(f"Welcome back, {user[1]}!")
                st.rerun()
            else:
                st.error("User not found!")
    
    with col2:
        st.subheader("Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_email = st.text_input("Email")
        if st.button("Sign Up"):
            user_id = db.add_user(new_username, new_email)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = new_username
                st.session_state.email = new_email
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error("Username already exists!")

def log_expense():
    """Expense logging section"""
    st.subheader("Log New Expense")
    
    col1, col2 = st.columns(2)
    
    with col1:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        description = st.text_input("Description")
        
    with col2:
        category = st.selectbox("Category", ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Others'])
        date = st.date_input("Date", datetime.now())
    
    if st.button("Add Expense"):
        category_id = db.get_category_id(category)
        expense_id = db.add_expense(st.session_state.user_id, category_id, amount, description, date.strftime('%Y-%m-%d'))
        
        if expense_id:
            st.success("Expense added successfully!")
            
            # Check budget threshold and send alert if needed
            month_start = date.replace(day=1)
            budget_status = db.get_budget_status(st.session_state.user_id, month_start)
            
            for status in budget_status:
                if status[1] == category:  # category_name
                    budget = status[2]  # budget amount
                    total_spent = status[3]  # current spent (already includes new expense)
                    
                    if alert_manager.check_budget_threshold(total_spent, budget):
                        alert_message = alert_manager.generate_budget_alert(category, total_spent, budget)
                        alert_manager.send_email_alert(
                            st.session_state.email,
                            f"Budget Alert - {category}",
                            alert_message
                        )
                        st.warning(f"Budget alert for {category}! Check your email for details.")
                    break

def set_budget():
    """Budget setting section"""
    st.subheader("Set Monthly Budget")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = st.selectbox("Category", ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Others'], key="budget_category")
    
    with col2:
        current_year = datetime.now().year
        current_month = datetime.now().month
        month_options = [f"{calendar.month_name[m]} {current_year}" for m in range(1, 13)]
        selected_month = st.selectbox("Month", month_options, index=current_month-1)
        month_date = datetime.strptime(selected_month, "%B %Y")
    
    with col3:
        amount = st.number_input("Budget Amount ($)", min_value=0.0, step=10.0, key="budget_amount")
    
    if st.button("Set Budget"):
        category_id = db.get_category_id(category)
        if category_id and db.set_budget(st.session_state.user_id, category_id, amount, month_date):
            st.success(f"Budget set for {category} - {selected_month}")
        else:
            st.error("Failed to set budget!")

def view_reports():
    """Reports and analytics section"""
    st.subheader("Expense Reports")
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Get expense data
    expenses = db.get_expenses(
        st.session_state.user_id,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    if expenses:
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(expenses, columns=['id', 'user_id', 'category_id', 'amount', 'description', 'date', 'category_name'])
        
        # Summary statistics
        total_spent = df['amount'].sum()
        st.metric("Total Spending", f"${total_spent:.2f}")
        
        # Spending by category pie chart
        fig1 = px.pie(df, values='amount', names='category_name', title='Spending by Category')
        st.plotly_chart(fig1)
        
        # Daily spending line chart
        df['date'] = pd.to_datetime(df['date'])
        daily_spending = df.groupby('date')['amount'].sum().reset_index()
        daily_spending = daily_spending.sort_values('date')
        fig2 = px.line(daily_spending, x='date', y='amount', title='Daily Spending', markers=True)
        st.plotly_chart(fig2)
        
        # Budget comparison
        month_date = end_date.replace(day=1)
        budget_status = db.get_budget_status(st.session_state.user_id, month_date)
        
        st.subheader("Budget Status")
        budget_data = []
        for status in budget_status:
            category_name = status[1]
            budget = status[2]
            spent = status[3]
            percentage = (spent / budget * 100) if budget > 0 else 0
            
            budget_data.append({
                'Category': category_name,
                'Budget': budget,
                'Spent': spent,
                'Remaining': budget - spent,
                'Percentage Used': f"{percentage:.1f}%"
            })
        
        st.table(pd.DataFrame(budget_data))
    else:
        st.info("No expenses found for the selected date range.")

def manage_groups():
    """Group expense management section"""
    st.subheader("Group Expenses")
    
    # Create new group
    with st.expander("Create New Group"):
        group_name = st.text_input("Group Name")
        if st.button("Create Group"):
            group_id = db.create_group(group_name, st.session_state.user_id)
            if group_id:
                st.success("Group created successfully!")
            else:
                st.error("Failed to create group!")
    
    # View group expenses
    groups = db.get_user_groups(st.session_state.user_id)
    
    if groups:
        selected_group = st.selectbox(
            "Select Group",
            options=[group[1] for group in groups],
            key="group_selector"
        )
        
        group_id = next(group[0] for group in groups if group[1] == selected_group)
        group_expenses = db.get_group_expenses(group_id)
        
        if group_expenses:
            df = pd.DataFrame(group_expenses, columns=[
                'id', 'user_id', 'category_id', 'amount', 'description',
                'date', 'category_name', 'paid_by_user'
            ])
            
            st.write("Group Expenses:")
            st.dataframe(df[['date', 'description', 'amount', 'category_name', 'paid_by_user']])
            
            # Group expense summary
            total_spent = df['amount'].sum()
            st.metric("Total Group Spending", f"${total_spent:.2f}")
            
            # Spending by member pie chart
            fig = px.pie(df, values='amount', names='paid_by_user', title='Spending by Member')
            st.plotly_chart(fig)
        else:
            st.info("No expenses recorded for this group yet.")
    else:
        st.info("You haven't created any groups yet.")

def main():
    """Main application"""
    st.set_page_config(page_title="Expense Tracker", layout="wide")
    init_session_state()
    
    if not st.session_state.user_id:
        login_signup()
    else:
        st.title(f"Welcome, {st.session_state.username}!")
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()
        
        # Main navigation
        pages = {
            "Log Expense": log_expense,
            "Set Budget": set_budget,
            "View Reports": view_reports,
            "Group Expenses": manage_groups
        }
        
        selection = st.sidebar.radio("Navigate", list(pages.keys()))
        pages[selection]()

if __name__ == "__main__":
    main()
