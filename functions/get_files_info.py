import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory) # Joined relative path
    abs_work_dir_path = os.path.abspath(working_directory) # Absolute path for working directory
    abs_full_path = os.path.abspath(full_path) # Transforms joined path into absolute path
    
    # LLM guardrails: restricts access to only the "working_directory" we give it.
    if not abs_full_path.startswith(abs_work_dir_path): # Check if the directory is contained in working_directory
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_full_path): # Check if the path is a valid directory
        return(f'Error: "{directory}" is not a directory')
    
    # Gather directory contents (files and child directories)
    try:
        path_list = os.listdir(abs_full_path)
        path_details = []
        for path in path_list:
            if os.path.isfile(os.path.join(abs_full_path, path)) or os.path.isdir(os.path.join(abs_full_path, path)):
                file_size = os.path.getsize(os.path.join(abs_full_path, path))
                is_dir = os.path.isdir(os.path.join(abs_full_path, path))
                path_details.append(f'- {path}: file_size={file_size} bytes, is_dir={is_dir}')

        return("\n".join(path_details))
    except OSError as e:
        return(f"Error: OSError {e}")