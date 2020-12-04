# Demo-Ipstack
This is demo backend repository when using Ipstack API.

The api is hosted on heroku: https://demo-ipstack.herokuapp.com (default config) and is purely backend, meaning that there is no fronted at the moment and can be access only via requests (GET / PUT / POST / DELETE)

Before usage in user has to register or login (demo account is user_name: kuboszek, password: demo). After success one should store access key in order to make use of API.

### Additional comments
* All requests as an input uses json data,
* All records are stored on postgresql database,
* Field list to get from Ipstack is saved in env variable:
  * "ip", "continent_name", "country_code", "country_name", "region_code", "region_name", "city", "zip", "latitude", "longitude"

## Logging
### Available under https://demo-ipstack.herokuapp.com/login
### PostMan raw code example:
```
POST /login HTTP/1.1
Host: demo-ipstack.herokuapp.com
Content-Type: application/json
Content-Length: 45

{"user_name": "kuboszek", "password": "demo"}
```

## Register
### Available under https://demo-ipstack.herokuapp.com/register

On sucess login, client will get json containing access key:
```
{"access_token": "access_token", "message": "Login succesful"}
```

## Usage
### Available under https://demo-ipstack.herokuapp.com/api
Once token has been generated user can access API with standard requests. For instance when passing following json:
```
{"url": "tvn24.pl"}
```
1. GET - to retrieve url data from database (if exists, otherwise returns 404),
1. PUT - update the record (if exists, otherwise returns 404),
1. POST - to insert new record (if does not exist, otherwise return 209),
1. DELETE - to delete record from database (if exists, otherwise returns 404)

### PostMan raw code example:
```
PUT /api HTTP/1.1
Host: demo-ipstack.herokuapp.com
Authorization: Bearer example_access_token
Content-Type: application/json
Content-Length: 19

{"url": "tvn24.pl"}
```
Returns: 
```
{"message": "Record updated"}
```

## Possible further development
1. At the moment DB is not normalized with full production app it would be nice to the split redundant data,
1. At the moment all IP / URL are converted and unified into IP. If page is hosted on multiple servers (like tvn24.pl) the same url can be inserted multiple times (see also previous point),
1. Implementing frontend to support logging and managing users' URLs,
1. Add support for token reneval
