from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from contextlib import asynccontextmanager
import uvicorn
import logging

# ------------------ Logging Setup --------------------
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ------------------ In-memory store --------------------
pets: Dict[int, dict] = {}
users: Dict[str, dict] = {}
orders: Dict[int, dict] = {}

def load_sample_data():
    logger.debug("Loading sample data...")
    pets.clear()
    pets.update({
        1: {"id": 1, "name": "Rex", "category": {"id": 1, "name": "Dog"}, "photoUrls": ["rex.jpg"], "tags": [{"id": 1, "name": "friendly"}], "status": "available"},
        2: {"id": 2, "name": "Whiskers", "category": {"id": 2, "name": "Cat"}, "photoUrls": ["whiskers.jpg"], "tags": [{"id": 2, "name": "cute"}], "status": "sold"},
        3: {"id": 3, "name": "Tweety", "category": {"id": 3, "name": "Bird"}, "photoUrls": ["tweety.jpg"], "tags": [{"id": 3, "name": "small"}], "status": "pending"},
    })
    users.clear()
    users.update({
        "alice": {"id": 1, "username": "alice", "firstName": "Alice", "lastName": "Wonder", "email": "alice@example.com", "password": "alicepwd", "phone": "1234567890", "userStatus": 1},
        "bob": {"id": 2, "username": "bob", "firstName": "Bob", "lastName": "Builder", "email": "bob@example.com", "password": "bobpwd", "phone": "0987654321", "userStatus": 1},
    })
    orders.clear()
    orders.update({
        1: {"id": 1, "petId": 1, "quantity": 1, "shipDate": "2025-07-04T10:00:00Z", "status": "approved", "complete": True},
    })
    logger.debug("Sample data loaded.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting application lifespan...")
    load_sample_data()
    yield
    logger.debug("Ending application lifespan...")

app = FastAPI(title="Petstore In-Memory Mock Server", lifespan=lifespan)

@app.post("/reset")
def reset():
    logger.debug("Resetting sample data...")
    load_sample_data()
    return {"message": "Sample data reloaded."}

# ------------------ Pets Endpoints ---------------------

@app.post("/pet", status_code=201)
async def add_pet(pet: dict):
    logger.debug(f"Adding pet: {pet}")
    pid = pet.get("id")
    if not pid or pid in pets:
        logger.error(f"Invalid or duplicate pet id: {pid}")
        raise HTTPException(400, "Invalid or duplicate pet id")
    pets[pid] = pet
    logger.debug(f"Pet added: {pet}")
    return pet

@app.put("/pet")
async def update_pet(pet: dict):
    logger.debug(f"Updating pet: {pet}")
    pid = pet.get("id")
    if not pid or pid not in pets:
        logger.error(f"Pet not found: {pid}")
        raise HTTPException(404, "Pet not found")
    pets[pid] = pet
    logger.debug(f"Pet updated: {pet}")
    return pet

# ------------------ STATIC ROUTES MUST COME BEFORE DYNAMIC ---------------------

@app.get("/pet/findByStatus")
async def find_pets_by_status(status: str = Query("available")):
    logger.debug(f"Finding pets by status: {status}")
    result = [pet for pet in pets.values() if pet.get("status") == status]
    logger.debug(f"Pets found: {result}")
    return result

@app.get("/pet/findByTags")
async def find_pets_by_tags(tags: List[str] = Query([])):
    logger.debug(f"Finding pets by tags: {tags}")
    result = []
    for pet in pets.values():
        pet_tags = [tag["name"] for tag in pet.get("tags", [])]
        if any(tag in pet_tags for tag in tags):
            result.append(pet)
    logger.debug(f"Pets found: {result}")
    return result

@app.get("/pet/{petId}")
async def get_pet(petId: int):
    logger.debug(f"Fetching pet with ID: {petId}")
    pet = pets.get(petId)
    if not pet:
        logger.error(f"Pet not found: {petId}")
        raise HTTPException(404, "Pet not found")
    logger.debug(f"Pet fetched: {pet}")
    return pet

