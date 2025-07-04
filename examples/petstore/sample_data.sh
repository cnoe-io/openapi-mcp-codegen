#!/bin/bash

BASE_URL="http://localhost:10000"

echo "Adding sample pets..."

curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 1, "name": "Rex", "category": {"id": 1, "name": "Dog"}, "photoUrls": ["https://example.com/rex.jpg"], "tags": [{"id": 1, "name": "friendly"}], "status": "available"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 2, "name": "Whiskers", "category": {"id": 2, "name": "Cat"}, "photoUrls": ["https://example.com/whiskers.jpg"], "tags": [{"id": 2, "name": "cute"}], "status": "sold"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 3, "name": "Tweety", "category": {"id": 3, "name": "Bird"}, "photoUrls": ["https://example.com/tweety.jpg"], "tags": [{"id": 3, "name": "small"}], "status": "available"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 4, "name": "Fang", "category": {"id": 1, "name": "Dog"}, "photoUrls": ["https://example.com/fang.jpg"], "tags": [{"id": 4, "name": "big"}], "status": "pending"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 5, "name": "Fluffy", "category": {"id": 2, "name": "Cat"}, "photoUrls": ["https://example.com/fluffy.jpg"], "tags": [{"id": 5, "name": "white"}], "status": "available"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 6, "name": "Spike", "category": {"id": 1, "name": "Dog"}, "photoUrls": ["https://example.com/spike.jpg"], "tags": [{"id": 6, "name": "guard"}], "status": "sold"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 7, "name": "Goldie", "category": {"id": 4, "name": "Fish"}, "photoUrls": ["https://example.com/goldie.jpg"], "tags": [{"id": 7, "name": "golden"}], "status": "available"
}'; echo
curl -s -X POST "$BASE_URL/pet" -H "Content-Type: application/json" -d '{
    "id": 8, "name": "Hopper", "category": {"id": 5, "name": "Rabbit"}, "photoUrls": ["https://example.com/hopper.jpg"], "tags": [{"id": 8, "name": "fast"}], "status": "pending"
}'; echo

echo "Adding sample users..."
curl -s -X POST "$BASE_URL/user" -H "Content-Type: application/json" -d '{
    "id": 1, "username": "alice", "firstName": "Alice", "lastName": "Wonder", "email": "alice@example.com", "password": "alicepwd", "phone": "1234567890", "userStatus": 1
}'; echo
curl -s -X POST "$BASE_URL/user" -H "Content-Type: application/json" -d '{
    "id": 2, "username": "bob", "firstName": "Bob", "lastName": "Builder", "email": "bob@example.com", "password": "bobpwd", "phone": "0987654321", "userStatus": 1
}'; echo
curl -s -X POST "$BASE_URL/user" -H "Content-Type: application/json" -d '{
    "id": 3, "username": "carol", "firstName": "Carol", "lastName": "Smith", "email": "carol@example.com", "password": "carolpwd", "phone": "5555555555", "userStatus": 1
}'; echo
curl -s -X POST "$BASE_URL/user" -H "Content-Type: application/json" -d '{
    "id": 4, "username": "dan", "firstName": "Dan", "lastName": "Brown", "email": "dan@example.com", "password": "danpwd", "phone": "4444444444", "userStatus": 1
}'; echo

echo "Adding sample orders..."
curl -s -X POST "$BASE_URL/store/order" -H "Content-Type: application/json" -d '{
    "id": 1, "petId": 1, "quantity": 1, "shipDate": "2025-07-04T10:00:00Z", "status": "approved", "complete": true
}'; echo
curl -s -X POST "$BASE_URL/store/order" -H "Content-Type: application/json" -d '{
    "id": 2, "petId": 4, "quantity": 2, "shipDate": "2025-07-05T10:00:00Z", "status": "placed", "complete": false
}'; echo
curl -s -X POST "$BASE_URL/store/order" -H "Content-Type: application/json" -d '{
    "id": 3, "petId": 7, "quantity": 1, "shipDate": "2025-07-06T10:00:00Z", "status": "delivered", "complete": true
}'; echo

echo "Checking inventory..."
curl -s "$BASE_URL/store/inventory"
echo

echo "Finding pets by tags..."
curl -s "$BASE_URL/pet/findByTags?tags=friendly&tags=small"
echo

echo "All done!"
