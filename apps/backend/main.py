"""
This main file will serve as the entry point for the backend and relays the request to the appropriate router to process it further.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Testing String" : "Hello World !!"}
# Microservice for the user related operations (Login, Signup, Profile Management, etc.)
# 1. Login Route
# 2. Signup Route
# 3. User Profile Route
# 4. Password Reset Route
# 5. Email Verification Route
# 6. Mobile Verification Route
# 7. Two-Factor Authentication Route
# 8. Google OAuth Route
# 9. GitHub OAuth Route

# Microservice related to the readme generation
