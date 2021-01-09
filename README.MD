## HOSPITAL-MANAGEMENT-API-REST
**DEPLOY**

 1. `$ python3 -m venv "/path/to/new/virtual/environment"`
 2. `$ source env/bin/activate`
 3. `$ pip3 install -r requirements.txt`
 4. *Open a new console and execute*
 5. `$ sudo psql -X postgres -p 5432`
 6. `$ createdb hospital -O usuario`
 7. Back to first console and execute
 8. `$ flask db init`
 9. `$ flask db migrate -m "FIRST MIGRATION"`
 10. `$ flask db upgrade` 
 11. `$ flask run`
 12. `🌈ITS MAGIC!!🌈`

**API DOCUMENTATION**
./api-routes.md - SIMPLE DOCUMENTATION

**API TESTING**

> You can try all routes with this POSTMAN Collection.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ea5dc1e6f60cdb86fa8e)