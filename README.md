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
2. Run the API using Docker
```sh
docker-compose up --build
```
3. (Optional) If running locally without Docker
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

