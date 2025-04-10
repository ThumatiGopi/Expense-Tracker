# Setting up a Python Virtual Environment

A virtual environment (venv) is an isolated Python environment that helps manage project dependencies separately. Here's how to set it up:

## Windows

1. Create a virtual environment:
```cmd
python -m venv venv
```

2. Activate the virtual environment:
```cmd
venv\Scripts\activate
```

You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Run the application:
```cmd
streamlit run src/app.py
```

5. To deactivate when you're done:
```cmd
deactivate
```

## Linux/Mac

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run src/app.py
```

5. To deactivate when you're done:
```bash
deactivate
```

## Troubleshooting

1. If `python -m venv venv` fails:
   - Make sure Python is installed and in your PATH
   - On Ubuntu/Debian, you might need to install:
     ```bash
     sudo apt-get install python3-venv
     ```
   - On Windows, make sure you have the latest Python version

2. If activation fails:
   - On Windows, you might need to run:
     ```cmd
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - On Linux/Mac, ensure you have execute permissions:
     ```bash
     chmod +x venv/bin/activate
     ```

3. If pip install fails:
   - Upgrade pip first:
     ```bash
     python -m pip install --upgrade pip
     ```
   - Make sure you're in the virtual environment (should see `(venv)` in prompt)

## Best Practices

1. Always activate the virtual environment before working on the project
2. Keep requirements.txt updated when adding new dependencies
3. Don't commit the `venv` directory to version control (it should be in .gitignore)
4. Create a new virtual environment for each Python project
