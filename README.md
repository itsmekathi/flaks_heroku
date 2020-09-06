# Aayud home management app
> Built do manage tasks, expenses, Contacts and To-Do lists.
> Build with Flask and Postgress SQL Server

## Setting up the application locally on Windows
1. Install the latest version of Python.
2. Clone the repository.
3. Swith into the folder created.
4. Create a python virtual environment using 
``` virtual env venv ```
5. Install the dependencies using
``` pip install -r requirements.txt ```
6. Run the run_dev.bat file from command prompt ```run_dev.bat```
7. To create the based database run ```flask db upgrade```. This should create a sql lite db in the project folder.
8. You should see the application come up on port 8000.
9. You change change the configuration by editing run_dev.bat file.

## Seting up angularjs part
1. Switch into /app/static folder from command promp.
2. Install node dependencies using ``` npm install ```
3. Before making a prod release make sure you minify the files by running ```npm run grunt-minify```

## Notes
1. The app uses Jina as well as angularJS in the front end so parts which has ```{% raw %}``` is where we would be using angularJS to give it a SPA fee.
2. The app will use the libraries from installed local node_modules when in development mode so make sure the node packages are installed.

# Resource Links
Resource Name | Resource Link
--------------|--------------
Angular JS UI Grid | http://ui-grid.info/docs

## Links
[Live App On Heroku](https://aayud-hms.herokuapp.com/)
