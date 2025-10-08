from google.genai import types
import os


def write_file(working_directory, file_path, content):
    # Normalize and compare paths robustly:
    full_path = os.path.join(working_directory, file_path) # Joined relative path
    abs_work_dir_path = os.path.abspath(working_directory) # Absolute path for working directory
    abs_file_path = os.path.abspath(full_path) # Absolute path for file path

    # LLM guardrails: restricts access to only the "working_directory" we give it.
    if not (abs_file_path == abs_work_dir_path or abs_file_path.startswith(abs_work_dir_path + os.sep)): # Check if the file path is contained in working_directory
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    # Ensure parent directories exist when the file/dirs don’t:
    parent = os.path.dirname(abs_file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
        
    try:
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


# Schema that tells the LLM how to use the function
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file at a given path within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to write."
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to write into the file."
            ),
        },
        required=["file_path", "content"],
    ),
)
