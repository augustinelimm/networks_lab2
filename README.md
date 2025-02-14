# Clothing Stock API
## Decription

This is a FastAPI-based RESTful API that manages clothing stock. The API allows users to retrieve, add, update, delete, upload files, and authenticate users based on roles.

## Features

- CRUD Operations: Create, Read, Update, and Delete clothing items.
- Sorting: Sort items by id, name, or stock, and limit results.
- File Upload: Supports file uploads using multipart/form-data.
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
then run:
```
uvicorn main:app --reload
```

## API Endpoints

### GET Requests
 - GET / - API Welcome Message
 - GET /items - Retrieve all items
 - GET /items/{id} - Retrieve a specific item by ID
 - GET /items?sortBy={id,name,stock}&count={int} - Sort and limit items

 ### POST Requests
 - POST /items - Add a new item
 - POST /uploadfile/ - Upload a file (multipart/form-data)
 Example:
```
curl -X POST "http://127.0.0.1:8000/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Oversized T-Shirt", "stock": 200}'
```
### PUT Requests
- PUT /items/{id} - Update an existing item
Example:
```
curl -X PUT "http://127.0.0.1:8000/items/156442" \
     -H "Content-Type: application/json" \
     -d '{"id": "156442", "name": "Long Sleeve T-Shirt", "stock": 181}'
```
### DELETE Requests
- DELETE /items/{id} - Delete an item by ID
Example:
```
curl -X DELETE "http://127.0.0.1:8000/items/187654"
```
### Authentication DELETE (Admin-Only Routes)
```
curl -X DELETE "http://127.0.0.1:8000/admin/items/100001" \
     -H "Authorization: {password}"
```

## Idempotency Test

- GET/items
- GET/items/{id}
- GET/items/items?sortBy={id/name/stock}
- GET/items/items?count={int}
- GET/items/items?sortBy={id/name/stock}&count={int} requests are idempotent because calling it many times doesn't change any data

- POST/items{id} requests are not idempotent because requesting this many times will result in duplications with different id. Since id is auto incremented
- DELETE/items/{id} requests are not idempotent because the item does not exists.

Prove: After running test_api.py, you will see that every GET request results in the same output. Hence, all GET requests are idempotent. Omitting POST 'Invalid Request', adding new_item = {"id": 187654, "name": "Slim Fit Hoodie", "stock": 150} the first time indicates item is successfully created. The second time around, a validation error is thrown stating that item with ID 187654 already exists. This shows that POST requests are not idempotent because it does not add it to the database after the first request is done. Deleting ID 187654 the first time shows that it is successful, subsequent DELETE requests of the same item will indicate that item with ID 187654 is not found, meaning it has been successfully deleted the first time. Hence, DELETE requests are also not idempotent because subsequent DELETE request after the first does not perform deletion again.

## Testing with .http files
This API supports HTTP request testing with .http files.

### Example with GET count request
```
GET http://127.0.0.1:8000/items?count=5 HTTP/1.1
```
If you are using VSCode, you can install 'REST Client' extension by Huachao Mao

