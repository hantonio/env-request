# flask-music-db

Example extracted from:
* https://www.blog.pythonlibrary.org/2017/12/12/flask-101-getting-started/
* https://www.blog.pythonlibrary.org/2017/12/12/flask-101-adding-a-database/
* https://www.blog.pythonlibrary.org/2017/12/13/flask-101-how-to-add-a-search-form/
* https://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing-and-displaying-data/
* https://www.blog.pythonlibrary.org/2017/12/15/flask-101-filtering-searches-and-deleting-data/

## Useful commands

### Create database

python db_creator.py

### Run the application in development mode

export FLASK_ENV="development"
FLASK_APP=main.py flask run

### Run the application in production mode

export FLASK_ENV="production"
FLASK_APP=main.py flask run

Server will be exposed at http://127.0.0.1:5000
