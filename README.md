## The folder called QMConnect contains all the code of QMConnect+. The application is split into two parts:
* qa
* accounts

## Tests
Before running the tests is important to be in the folder *QMConnect/myproject* (cd QMConnect/myproject)

To run the tests in the "accounts" application run the following in the terminal:
* python manage.py test accounts/tests (55 tests)

To run the tests in the "qa" application run the following in the terminal:
* python manage.py test qa/tests (41 tests)

** The tests only work by following the 2nd method from below.

# Accessing the application: 1st method (easiest method)
Go to the url [QMConnect+](http://qmconnect.herokuapp.com/)

# Accessing the application: 2nd method (harder method)
1. **Install Virtualenv**: [Virtualenv installation guide](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
2. **Create a virtual environment (go into QMConnect folder then run the following command)**: virtualenv QMConnect
3. **Activate the virtual environment by running the following command**: source QMConnect/bin/activate
4. **Install the required dependencies**: pip install -r requirements.txt
5. **Run the following in the terminal**: python manage.py runserver
6. **Open the browser and enter the following address**: http://127.0.0.1:8000/ or http://localhost:8000/ !
7. **Play with the application**

# ! - check your terminal output, you might have a different address
