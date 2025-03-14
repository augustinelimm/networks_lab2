# Clothing Stock API
## Description

This is a FastAPI-based RESTful API that manages clothing stock. The API allows users to retrieve, add, update, delete, upload files, and authenticate users based on roles.

## Features

- CRUD Operations: Create, Read, Update, and Delete clothing items.
- Sorting: Sort items by id, name, or stock, and limit results.
- Batch Delete: Instead of deleting one item at a time, you can delete several at a time.
- Authentication: Admin-only protected routes via request headers.
- Idempotency Handling: Ensures GET requests are idempotent while POST & DELETE are not.

## Installation & Setup

This project uses Docker for deployment. Follow these steps:

1. Clone the Repository
```sh
git clone https://github.com/augustinelimm/networks_lab2.git

```
2. Create a .env file
This application uses a MySQL database to store data. The init.sql file will automatically execute SQL commands to initialize the database with predefined data. Replace placeholders with MySQL credentials to allow the application to connect to MySQL.
For Mac/Linux users
```sh
touch .env
```
For Windows
```
echo > .env
```
```
DATABASE_URL=mysql+pymysql://<your_username>:<your_password>@db/items_db
ADMIN_PASSWORD=<your_admin_password>
MYSQL_ROOT_PASSWORD=<your_sql_root_password>
MYSQL_DATABASE=items_db
MYSQL_USER=<your_mysql_user>
MYSQL_PASSWORD=<your_mysql_password>
```
3. Run the API using Docker
```sh
docker-compose up --build
```
4. (Optional) If running locally without Docker
```sh
pip install -r requirements.txt
```
```
uvicorn main:app --reload
```

## API Endpoints

### GET Requests

 - GET / - API Welcome Message
 ```
 curl -X GET "http://127.0.0.1:8000/"
 ```
 - GET /items - Retrieve all items
 ```
 curl -X GET "http://127.0.0.1:8000/items"
 ```
 - GET /items/{id} - Retrieve a specific item by ID
 ```
 curl -X GET "http://127.0.0.1:8000/items/100000"
 ```
 - GET /items?sortBy={id,name,stock}&count={int} - Sort and limit items
 ```
 curl -X GET "http://127.0.0.1:8000/items?sortBy=id&count=5"
 ```

 ### POST Requests

 - POST /items - Add a new item

```
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Oversized T-Shirt", "stock": 200}'
```

### PUT Requests

- PUT /items/{id} - Update an existing item

```
curl -X PUT "http://127.0.0.1:8000/items/156442" \
     -H "Content-Type: application/json" \
     -d '{"id": "156442", "name": "Long Sleeve T-Shirt", "stock": 181}'
```

### DELETE Requests

- DELETE /items/{id} - Delete an item by ID

```
curl -X DELETE "http://127.0.0.1:8000/items/187654"
```

### Batch DELETE

```
curl -X DELETE "http://127.0.0.1:8000/items/batch-delete/" \
     -H "Content-Type: application/json" \
     -d '{"item_ids": [100000, 101836, 111023]}'
```

### Authentication DELETE (Admin-Only Routes)

```
curl -X DELETE "http://127.0.0.1:8000/admin/items/234222" \
     -H "Authorization: {password}"
```

## Idempotent or Non-Idempotent routes

These routes should always produce the same result no matter how often it is called.

| Route | Method | Idempotent? | Reason|
|-------|--------|--------------|------|
|GET /items/ | GET |Yes|Always returns the same items unless modified by another request|
|GET /items/{id}|GET|Yes|Always returns the same items unless modified by another request|
|DELETE /items/batch-delete|DELETE|Yes|If there are no items in the database, repeated request will be the same as requesting it once|
|DELETE /items/{id}|DELETE|Yes|If there are no items in the database, repeated request will be the same as requesting it once|
|POST /items/|POST|No|Each request creates a new item|
|PUT /items/{id}|PUT|No|	Updates a item's details, modifying the database.|

## Testing with .http files

This API supports HTTP request testing with .http files.

### Example with GET count request

```
GET http://127.0.0.1:8000/items?count=5 HTTP/1.1
```
If you are using VSCode, you can install 'REST Client' extension by Huachao Mao

