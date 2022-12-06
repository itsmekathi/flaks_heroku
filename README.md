# Aayud home management app

1. Built do manage expenses, tasks, Contacts and To-Do lists.
2. Build with Flask, angularjs and Postgress SQL Server
3. Served through [Render](https://render.com/)

## Use of angular JS

1. The app uses Jinja python template engine as well as angularJS in the front end so parts which has `{% raw %}` is where we would be using angularJS to render.
2. The app will use the libraries from installed locally in node_modules when in development mode and load from CDN when in production.

## Setting up the application locally on Windows for the first time.

1. Install the latest version of Python. The version which is currently used to build is python 3.10.8.
2. Install the C++ build tools from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
3. Clone the repository.
4. Swith into the folder created.
5. Create a python virtual environment using
   `virtualenv venv` or `python -m venv venv`.
6. Activate the virtual environment. On windows run `venv/scripts/activate`.
7. Install the dependencies using
   `pip install -r requirements.txt`
8. To create the based database run `flask db upgrade`. This will create a sql lite db in the project folder.
9. To populate dummy data in db run `flask populateseeddata`. This will populate the lookup tables and create dummy user.
10. Switch to /app/static folder from command promp.
11. Install node dependencies using `npm install`.
12. Install Grunt cli globally `npm install -g grunt-cli`
13. Minify the JS files by running `npm run grunt-minify`
14. Run the run_dev.bat file from command prompt `run_dev.bat`
15. You should see the application come up on port 8000.
16. You change change the configuration by editing run_dev.bat file.
17. By default admin user is admin, email: admin@123.com, password: admin@123.

## Setting up on linux

### Setting up python, pip and virtualenv

1. Check whether python3 is installed by opening terminal and running `python3 --version`
2. Update the repo and install pip `sudo apt update & sudo apt install python3-pip `
3. Verify pip installation `pip3 --version`
4. Install virtualenv `apt-get install -y python3-venv`
5. Create virtual environment `python3 -m venv venv`
6. Activate the virtual environment `source venv/bin/activate`
7. Installing the requirements `pip3 install -r requirements.txt`
8. To deactivate type `deactivate`.
9. Installing nodejs `sudo apt install nodejs`
10. Verify installation `nodjs -v `
11. Installing npm `sudo apt install npm`
12. Verify installation `npm -v `

## Reference resource Links

| Resource Name                                                                              | Description                                                  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| [Angular JS UI Grid](http://ui-grid.info/docs)                                             | UI Grid component for angularJS                              |
| [Deploy flask applications to render](https://testdriven.io/blog/flask-render-deployment/) | How to deploy flask applications to render and connect to db |
| [Grunt JS](https://gruntjs.com/getting-started)                                            | Getting started with Grunt JS                                |

## Steps for production deployment.

1. Set below environment values accordingly before PAAS deployment.
   - DATABASE_URL = postgresql://user:password@server/db_name
   - FLASK_CONFIG = production
   - PYTHON_VERSION = 3.10.8

## Tools used for Development

| Tool                                                 | Description/Purpose                                                                   | Usage |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------- | ----- |
| [Sqlite Browser](https://sqlitebrowser.org/dl/)      | Used to query SQL Lite DB created locally during development.                         | Free  |
| [DBeaver](https://dbeaver.io/)                       | Used to connect to production database for querying, taking backup and restoring data | Free  |
| [Visual studio code](https://code.visualstudio.com/) | Free code editor from microsoft                                                       | Free  |

### [Live App On render](https://aayud-hms.onrender.com/)
