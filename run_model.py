
import os
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Configuration with validation
endpoint = os.getenv("ENDPOINT_URL", "https://aifoundry-bundai-101.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Validate required configuration
if not subscription_key:
    print("❌ Error: AZURE_OPENAI_API_KEY environment variable is not set.")
    print("\nTo fix this issue:")
    print("1. Copy '.env.example' to '.env'")
    print("2. Edit '.env' and add your Azure OpenAI API key")
    print("3. Run the script again")
    print("\nExample:")
    print("  cp .env.example .env")
    print("  # Edit .env file with your actual API key")
    sys.exit(1)

print(f"✅ Using endpoint: {endpoint}")
print(f"✅ Using deployment: {deployment}")
print("✅ API key found")

# Initialize Azure OpenAI client with key-based authentication
try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=subscription_key,
        api_version="2025-01-01-preview",
    )
    print("✅ Azure OpenAI client initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Azure OpenAI client: {e}")
    sys.exit(1)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "I am going to Paris, what should I see?"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:\n\n1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.\n2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.\n3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.\n\nThese are just a few of the many attractions that Paris has to offer. With so much to see and do, it's no wonder that Paris is one of the most popular tourist destinations in the world."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What is so great about #1?"
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
try:
    print("🔄 Generating completion...")
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    print("✅ Completion generated successfully")
    print("\n" + "="*50)
    print("RESPONSE:")
    print("="*50)
    print(completion.choices[0].message.content)
    print("="*50)
    
except Exception as e:
    print(f"❌ Error generating completion: {e}")
    sys.exit(1)
    