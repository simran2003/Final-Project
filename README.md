# Final-Project
# **Database Interaction with PostgreSQL and Python**

#### This  is a Python application designed to interact with a PostgreSQL database for managing student records. It supports basic CRUD (Create, Read, Update, Delete) operations on member,trainer,administrartive staff data, including members should be able to register and manage their profiles, establish personal fitness goals, and input health
metrics. They have access to a personalized dashboard that tracks exercise routines, fitness achievements,and health statistics. Members can schedule, reschedule, or cancel personal training sessions with certified trainers. Additionally, they are be able to register for group fitness classes.Trainers should have the ability to manage their schedules and view member profiles.Administrative Staff are equipped with features to manage room bookings, monitor fitness equipmentmaintenance, update class schedules, oversee billing, and process payments for membership fees, personal training sessions, and other services

###### **Simran Datta - 101278046**


## Requirements
Ensure you have the following installed
- Python 3.x
- PostgreSQL

## Application Set up
- **Clone Repo to local machine**
  - ```git clone https://github.com/simran2003/a3-comp3005.git```
- **Install psycopg2 from the terminal**
  - ```pip3 install psycopg2```

## Database Set up
- **Create and name a database using pgAdmin (or PostgreSQL command line)**
  - In the browser panel on the left, right-click on Databases and select Create > Database
  - Name the new database "gym" and click Save (Note you can name whatever you want)
- **Run the SQL commands in the CreatingTables.sql to set up database schema and insert initial data**
  - Right-click on the database name in pgAdmin.
  - Choose Query Tool to open an SQL editor window.
  - In the Query Tool, click on the Open File button and choose the ```CreatingTables.sql``` file in the database directory in the FINAL PROJECT folder.
  - Once the file is open in the editor, click on the green Run button to execute the SQL commands

## Running Application

#### 1. Run the application
  - Run the code.py file
  -```python3 project.py```

## YouTube Link
[Video Demonstration](https://youtu.be/KxRqQsONG8M?si=rypbwk3MK878Wl9O)





