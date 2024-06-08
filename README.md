# BAP-MortgageCalculator

## Description
The Mortgage Calculator aims to provide ways to store mortgage data and get analysis for these mortgages. With built-in database connections, support for user authentication, and multi-mortgage support, this tool offers a more robust solution compared to other mortgage calculators. It allows users to analyze, graph, and amortize mortgages, with the ability to edit mortgages at set points in time.

## Features
 - Analysis and Graphing: Comprehensive analysis and visualization of mortgage data.
 - Amortization: Detailed amortization schedules for each mortgage.
 - Editable Mortgages: Ability to edit mortgage details at specific points in time.
 - Multi-Mortgage Support: Manage and analyze multiple mortgages simultaneously.
 - Database Integration: Secure storage of mortgage data with built-in database connections.
 - User Authentication: Secure login and management of user accounts.

## Installation

### Prerequisites
Before you begin, ensure you have the follwing installed:
 - Python 3.8 or higher
 - PostgreSQL

### Environment Setup
1. Download the Repository:
   Download the ZIP file from the repository and extract it to your desired location.
2. Navigate to the Project Directory:
   ``` sh
   cd path/to/mortgage-calculator
   ```
3. Create a Virtual Environment:
   ``` sh
   python -m venv venv
   ven\Scripts\activate
   ```
4. Install Dependencies:
   ``` sh
   pip install -r requirements.txt
   ```

### Database Configuration
1. Install PostgresSQL:
 - Follw the instructions on the [official PostgresSQL website](https://www.postgresql.org/download/) to install PostgresSQL on your machine.
2. Configure Database Connection:
 - Update the database connection settings in the 'dbhandler.py' and 'initial/startup.py'.

``` python
conn = psycopg2.connect(
            dbname="MortgageCalculator",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
```

### Running the Application
Start the apllcation by running this in the directory the project is located in. This will also setup the database on first run.
``` sh
flask run
```

### Accessing the Application
Open your web browser and go to 'http://127.0.0.1:5000' to see the application in action.

## Usage
1. Create an Account:
 - Register for an account to securely store and manage your mortgage data.
2. Add a Mortgage:
 - Input mortgage details, including principal, interest rate, term, and start date.
3. View Analysis:
 - Analyze your mortgage data with detailed graphs and amortization schedules.
4. Apply Transactions:
 - Make changes to your mortgage by applying transactions, such as additional payments or interest rate adjustments.
