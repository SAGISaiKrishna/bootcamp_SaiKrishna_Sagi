import os
from dotenv import load_dotenv, find_dotenv

# Load the nearest .env so it works no matter where you open the notebook from
load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")
