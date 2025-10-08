# python
from dotenv import load_dotenv
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from google import genai
from google.genai import types
import os
from sys import argv, exit



def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    # Create a list of all the available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

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
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    # Print token usage details if verbose flag is set
    if len(argv) > 2 and argv[2] == "--verbose":
        print(f"User prompt: {argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    verbose = len(argv) > 2 and argv[2] == "--verbose"

    print("Response:")
    if response.function_calls:
        function_call_part = response.function_calls[0] # Grab the function call(s).
        function_call_result = call_function(function_call_part, verbose=verbose) # Call the function call(s).

        # Validate the structure
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or function_call_result.parts[0].function_response.response is None
        ):
            raise RuntimeError("Function call returned an invalid tool response")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(response.text)


if __name__ == "__main__":
    main()
