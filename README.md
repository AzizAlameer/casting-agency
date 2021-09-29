# casting-agency
Udacity capstone project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

# API URL 
- **Heroku:** `https://morning-brushlands-62267.herokuapp.com/`
- **Localhost:** base URL is `http://127.0.0.1:5000/`

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
ensure you are working using your created virtual environment.
change the DATABASE_URL to the one you created in setup.sh and run the following

```bash
source setup.sh
```

```bash
python manage.py db upgrade
python manage.py seed
```

### Running the server

After initializing your virables run:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: Method Not Allowed

### Endpoints 
A postman collection provided to test both Local and heroku server with all variables provided
(test-postman-local.postman_collection) 

#### GET /movies

- General:
    - Returns all movies.
    - Roles:Casting Assistant,Casting Director,Executive Produce
- Sample: `curl http://127.0.0.1:5000/movies`

```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sat, 06 May 2000 00:00:00 GMT",
            "title": "Gladiator"
        },
        {
            "id": 2,
            "release_date": "Fri, 09 Feb 1979 00:00:00 GMT",
            "title": "The Warriors"
        }
    ],
    "success": true
}

```

#### GET /actors
- General:
    - returns all actors
    - Roles:Casting Assistant,Casting Director,Executive Produce.
- Sample:  `curl http://127.0.0.1:5000/actors`
```
{
    "actors": [
        {
            "age": 54,
            "gender": "male",
            "id": 1,
            "name": "Vin Diesel"
        },
        {
            "age": 57,
            "gender": "male",
            "id": 2,
            "name": "Brad Pitt"
        }
    ],
    "success": true
}

```
#### POST /actors
- General:
    - posts an actor
    - Roles:Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{
	"name": "Maha",
	"age": 23,
	"gender": "female"
}'`

```
{
    "actor": {
        "age": 23,
        "gender": "female",
        "id": 4,
        "name": "Maha"
    },
    "success": true
}

```
#### PATCH /actors/\<int:id\>
- General:
    - updates actors
    - Roles:Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/2 -X POST -H "Content-Type: application/json" -d '{
	"name": "Khalid",
	"age": 22,
	"gender": "male"
```
{
    "actor": {
        "age": 22,
        "gender": "male",
        "id": 2,
        "name": "Khalid"
    },
    "success": true
}

```
#### DELETE /actors/<int:id\>

- General:
    - deletes an actor
    - Roles:Executive Producer,Casting Director.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```
{
    "deleted": "3",
    "success": true
}

```
#### POST /movies

- General:
    - posts a movie.
    - Roles: Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{
	"title": "moviemovie",
	"release_date": "2020-10-06"
}'`

```

{
    "movie": {
        "id": 3,
        "release_date": "Mon, 05 Oct 2020 21:00:00 GMT",
        "title": "moviemovie"
    },
    "success": true
}

```

#### PATCH /movies/\<int:id\>

- General:
    - patches a movie
    -Roles:Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{
	"title": "moviemovie 2",
	"release_date": "2020-10-07"
}'`

```
{
    "movie": {
        "id": 3,
        "release_date": "Tue, 06 Oct 2020 21:00:00 GMT",
        "title": "moviemovie 2"
    },
    "success": true
}
```
#### DELETE /movies/<int:id\>


- General:
  - Deletes a movie.
  - Roles: Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/1 -X DELETE`


```
{
    "deleted": "1",
    "success": true
}
```

## Testing
To run the tests,  delete and create your db and run the following
```
python manage.py db upgrade
python manage.py seed
python test_app.py
```