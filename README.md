# ctx

Have you ever wanted to ask a question about a project to a LLM but lost a lot of time trying to explain the structure of the project and the relevant files? 

`ctx` is a command-line tool that allows you to recursively print the file tree of a specified directory, display contents of specified files, and ignore certain paths or the entire tree. It's useful for quickly understanding the structure and content of a project in the context of a question.

## Features

- **Recursively print file trees**: Visualize the directory structure of your project.
- **Display file contents**: Easily view the contents of specified files.
- **Ignore paths**: Exclude certain files or directories from the tree.
- **Ignore entire tree**: Focus solely on specified files without displaying the tree.
- **Specify line ranges**: Display specific lines from files.

## Installation

You can install `ctx` via pip:

```bash
pip install ctx
```

This will install the `ctx` package and make the `ctx` command available globally.

## Usage

```bash
ctx [OPTIONS] [FILE_PATHS...]
```

### Options

- `--cwd <path>`: Change the current working directory. Defaults to the current directory.
- `-ip`, `--ignore-path <path>`: Paths to ignore in the file tree (relative to cwd or absolute). Can be used multiple times to ignore multiple paths.
- `-it`, `--ignore-tree`: Ignore the entire tree and only display specified files.

### Arguments

- `FILE_PATHS`: One or more files to display contents of if they exist in the tree. You can specify line numbers using the format `path:start_line:end_line`.

### Examples

#### Display the file tree and the contents of specific files

```bash
ctx README.md ctx/main.py
```

#### Display contents of specific lines in a file (e.g., lines 10 to 20)

```bash
ctx ctx/main.py:10:20
```

#### Ignore the tree and only display contents of specified files

```bash
ctx --ignore-tree README.md
```

#### Ignore specific paths when displaying the tree

```bash
ctx --ignore-path=folder1 --ignore-path=folder2
```

#### Display the file tree of a specified directory

```bash
ctx --cwd=/path/to/directory
```

## Development

If you want to run `ctx` in development mode or contribute to the project, follow these steps.

### Clone the repository

```bash
git clone https://github.com/asnunes/ctx.git
cd ctx
```

### Install dependencies

Make sure you have Python 3 installed. It's recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### Install the package in editable mode

```bash
pip install -e .
```

### Run the script

```bash
ctx [OPTIONS] [FILE_PATHS...]
```

Or directly via Python:

```bash
python ctx/main.py [OPTIONS] [FILE_PATHS...]
```

### Example

```bash
python ctx/main.py --cwd=. README.md
```

## Running Tests

To run the tests, use the `unittest` module from the root directory.

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.