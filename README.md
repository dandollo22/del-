# DELIVERY SERVICE

## Introduction

This is an implementation of a service that takes an order and schedules the order and inserts it in the DB. Running the
app will result in creating the tables filling them with the data of restaurants,customers and riders. It computes the
orders' responses and inserts them in the table.

## 📂 Project Structure

```
src
├── data                     # The folder containing json files and database files
|     └── ...
├── app.py                   # Application main file
├── database.py              # Database transactions
├── exceptions.py            # Custom defined exception
├── helper.py                # Helper functions
├── models.py                # Pydantic Data models
├── routes.py                # Controllers for defined endpoints
├── schemas.py               # Database schemas
├── services.py              # All app logic is defined
│         
├── Dockerfile
├── docker-compose.yaml   
|
├── README.md
|
├── .gitignore
└── 

```

## ⚙ Building and running the project

- Run the docker-compose by running the command  ```docker-compose up -d```
- Insert the data json files in the data folder with the paths corresponding to the ones in the app.py
- Run the app.py
- Access URL http://localhost:8000/docs
