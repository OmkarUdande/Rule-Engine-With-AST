# Rule Engine

## Overview :=

    This project is a Rule Engine built using Django, designed to evaluate user-defined rules based on specific attributes
    such as age, department, salary, and experience. It allows users to create, combine, and modify rules dynamically and
    evaluates user eligibility based on these rules.

## Features :=

- Create and validate complex rules using various logical conditions.
- Supports combining multiple rules using AND/OR operators.
- Evaluates rules against user attributes to determine eligibility.
- User-friendly web interface for rule management and evaluation.

## Installation

### Requirements :=

Before you begin, ensure you have the following installed on your machine:

- **Python**: Version 3.x
- **Django**: Version 3.x or higher
- **Django REST Framework**: For building RESTful APIs
- **Requests** library: For making HTTP requests

### Steps to Install:=

**1.**

### Clone the Repository :=

    First, clone the repository to your local machine using Git. Open your terminal or command prompt and run:

--> git clone <repository-url>
cd rule-engine

**2**

### Install Dependencies :=

    Install the required Python packages using pip. Make sure you have a requirements.txt file in your project directory:

    --> pip install -r requirements.txt <--

**3**

### Migrations :=

    Run Migrations Make sure your database is set up and run the migrations:

--> python manage.py migrate <--

**4**
Start the Server You can start the Django development server using:

    --> python manage.py runserver <--
