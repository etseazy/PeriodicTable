# Periodic Table Information System

## Overview
The **Periodic Table Information System** is a structured database system designed to provide accurate details about the **atomic number and atomic mass** of **S and P block elements**. This project is implemented using **Python and SQL** to efficiently manage and retrieve element data.

## Features
- Stores **S and P block elements** with atomic details.
- **SQL queries** for accurate data retrieval.
- **Python-based interface** for querying element information.
- Supports **stored procedures** for efficient data handling.

## Project Structure
```
PeriodicTable/
│── interface/                 # UI files for interaction
│── database/                  # SQL schema, queries, and procedures
│   │── schema.sql             # Database schema setup
│   │── procedures.sql         # Stored procedures
│   │── queries.sql            # Queries for retrieving data
│── main.py                    # Python script for database interaction
│── README.md                  # Project documentation
│── requirements.txt           # Dependencies
```

## Setup Instructions
### 1 Clone the Repository
```bash
git clone https://github.com/etseazy/PeriodicTable.git
cd PeriodicTable
```

### 2 Database Setup
1. Open **SQL Server Management Studio (SSMS)**.
2. Execute **schema.sql** to create the database and tables.
3. Execute **procedures.sql** to add stored procedures.
4. Use **queries.sql** to test data retrieval.

### 3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 4 Run the Application
```bash
python main.py
```

## How to Use
- Enter an element’s **symbol** or **atomic number** to get its details.
- Query atomic properties using the Python interface.
- Modify the SQL files to update or expand the element database.

## Technologies Used
- **Python** (for interaction)
- **SQL Server** (for database management)
- **SQL Queries & Stored Procedures** (for optimized data retrieval)

