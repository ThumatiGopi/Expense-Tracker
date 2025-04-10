import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class AlertManager:
    def __init__(self):
        # Email configuration should be set through environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')

    def send_email_alert(self, to_email, subject, message):
        """Send an email alert to the user if email is configured"""
        # Check if email is configured
        if not all([self.smtp_username, self.smtp_password]):
            print("Email notifications are not configured. Skipping email alert.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            print("You can set up email notifications by following the instructions in email_setup.md")
            return False

    def check_budget_threshold(self, spent, budget, threshold=0.9):
        """
        Check if spending has exceeded the threshold percentage of budget
        Returns True if threshold is exceeded
        """
        if budget <= 0:
            return False
        return (spent / budget) >= threshold

    def generate_budget_alert(self, category, spent, budget, threshold=0.9):
        """Generate a budget alert message"""
        percentage = (spent / budget) * 100 if budget > 0 else 0
        remaining = budget - spent
        
        message = f"""Budget Alert for {category}

Current Status:
- Spent: ${spent:.2f}
- Budget: ${budget:.2f}
- Remaining: ${remaining:.2f}
- Used: {percentage:.1f}%

{'Warning: You have exceeded your budget!' if spent > budget else f'Warning: You have used {percentage:.1f}% of your budget!'}

This is an automated notification from your expense tracker.
"""
        return message

    def generate_monthly_summary(self, expenses_by_category, budgets):
        """Generate a monthly summary report"""
        today = datetime.now()
        
        message = f"""Monthly Expense Summary - {today.strftime('%B %Y')}

Expense Breakdown by Category:
"""
        total_spent = 0
        total_budget = 0
        
        for category, data in expenses_by_category.items():
            spent = data.get('spent', 0)
            budget = budgets.get(category, 0)
            total_spent += spent
            total_budget += budget
            
            message += f"\n{category}:"
            message += f"\n- Spent: ${spent:.2f}"
            message += f"\n- Budget: ${budget:.2f}"
            message += f"\n- {'Over budget' if spent > budget else 'Within budget'}"
            
        message += f"\n\nTotal Spending: ${total_spent:.2f}"
        message += f"\nTotal Budget: ${total_budget:.2f}"
        
        return message
