# python

import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    # Normalize and compare paths robustly:
    full_path = os.path.join(working_directory, file_path) # Joined relative path
    abs_work_dir_path = os.path.abspath(working_directory).rstrip(os.sep) # Absolute path for working directory
    abs_file_path = os.path.abspath(full_path) # Absolute path for file path

    # LLM guardrails: restricts access to only the "working_directory" we give it.
    if not (abs_file_path == abs_work_dir_path or abs_file_path.startswith(abs_work_dir_path + os.sep)): # Check if the file path is contained in working_directory
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_file_path): # Check if the file path is a file
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith(".py"): # Check if the file is a python file
        return(f'Error: "{file_path}" is not a Python file.')

    # Run the file
    try:
        cmd = [sys.executable, abs_file_path, *args] # Use the current Python interpreter (sys.executable) so environments match
        # Run it and capture text, from the working directory
        result = subprocess.run(
            cmd,
            cwd=abs_work_dir_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    
    stdout = result.stdout or ""
    stderr = result.stderr or ""

    if not stdout.strip() and not stderr.strip():
        return "No output produced."

    lines = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]
    if result.returncode != 0:
        lines.append(f"Process exited with code {result.returncode}")

    return "\n".join(lines)