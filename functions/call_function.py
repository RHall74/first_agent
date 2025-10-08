# python
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    # Read function_call_part.name and function_call_part.args.
    function_name = function_call_part.name
    kwargs = dict(function_call_part.args) # shallow copy
    
    # Merge {"working_directory": "./calculator"} into the args.
    kwargs["working_directory"] = "./calculator" 

    # Print the appropriate line(s) if verbose is True or False.
    if verbose:
        print(f"Calling function: {function_name}({kwargs})")
    else:
        print(f" - Calling function: {function_name}")

    # Build a dict: function name (string) -> callable (your four functions).
    dispatch = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # If name not in the dict, return a types.Content with an error via from_function_response.
    if function_name not in dispatch:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Call the function with **args, capture the result.
    result = dispatch[function_name](**kwargs)

    # Wrap the result into a types.Content with from_function_response.
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )




    