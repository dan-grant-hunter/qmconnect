## The folder called QMConnect is split into two other folders:
* myproject - contains all the code of QMConnect (split further into two folders - **qa** and **accounts**)
* QMConnectVirtualEnvironment - the virtual environment for the application (used to run the application)

# Accessing the application: 1st method (easiest method)
Go to the url [QMConnect+](http://qmconnect.herokuapp.com/)

# Accessing the application: 2nd method
1. **Install Virtualenv**: [Virtualenv installation guide for Linux/Windows/MacOS](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
2. **Go into QMConnect folder**
3. **Activate the virtual environment by running the following command**: source QMConnectVirtualEnvironment/bin/activate
4. **Go into "myproject"**
5. **Run the application**: python manage.py runserver

# Accessing the application: 3rd method (hardest method)
1. **Install Virtualenv**: [Virtualenv installation guide for Linux/Windows/MacOS](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
2. **Create a virtual environment (go into QMConnect folder then run the following command)**: virtualenv qmconnectvenv
3. **Activate the virtual environment by running the following command**: source qmconnectvenv/bin/activate
4. **Go into "myproject"**
5. **Install the required dependencies**: pip install -r requirements.txt
6. **Run the application**: python manage.py runserver
7. **Open the browser and enter the following address**: http://127.0.0.1:8000/ or http://localhost:8000/ !

*! - check your terminal output, you might have a different address*

## Tests
Before running the tests, it is important to be in the folder *QMConnect/myproject* (cd QMConnect/myproject)

To run the tests in the "accounts" application (55 tests) run the following in the terminal:
* **python manage.py test accounts/tests**

To run the tests in the "qa" application (41 tests) run the following in the terminal:
* **python manage.py test qa/tests**

To run all tests (96 tests) in one go:
* **python manage.py test accounts/tests qa/tests**

**The above commands (tests) only work by following the 2nd or 3rd method from above.**
