import os

def record(file):
    name = file.split("/")[-1] 
    size = os.path.getsize(file)
    is_dir = os.path.isdir(file)

    return f'{name}: file_size={size} bytes, is_dir={is_dir}'

def list_files(target_dir: str) -> str:
    paths = os.listdir(target_dir) 
    new_paths = []

    for file in paths:
        new_paths.append(record(os.path.join(target_dir, file)))

    return "- " + "\n- ".join(new_paths)




def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        return list_files(target_dir)

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
