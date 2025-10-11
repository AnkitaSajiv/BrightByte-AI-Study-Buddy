from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Make a test request
response = client.models.generate_content(
    model="gemini-2.5-flash",  # You can also try "gemini-2.5-pro"
    contents="Explain how photosynthesis works in simple terms."
)

print(response.text)
