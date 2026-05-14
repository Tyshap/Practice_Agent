import os

from google.genai import types

def get_file_content(working_directory, file_path):
    absoluteDirectory = os.path.abspath(working_directory)
    targetDirectory = os.path.normpath(os.path.join(absoluteDirectory, file_path))
    validPath = os.path.commonpath([absoluteDirectory, targetDirectory]) == absoluteDirectory
    if not validPath:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(targetDirectory):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        file = open(targetDirectory)
        content = file.read(10000)
        if file.read(1):
            content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the content (at most {10000} characters) of a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)