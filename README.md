# Mimir API
## What is Mimir?
Mimir is a Microservice REST API used to pull data from the University of Lincoln Timetabling systems and parse it into a usable format by parts of the Asgard system stack. Mimir is written in Python (Version 3), using the Flask web microframework and its RESTful extension.

Mimir takes its name from Norse mythology, where Mimir was a wise and all knowing advisor to the gods.

<br>

---

## Repository Structure
UNDER CONSTRUCTION

<br>

---

## Dependencies
The template uses the pip3 package manager and is written using Python3.

The following packages are used in the project:

### API - Flask - 1.0.3
Flask is the web microframework the application was developed to use as its core. It supplies all the main functionality and networking.

### API - Flask-RESTful - 0.3.7
Flask-RESTful is an extension to the Flask framework allowing for the easy configuration of REST architecture APIs. This handles our endpoint definition and opening the application up to the different query verb types.

### API - mysqlclient - 1.4.6
MySQL client is required for SQLAlchemy to interact with MySQL databases.

### API - Flask-SQLAlchemy - 2.4.0
Flask-SQLAlchemy is a Flask wrapper for the Object-Relational Mapper, SQLAlchemy. SQLAlchemy provides the toolset we use to interact with the MySQL database used by the API and provide a layer of security between the API and the raw data itself.

### API - Flask-Jsonpify - 1.5.0
Jsonify is our json parser, this package is what converts our result data from the database into the JSON responses we reply to our connected clients.

### API - Flask-Cors - 3.0.8
Flask-Cors is an extension package for routing and managing Cross-Origin Resource Sharing (CORS) across the application, and is mainly used to allow our web client to interact with the API itself.

### API - Webargs - 5.3.2
Webargs handles the parameter parsing from the endpoint URLs to usable data within our Flask resource objects, this library replaces the now depreciated "reqparse" from Flask-RESTful.

### API - Marshmellow - 3.0.1
Marshmellow is a dependency of Webargs, we had to freeze this at this version due to something on their end stopping working correctly.

### API - Nose2 - 0.9.1
Nose2 is an extension of the Python Unit-test module, we use this as part of our unit, feature and integration testing. The project is set to export the results of these tests as JUnit XML files.

<br>

---

## Commands
### Pip3
Batch Install the Pip3 modules at their frozen version by the following commands whilst in the projects root directory.
```pip3
pip3 install -r api/requirements.txt
```

<br>

---

## Testing
Under Construction

<br>

---

## Installation
Under Construction

<br>

---

## Usage Guide - API Interactions and Endpoints

### Exposed Endpoints
Valid Endpoints
```
<server_address>/mimir-api/timetables
<server_address>/mimir-api/bookings
<server_address>/mimir-api/timetable_handler
<server_address>/mimir-api/booking_handler
```

Example Endpoints
```
10.5.11.173/mimir-api/timetables
10.5.11.173/mimir-api/bookings
10.5.11.173/mimir-api/timetable_handler
10.5.11.173/mimir-api/booking_handler
```

### Endpoint - Timetables List
Usage:
```
<server_address>/mimir-api/timetables

Supported HTTP Methods
* GET
```

params:
```
N/A
```

#### GET method
The GET method for the Timetable list endpoint returns a JSON array listing the timetables registered with Mimir.

Usage:
```
GET -> <server_address>/mimir-api/timetables
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://mimir-api/timetables"
    },
    "data": {
        "timetables":[
            {
                "bookings":[],
                "id": 1,
                "timetable": "timetable_example"
            }
        ]
    }
}
```

### Endpoint - Bookings List
Usage:
```
<server_address>/mimir-api/bookings

Supported HTTP Methods
* GET
```

params:
```
timetable - String name of the timetable to list the bookings from
```

#### GET method
The GET method for the Bookings list endpoint returns a JSON array listing the bookings for a given timetable.

Usage:
```
GET -> <server_address>/mimir-api/bookings?timetable=timetable_example
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://mimir-api/bookings"
    },
    "data": {
        "bookings":[
            {
                "booking": "test_booking",
                "cell_colour": "#a2b0b8",
                "duration": 8.0,
                "end_time": "Tue, 14 Jan 2020 17:00:00 GMT",
                "id": 2,
                "start_time": "Tue, 14 Jan 2020 09:00:00 GMT",
                "timetable": "timetable_example",
                "timetable_id": 1
            }
        ]
    }
}
```

### Endpoint - Timetable Handler
Usage:
```
<server_address>/mimir-api/timetable_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the timetable to get
```

