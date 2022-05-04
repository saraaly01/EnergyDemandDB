[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6874734&assignment_repo_type=AssignmentRepo)

### CAB Energy Demand Project
- Provides a database that holds information of TCNJ building's and their enegry consumption. Webview component to query database. 
- Allows TCNJ sustainbility team a simple view to access TCNJ building data.
- Implements PostgreSQL and Python Flask. 

### Steps for Installation
1. Navigate to ```src/``` and run setup.sh
  ```./bash setup.sh```
2. Navigate to web_app/ and run the following commands:
  ```
  FLASK_APP=app.py
  flask run
  ```
3. Input the following url ```127.0.0.1:5000``` in any modern web-browser
4. "Enjoy this brilliant application we made" -Andrew

### Steps for Deleting the Database 
1. Navigate to ```src/``` and run: ```./bash drop.sh ```
2. Done. It's as easy as that.
