import os, subprocess
from collections.abc import Callable



def run_checks(directory: str) -> Callable[[str], str]:
    dir_abs = os.path.abspath(directory)
    def inner_check(path: str) -> str:
        target_dir = os.path.normpath(os.path.join(dir_abs, path))
        valid_target_dir = os.path.commonpath([dir_abs, target_dir]) == dir_abs

        if valid_target_dir == False:
            return f'Error: Cannot execute "{path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{path}" does not exist or is not a regular file'
        if ".py" not in path:
            return f'Error: "{path}" is not a Python file'
    return inner_check


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_file_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_file_path, file_path))
        target_dir = os.path.commonpath([abs_file_path, target_file])
        check = run_checks(working_directory)(file_path)


        if check != None:
            return check

        command = ["python", target_file]
        if args != None:
            command.extend(args)

        proc = subprocess.run(args = command, cwd = target_dir, text = True, timeout = 30, capture_output=True)
        result_str = ""
        if proc.returncode != 0:
            result_str += f"Process exited with code {proc.returncode}\n"
        if len(proc.stdout) == 0 and len(proc.stderr) == 0:
            result_str += f"No output produced\n"
        else:
            result_str += f"STDOUT: {proc.stdout}\n"
            result_str += f"STDERR: {proc.stderr}\n"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return result_str



schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}
