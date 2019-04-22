## The folder called QMConnect contains all the code of QMConnect+. The application is split into two parts:
* qa
* accounts

## Tests
Before running the tests is important to be in the folder *QMConnect/myproject* (cd QMConnect/myproject)

To run the tests in the "accounts" application run the following in the terminal:
* python manage.py test accounts/tests (55 tests)

To run the tests in the "qa" application run the following in the terminal:
* python manage.py test qa/tests (41 tests)

# Accessing the application: 1st method (easiest method)
Go to the url * [QMConnect+](http://qmconnect.herokuapp.com/)

# Accessing the application: 2nd method (harder method)
1. **Install Anaconda or Miniconda to be able to access the application from the terminal**
2. **Create a virtual environment**: conda create --name QMConnect
3. **Run the following in the terminal**: conda activate QMConnect
4. **Run the following in the terminal**: pip install -r requirements.txt --user
5. **Run the following in the terminal**: python manage.py runserver
6. **Open the browser and enter the following address**: http://127.0.0.1:8000/ or http://localhost:8000/ !
7. **Play with the application**

# ! - check your terminal output, you might have a different address
