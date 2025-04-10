# Expense Tracker Application

A Streamlit-based expense tracking application that helps users manage their expenses, set budgets, and track spending habits. The application includes features for expense logging, budget management, spending reports, and group expense sharing.

## Features

### Core Features
- User authentication and account management
- Daily expense logging with categories
- Monthly budget setting for each category
- Real-time budget tracking and alerts
- Detailed expense reports and visualizations

### Extra Credit Features
- Different budgets for different months
- Custom alerts when budget threshold is reached (90% by default)
- Email notifications for budget alerts
- Group expense sharing functionality (similar to Splitwise)

## Prerequisites

- Python 3.9 or higher
- Docker (optional, see docker_setup.md for Docker installation instructions)

## Installation and Setup

### Local Setup (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd expense-tracker
```

2. Set up a virtual environment (Recommended):
   - Follow the instructions in venv_setup.md for detailed steps
   - This ensures clean dependency management and isolation

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables for email notifications:
```bash
# Linux/Mac
export SMTP_SERVER='smtp.gmail.com'
export SMTP_PORT='587'
export SMTP_USERNAME='your-email@gmail.com'
export SMTP_PASSWORD='your-app-specific-password'

# Windows
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-specific-password
```

5. Run the application:
```bash
streamlit run src/app.py
```

## Testing Steps

1. User Authentication
   - Open the application
   - Try signing up with a new account
   - Verify login functionality
   - Test logout and session management

2. Expense Logging
   - Log a new expense with all required fields
   - Verify the expense appears in the reports
   - Test date selection functionality
   - Validate amount input constraints

3. Budget Management
   - Set monthly budgets for different categories
   - Test budget updates
   - Verify different budgets for different months work
   - Ensure budget alerts trigger appropriately

4. Reports and Analytics
   - Check if expense reports show correct totals
   - Verify pie chart and line chart data accuracy
   - Test date range filtering
   - Validate budget vs. spending comparisons

5. Group Expenses
   - Create a new expense group
   - Add group members
   - Log group expenses
   - Verify expense splitting calculations
   - Test group expense reports

6. Email Notifications
   - Set up email credentials
   - Trigger a budget alert
   - Verify email notification is received
   - Check notification content accuracy

## Edge Cases Handled

1. Database Operations
   - Concurrent user access
   - SQLite thread safety
   - Database connection management
   - Error handling for failed operations

2. Input Validation
   - Negative amounts prevention
   - Date validation
   - Required field checks
   - Duplicate username prevention

3. Budget Alerts
   - Zero budget handling
   - Multiple alerts prevention
   - Email sending failures
   - Custom threshold validation

4. Group Expenses
   - Empty group handling
   - Member removal handling
   - Expense deletion cascading
   - Split amount rounding

## Documentation

### Code Structure

```
expense-tracker/
├── src/
│   ├── app.py           # Main Streamlit application
│   ├── database.py      # Database operations & SQL queries
│   └── utils/
│       └── alerts.py    # Alert management and email notifications
├── database/            # SQLite database directory
├── Dockerfile          # Docker configuration
├── requirements.txt    # Project dependencies
└── README.md          # Documentation
```

### Database Schema

The application uses SQLite with the following tables:
- `users`: User account information
- `categories`: Expense categories
- `expenses`: Individual expense records
- `budgets`: Monthly budget settings
- `groups`: Expense sharing groups
- `group_expenses`: Group expense records

## Deployment Options

### Development URLs
When running `streamlit run src/app.py`, Streamlit provides two URLs:
- **Local URL** (`http://localhost:8501`): 
  - For accessing the app on your local machine
  - Only accessible from the computer running the application
  - Best for development and testing

- **Network URL** (`http://192.168.x.x:8501`):
  - For accessing the app from other devices on the same network
  - Useful for testing on different devices or sharing with teammates
  - The IP address will match your computer's local network IP

### Production Deployment Options

1. **Cloud Platforms**
   - **Streamlit Cloud** (Recommended):
     ```
     1. Create an account at share.streamlit.io
     2. Connect your GitHub repository
     3. Deploy with a few clicks
     ```
   
   - **Heroku**:
     ```
     1. Create a Procfile:
        web: streamlit run src/app.py
     2. Set environment variables in Heroku dashboard
     3. Deploy using Heroku CLI or GitHub integration
     ```

   - **AWS/GCP/Azure**:
     ```
     1. Set up a virtual machine
     2. Install dependencies
     3. Use systemd or supervisor to run the app
     4. Set up a reverse proxy (nginx/apache)
     ```

2. **Docker Deployment**
   ```bash
   # Build the Docker image
   docker build -t expense-tracker .
   
   # Run the container
   docker run -p 8501:8501 expense-tracker
   ```

3. **Production Considerations**
   - Use a production-grade database (PostgreSQL recommended)
   - Set up SSL/TLS for secure connections
   - Implement proper backup strategies
   - Consider using a process manager (PM2, Supervisor)
   - Set up monitoring and logging
   - Configure proper authentication for public access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request