@app.delete("/pet/{petId}")
async def delete_pet(petId: int):
    logger.debug(f"Deleting pet with ID: {petId}")
    if petId not in pets:
        logger.error(f"Pet not found: {petId}")
        raise HTTPException(404, "Pet not found")
    del pets[petId]
    logger.debug(f"Pet deleted: {petId}")
    return {"message": "Pet deleted"}

# ------------------ Store Endpoints ---------------------

@app.get("/store/inventory")
async def get_inventory():
    logger.debug("Fetching inventory...")
    inventory = {"available": 0, "pending": 0, "sold": 0}
    for pet in pets.values():
        status = pet.get("status")
        if status in inventory:
            inventory[status] += 1
    logger.debug(f"Inventory: {inventory}")
    return inventory

@app.post("/store/order", status_code=201)
async def place_order(order: dict):
    logger.debug(f"Placing order: {order}")
    oid = order.get("id")
    if not oid:
        logger.error("Order must have an id")
        raise HTTPException(400, "Order must have an id")
    orders[oid] = order
    logger.debug(f"Order placed: {order}")
    return order

@app.get("/store/order/{orderId}")
async def get_order(orderId: int):
    logger.debug(f"Fetching order with ID: {orderId}")
    order = orders.get(orderId)
    if not order:
        logger.error(f"Order not found: {orderId}")
        raise HTTPException(404, "Order not found")
    logger.debug(f"Order fetched: {order}")
    return order

@app.delete("/store/order/{orderId}")
async def delete_order(orderId: int):
    logger.debug(f"Deleting order with ID: {orderId}")
    if orderId not in orders:
        logger.error(f"Order not found: {orderId}")
        raise HTTPException(404, "Order not found")
    del orders[orderId]
    logger.debug(f"Order deleted: {orderId}")
    return {"message": "Order deleted"}

# ------------------ User Endpoints ---------------------

@app.post("/user", status_code=201)
async def create_user(user: dict):
    logger.debug(f"Creating user: {user}")
    uname = user.get("username")
    if not uname or uname in users:
        logger.error(f"Invalid or duplicate username: {uname}")
        raise HTTPException(400, "Invalid or duplicate username")
    users[uname] = user
    logger.debug(f"User created: {user}")
    return user

@app.post("/user/createWithList", status_code=201)
async def create_users_with_list(users_list: List[dict]):
    logger.debug(f"Creating users with list: {users_list}")
    for user in users_list:
        uname = user.get("username")
        if uname and uname not in users:
            users[uname] = user
    logger.debug(f"Users created: {users_list}")
    return users_list

@app.get("/user/{username}")
async def get_user(username: str):
    logger.debug(f"Fetching user with username: {username}")
    user = users.get(username)
    if not user:
        logger.error(f"User not found: {username}")
        raise HTTPException(404, "User not found")
    logger.debug(f"User fetched: {user}")
    return user

@app.put("/user/{username}")
async def update_user(username: str, user: dict):
    logger.debug(f"Updating user with username: {username}, data: {user}")
    if username not in users:
        logger.error(f"User not found: {username}")
        raise HTTPException(404, "User not found")
    users[username] = user
    logger.debug(f"User updated: {user}")
    return user

@app.delete("/user/{username}")
async def delete_user(username: str):
    logger.debug(f"Deleting user with username: {username}")
    if username not in users:
        logger.error(f"User not found: {username}")
        raise HTTPException(404, "User not found")
    del users[username]
    logger.debug(f"User deleted: {username}")
    return {"message": "User deleted"}

@app.get("/user/login")
async def login_user(username: Optional[str] = None, password: Optional[str] = None):
    logger.debug(f"Logging in user: username={username}, password={password}")
    if username in users and users[username]["password"] == password:
        logger.debug("Login successful")
        return "logged in"
    logger.error("Invalid username/password supplied")
    raise HTTPException(400, "Invalid username/password supplied")

@app.get("/user/logout")
async def logout_user():
    logger.debug("Logging out user...")
    return "logged out"

# ------------------ Root ---------------------

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed.")
    return {"status": "Petstore mock server running."}

if __name__ == "__main__":
    logger.debug("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=10000)