POST
```
name - The friendly name for the timetable
```

PUT
```
id - The integer id of the timetable to update
new_name - The new name for the timetable
```

DELETE
```
id - The integer id of the timetable to delete
```

#### GET method
The GET method for the timetable_handler endpoint returns a JSON object representing a serialised version of the timetable.

Usage:
```
GET -> <server_address>/mimir-api/timetable_handler?id=1
```

Response Codes:
```
200 - Ok
404 - Timetable not found
422 - Invalid Parameters
```

Example Response:
```JSON
{
    "meta":{},
    "links":{
        "self": "http://mimir-api/timetable_handler?id=1"
    },
    "data": {
        "timetable": {
            "bookings":[],
            "id": 1,
            "timetable": "timetable_example"
        }
    }
}
```

#### POST method
The POST method for the timetable_handler endpoint allows the creation of a new timetable.

Usage:
```
POST -> <server_address>/mimir-api/timetable_handler
```

Response Codes:
```
201 - Created
422 - Timetable of that name already exists
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "name": "Example Timetable"
}
```

#### PUT method
The PUT method for the timetable_handler endpoint allows for changes to be made to a timetable's data.

Usage:
```
PUT -> <server_address>/mimir-api/timetable_handler
```

Response Codes:
```
202 - Accepteds
405 - Timetable does not exist
422 - Timetable of that name already exists
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "id": 1,
    "name": "Renamed Example Timetable"
}
```

#### DELETE method
The DELETE method for the timetable_handler endpoint allows for the deletion of a specified timetable.

Usage:
```
DELETE -> <server_address>/mimir-api/timetable_handler?id=1
```

Response Codes:
```
202 - Success
404 - Timetable not found
422 - Invalid Parameters
```

### Endpoint - Booking Handler
Usage:
```
<server_address>/mimir-api/booking_handler

Supported HTTP Methods
* GET
* POST
* PUT
* DELETE
```

params:

GET
```
id - The integer id of the booking to get
```

POST
```
timetable
name - The name for the session
start - The Date/Time the session starts at
end - The Date/Time the session end at
colour - The colour of the session on the timetable frontend
```

PUT
```
id - The integer id of the booking to update
name - The new name for the session
colour - The new colour of the session on the timetable frontend
```

DELETE
```
id - The integer id of the booking to delete
```

#### GET method
The GET method for the booking_handler endpoint returns a JSON object representing a serialised version of the booking.

Usage:
```
GET -> <server_address>/mimir-api/booking_handler?id=1
```

Response Codes:
```
200 - Ok
404 - Booking not found
422 - Invalid Parameters
```

Example Response:
```JSON
 {
    "meta":{},
    "links":{
        "self": "http://mimir-api:5000/booking_handler?id=1"
    },
    "data":{
        "booking":{
            "booking": "Test Booking",
            "cell_colour": "#a2b0b8",
            "duration": 8.0,
            "end_time": "Mon, 13 Jan 2020 17:00:00 GMT",
            "id": 1,
            "start_time": "Mon, 13 Jan 2020 09:00:00 GMT",
            "timetable": "Example Timetable",
            "timetable_id": 4
        }
    }
}
```

#### POST method
The POST method for the booking_handler endpoint allows the creation of a new booking.

Usage:
```
POST -> <server_address>/mimir-api/booking_handler
```

Response Codes:
```
201 - Created
422 - booking of that name already exists
422 - Invalid Parameters
422 - Start and end date must match
422 - End time must be after start time
422 - A booking already exists at that time
```

Example Request Body:
```JSON
{
    "timetable": "Example Timetable",
    "name": "Example Booking",
    "start": "2019-09-17T09:00:00+00:00",
    "end": "2019-09-17T10:00:00+00:00",
    "colour": "#FFFFFF"
}
```

#### PUT method
The PUT method for the booking_handler endpoint allows for changes to be made to a booking's data.

Usage:
```
PUT -> <server_address>/mimir-api/booking_handler
```

Response Codes:
```
202 - Accepted
404 - Booking not found
422 - Invalid Parameters
```

Example Request Body:
```JSON
{
    "id": 1,
    "name": "New Example Booking",
    "colour": "#F1FFFF"
}
```

#### DELETE method
The DELETE method for the booking_handler endpoint allows for the deletion of a specified booking.

Usage:
```
DELETE -> <server_address>/mimir-api/booking_handler?id=1
```

Response Codes:
```
202 - Success
404 - booking not found
422 - Invalid Parameters
```
