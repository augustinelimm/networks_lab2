'''
TEST CASES are run twice to test for idempotency.

    Idempotency Testing

    - GET/items
    - GET/items/{id}
    - GET/items/items?sortBy={id/name/stock}
    - GET/items/items?count={int}
    - GET/items/items?sortBy={id/name/stock}&count={int}
    requests are idempotent because calling it many times doesn't change any data

    - POST/items{id} requests are not idempotent because requesting this many times will result in duplications with different id. Since id is auto incremented
    - DELETE/items/{id} requests are not idempotent because the item does not exists.

    Prove: After running this python file, you will see that every GET request results in the same output. Hence, all GET requests \
    are idempotent. Omitting POST 'Invalid Request', adding new_item = {"id": 187654, "name": "Slim Fit Hoodie", "stock": 150} \
    the first time indicates item is successfully created. The second time around, a validation error is thrown stating that item \
    with ID 187654 already exists. This shows that POST requests are not idempotent because it does not add it to the database after \
    the first request is done. Finally, deleting ID 187654 the first time shows that it is successful, subsequent DELETE requests of \
    the same item will indicate that item with ID 187654 is not found, meaning it has been successfully deleted the first time and \
    subsequent DELETE requests will result in the same outcome. Hence, DELETE requests are idempotent.
'''

import httpx

BASE_URL = "http://127.0.0.1:8000/items"


def print_response(response, request_type, url):
    print(f"\n{request_type} {url}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Failed to parse JSON: {e}")


with httpx.Client() as client:

    """
    GET REQUESTS
    """
    # Test GET all items with no query parameters
    response = client.get(BASE_URL)
    print_response(response, "GET", BASE_URL)
    response = client.get(BASE_URL)
    print_response(response, "GET", BASE_URL)

    # Test GET for specific id
    response = client.get(f"{BASE_URL}/237922")
    print_response(response, "GET", BASE_URL)
    response = client.get(f"{BASE_URL}/237922")
    print_response(response, "GET", BASE_URL)

    # Test GET request with sortBy query parameter (sorting by stock)
    response = client.get(BASE_URL, params={"sortBy": "stock"})
    print_response(response, "GET", f"{BASE_URL}?sortBy=stock")
    response = client.get(BASE_URL, params={"sortBy": "stock"})
    print_response(response, "GET", f"{BASE_URL}?sortBy=stock")

    # Test GET request with count parameter (limit number of items)
    response = client.get(BASE_URL, params={"count": 5})
    print_response(response, "GET", f"{BASE_URL}?count=5")
    response = client.get(BASE_URL, params={"count": 5})
    print_response(response, "GET", f"{BASE_URL}?count=5")

    # Test GET request with both sortBy and count parameters
    response = client.get(BASE_URL, params={"sortBy": "stock", "count": 3})
    print_response(response, "GET", f"{BASE_URL}?sortBy=stock&count=3")
    response = client.get(BASE_URL, params={"sortBy": "stock", "count": 3})
    print_response(response, "GET", f"{BASE_URL}?sortBy=stock&count=3")

    """
    POST REQUEST
    """
    # Test valid POST request
    new_item = {"id": 187654, "name": "Slim Fit Hoodie", "stock": 150}
    response = client.post(BASE_URL, json=new_item)
    print_response(response, "POST", BASE_URL)
    new_item = {"id": 187654, "name": "Slim Fit Hoodie", "stock": 150}
    response = client.post(BASE_URL, json=new_item)
    print_response(response, "POST", BASE_URL)

    # Test invalid POST request (missing name)
    invalid_item = {"id": 888888, "stock": 200}
    response = client.post(BASE_URL, json=invalid_item)
    print_response(response, "POST (Invalid Request)", BASE_URL)

    # Test invalid POST request (missing stock)
    invalid_item = {"id": 888888, "name": "Skinny Jeans"}
    response = client.post(BASE_URL, json=invalid_item)
    print_response(response, "POST (Invalid Request)", BASE_URL)

    # Test invalid POST request (negative stock)
    invalid_item_stock = {"id": 888889, "name": "Invalid Stock Item", "stock": -5}
    response = client.post(BASE_URL, json=invalid_item_stock)
    print_response(response, "POST (Invalid Stock)", BASE_URL)

    # Test invalid POST request (duplicate ID)
    duplicate_item = {"id": 100000, "name": "Duplicate Item", "stock": 300}
    response = client.post(BASE_URL, json=duplicate_item)
    print_response(response, "POST (Duplicate ID)", BASE_URL)

    '''
    DELETE REQUEST
    '''
    # Test valid delete request
    response = client.delete(f"{BASE_URL}/187654")
    print_response(response, "DELETE", f"{BASE_URL}/items")
    response = client.delete(f"{BASE_URL}/187654")
    print_response(response, "DELETE", f"{BASE_URL}/items")

    # Test invalid DELETE request (deleting a non-existent item)
    response = client.delete(f"{BASE_URL}/234123")
    print_response(response, "DELETE (Invalid Request)", f"{BASE_URL}/187654")
