# Aayud home management app
1. Built do manage expenses, tasks, Contacts and To-Do lists.
2. Build with Flask, angularjs and Postgress SQL Server
3. Served through [Render](https://render.com/)


## Use of angular JS
1. The app uses Jina as well as angularJS in the front end so parts which has ```{% raw %}``` is where we would be using angularJS to give it a SPA fee.
2. The app will use the libraries from installed local node_modules when in development mode so make sure the node packages are installed.

## Setting up the application locally on Windows
1. Install the latest version of Python. The latest version is build with python 3.10.8.
2. Clone the repository.
3. Swith into the folder created.
4. Create a python virtual environment using 
``` virtualenv venv ```
5. Activate the virtual environment. On windows run ```venv/scripts/activate```.
5. Install the dependencies using
``` pip install -r requirements.txt ```
7. To create the based database run ```flask db upgrade```. This will create a sql lite db in the project folder.
8. To populate dummy data in db run ```flask populateseeddata```. This will populate the lookup tables and create dummy user.
9. By default admin user is admin, email: admin@123.com, password: admin@123. 
6. Run the run_dev.bat file from command prompt ```run_dev.bat```
8. You should see the application come up on port 8000.
9. You change change the configuration by editing run_dev.bat file.

## Setting up on linux
### Setting up python, pip and virtualenv
1. Check whether python3 is installed by opening terminal and running ```python3 --version```
2. Update the repo and install pip ```sudo apt update & sudo apt install python3-pip ```
3. Verify pip installation ```pip3 --version```
4. Install virtualenv ```apt-get install -y python3-venv```
5. Create virtual environment ```python3 -m venv venv```
6. Activate the virtual environment ```source venv/bin/activate```
7. Installing the requirements ```pip3 install -r requirements.txt```
8. To deactivate type ```deactivate```.
8. Installing nodejs ```sudo apt install nodejs```
9. Verify installation ```nodjs -v ```
10. Installing npm ```sudo apt install npm```
11. Verify installation ```npm -v ```

## Seting up angularjs part before deployment
1. Switch into /app/static folder from command promp.
2. Install node dependencies using ``` npm install ```
3. Before making a prod release make sure you minify the files by running ```npm run grunt-minify```

## Reference resource Links
Resource Name | Description
--------------|--------------
[Angular JS UI Grid](http://ui-grid.info/docs) | UI Grid component for angularJS
[Deploy flask applications to render](https://testdriven.io/blog/flask-render-deployment/)| How to deploy flask applications to render and connect to db

## Steps for production deployment
1. Set below environment values accordingly before PAAS deployment.
    * DATABASE_URL = postgresql://user:password@server/db_name
    * FLASK_CONFIG = production
    * PYTHON_VERSION = 3.10.8

### [Live App On render](https://aayud-hms.onrender.com/)