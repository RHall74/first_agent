from config import MAX_CHARS # e.g., 10000
from google.genai import types
import os



def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path) # Joined relative path
    abs_work_dir_path = os.path.abspath(working_directory) # Absolute path for working directory
    abs_file_path = os.path.abspath(full_path) # Absolute path for file path

    # LLM guardrails: restricts access to only the "working_directory" we give it.
    if not abs_file_path.startswith(abs_work_dir_path + os.sep): # Check if the file path is contained in working_directory
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_file_path): # Check if the path is a valid file
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    try:
        with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(MAX_CHARS + 1) # read a sentinel extra char
    except Exception as e:
        return f"Error: {e}"
    
    if len(content) > MAX_CHARS:
        content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
    
    return content


# Schema that tells the LLM how to use the function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents of file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read.",
            ),
        },
        required=["file_path"],
    ),
)
