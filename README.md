# Carford Car Shop CRM
This project contains a CRM like application built using Python/Flask and Docker.


# Quickstart 
### USING DOCKER
1. Clone this repository
2. Download docker
3. Open your terminal
4. Set the root of this repo as your working directory
5. Run `docker-compose up`
6. Enter the following address in your browser of choice: `localhost:5000`

DONE!


### RUNNING LOCALLY WITHOUT DOCKER
1. Clone this repository
2. Open your terminal
3. Set the root of this repo as your working directory
4. Create a Python 3.7 virtualenv called venv `python3 -m venv venv`
5. Activate your virtualenv `source venv/bin.activate`
6. Set necessary environment variables `export FLASK_APP=carford_car_crm && export FLASK_ENV=development`
7. Run `flask run`
8. Enter the following address in your browser of choice: `localhost:5000`

DONE!


# Suggested Next Steps:
- Create unit tests for carford_car_crm/crm_utils.py
- Use class based views
- Change to a different DBMS
- Add logs
- Add list functionality for viewing data from both Person and Vehicle tables 


# Disclaimer
This projects make use of code snippets from Flask and Docker Compose tutorials.