from google import genai
from google.genai import types
from dotenv import load_dotenv
from sys import argv, exit
import os


def main():
    if len(argv) < 2:
        print('Usage: python main.py "<your prompt here>"')
        exit(1)
    load_dotenv(dotenv_path="key.env")
    api_key = os.environ.get("GEMINI_API_KEY") 
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=argv[1])])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages
    )
    
    # Print token usage details if verbose flag is set
    if len(argv) > 2 and argv[2] == "--verbose":
        print(f"User prompt: {argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
