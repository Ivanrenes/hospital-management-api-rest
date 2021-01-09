## HOSPITAL-MANAGEMENT-API-REST
**DEPLOY**

 1. `$ python3 -m venv "/path/to/new/virtual/environment"`
 2. `$ source env/bin/activate`
 3. `$ pip3 install -r requirements.txt`
 4. *Open a new console and execute*
 5. `$ sudo psql -X postgres -p 5432`
 6. `$ createdb hospital -O usuario`
 7. change __init____.py  for your user db and password`'postgresql://usuario:password@localhost:5432/hospital'`
 8. Save Changes
 9. Back to first console and execute
 10. `$ flask db init`
 11. `$ flask db migrate -m "FIRST MIGRATION"`
 12. `$ flask db upgrade` 
 13. `$ flask run`
 14. `🌈ITS MAGIC!!🌈`

**API DOCUMENTATION**
./api-routes.md - SIMPLE DOCUMENTATION

**API TESTING**

> You can try all routes with POSTMAN.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ea5dc1e6f60cdb86fa8e)