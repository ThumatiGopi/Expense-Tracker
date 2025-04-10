# Setting Up Email Notifications

To enable email notifications in the expense tracker, you'll need to set up your Gmail account to work with the application. Here's a step-by-step guide:

## 1. Generate an App Password for Gmail

1. Go to your Google Account settings: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Under "2-Step Verification", make sure it's enabled
4. Scroll down and click on "App passwords"
5. Select "Mail" as the app and "Windows Computer" (or your device type) as the device
6. Click "Generate"
7. Copy the 16-character password that appears

This app-specific password is what you'll use in the application, NOT your regular Gmail password.

## 2. Setting Environment Variables

### For Windows (Command Prompt):

1. Open Command Prompt
2. Run these commands, replacing the values with your information:
```cmd
setx SMTP_SERVER smtp.gmail.com
setx SMTP_PORT 587
setx SMTP_USERNAME "your-gmail@gmail.com"
setx SMTP_PASSWORD "your-16-char-app-password"
```
3. Close and reopen Command Prompt for changes to take effect

### For Windows (PowerShell):

1. Open PowerShell
2. Run these commands:
```powershell
[Environment]::SetEnvironmentVariable("SMTP_SERVER", "smtp.gmail.com", "User")
[Environment]::SetEnvironmentVariable("SMTP_PORT", "587", "User")
[Environment]::SetEnvironmentVariable("SMTP_USERNAME", "your-gmail@gmail.com", "User")
[Environment]::SetEnvironmentVariable("SMTP_PASSWORD", "your-16-char-app-password", "User")
```
3. Close and reopen PowerShell for changes to take effect

### For Linux/Mac:

1. Open your terminal
2. Edit your shell profile file (~/.bashrc, ~/.zshrc, etc.):
```bash
nano ~/.bashrc  # or ~/.zshrc for Zsh
```

3. Add these lines at the end of the file:
```bash
export SMTP_SERVER='smtp.gmail.com'
export SMTP_PORT='587'
export SMTP_USERNAME='your-gmail@gmail.com'
export SMTP_PASSWORD='your-16-char-app-password'
```

4. Save the file and reload it:
```bash
source ~/.bashrc  # or source ~/.zshrc for Zsh
```

## 3. Verify Setup

To verify that your environment variables are set correctly:

### Windows (Command Prompt):
```cmd
echo %SMTP_USERNAME%
```

### Windows (PowerShell):
```powershell
$env:SMTP_USERNAME
```

### Linux/Mac:
```bash
echo $SMTP_USERNAME
```

## 4. Running the Application

After setting up the environment variables, you can run the application:

```bash
streamlit run src/app.py
```

The application will now be able to send email notifications when budget thresholds are reached.

## Troubleshooting

1. If you receive "Authentication failed" errors:
   - Make sure you're using the app password, not your regular Gmail password
   - Double-check that the username matches your Gmail address exactly

2. If emails aren't being sent:
   - Verify environment variables are set correctly
   - Check if your antivirus or firewall is blocking the connection
   - Make sure port 587 is not blocked by your network

3. If you get "Variable not found" errors:
   - Try restarting your terminal/command prompt
   - Verify the variables are set in the current environment
   - On Windows, you might need to log out and log back in
