import os
import unittest
import subprocess
import tempfile
import shutil


class TestFileTreeCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.test_dir)

        # Create the directory structure
        os.makedirs("folder1", exist_ok=True)
        os.makedirs("folder2", exist_ok=True)
        # Create files with content
        with open("folder1/file1.txt", "w") as f:
            f.write("Content of file1.txt")
        with open("folder1/file2.txt", "w") as f:
            f.write("Content of file2.txt")
        with open("folder2/file3.txt", "w") as f:
            f.write("Content of file3.txt")
        with open("file4.txt", "w") as f:
            f.write("Content of file4.txt")
        with open("README.md", "w") as f:
            f.write("# README Content")

        # Path to the script to be tested
        self.script_path = os.path.join(
            self.original_cwd,
            "..",
            "ctx",
            "main.py",
        )

    def tearDown(self):
        # Change back to the original working directory
        os.chdir(self.original_cwd)
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_basic_tree_display(self):
        # Test the basic tree display
        result = subprocess.run(
            ["python", self.script_path, f"--cwd={self.test_dir}"],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_output = f"""/{os.path.basename(self.test_dir)}
    ├── folder1
    │   ├── file1.txt
    │   └── file2.txt
    ├── folder2
    │   └── file3.txt
    ├── README.md
    └── file4.txt
"""
        self.assertEqual(expected_output.strip(), result.stdout.strip())

    def test_ignore_path(self):
        # Test ignoring a path
        result = subprocess.run(
            [
                "python",
                self.script_path,
                f"--cwd={self.test_dir}",
                "--ignore-path=folder1",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_output = f"""/{os.path.basename(self.test_dir)}
    ├── folder2
    │   └── file3.txt
    ├── README.md
    └── file4.txt
"""
        self.assertEqual(expected_output.strip(), result.stdout.strip())

    def test_display_file_contents(self):
        # Test displaying contents of specified files
        result = subprocess.run(
            [
                "python",
                self.script_path,
                f"--cwd={self.test_dir}",
                "README.md",
                "folder2/file3.txt",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_tree = f"""/{os.path.basename(self.test_dir)}
├── folder1
│   ├── file1.txt
│   └── file2.txt
├── folder2
│   └── file3.txt
├── file4.txt
└── README.md
"""
        expected_content = """
./README.md
```
# README Content
```

./folder2/file3.txt
```
Content of file3.txt
```
"""
        expected_output = expected_tree.strip() + expected_content
        self.assertEqual(expected_output.strip(), result.stdout.strip())

    def test_specified_files_under_ignored_paths(self):
        # Test specifying files under ignored paths
        result = subprocess.run(
            [
                "python",
                self.script_path,
                f"--cwd={self.test_dir}",
                "--ignore-path=folder1",
                "folder1/file1.txt",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_tree = f"""/{os.path.basename(self.test_dir)}
    ├── folder2
    │   └── file3.txt
    ├── README.md
    └── file4.txt
"""
        expected_content = """

Warning: 'folder1/file1.txt' is under an ignored path and will not be displayed.
"""
        expected_output = expected_tree.strip() + expected_content
        self.assertEqual(expected_output.strip(), result.stdout.strip())

    def test_nonexistent_file(self):
        # Test specifying a nonexistent file
        result = subprocess.run(
            ["python", self.script_path, f"--cwd={self.test_dir}", "nonexistent.txt"],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_tree = f"""/{os.path.basename(self.test_dir)}
        ├── folder1
        │   ├── file1.txt
        │   └── file2.txt
        ├── folder2
        │   └── file3.txt
        ├── file4.txt
        └── README.md
        
        Warning: 'nonexistent.txt' does not exist or is not a file."""
        self.assertEqual(expected_tree.strip(), result.stdout.strip())

    def test_directory_as_file(self):
        # Test specifying a directory instead of a file
        result = subprocess.run(
            ["python", self.script_path, f"--cwd={self.test_dir}", "folder1"],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_tree = f"""/{os.path.basename(self.test_dir)}
        ├── folder1
        │   ├── file1.txt
        │   └── file2.txt
        ├── folder2
        │   └── file3.txt
        ├── file4.txt
        └── README.md
        
        Warning: 'folder1' is a directory, not a file."""
        self.assertEqual(result.stdout.strip(), expected_tree.strip())

    def test_file_outside_cwd(self):
        # Create a file outside the test directory
        new_temp_dir = tempfile.mkdtemp()
        outside_file = os.path.join(new_temp_dir, "outside.txt")
        with open(outside_file, "w") as f:
            f.write("Content of outside.txt")
        try:
            # Test specifying a file outside the cwd
            result = subprocess.run(
                ["python", self.script_path, f"--cwd={self.test_dir}", outside_file],
                stdout=subprocess.PIPE,
                text=True,
            )
            expected_tree = f"""/{os.path.basename(self.test_dir)}
    ├── folder1
    │   ├── file1.txt
    │   └── file2.txt
    ├── folder2
    │   └── file3.txt
    ├── README.md
    └── file4.txt

Warning: '{os.path.relpath(outside_file, self.test_dir)}' is not under the specified cwd."""
            self.assertEqual(result.stdout.strip(), expected_tree.strip())
        finally:
            # Clean up the outside file
            os.remove(outside_file)

    def test_ignore_tree_with_files(self):
        # Test using --ignore-tree with specified files
        result = subprocess.run(
            [
                "python",
                self.script_path,
                f"--cwd={self.test_dir}",
                "--ignore-tree",
                "README.md",
                "folder1/file1.txt",
            ],
            stdout=subprocess.PIPE,
            text=True,
        )

        expected_output = """
./README.md
```
# README Content
```

./folder1/file1.txt
```
Content of file1.txt
```
"""
        self.assertEqual(expected_output.strip(), result.stdout.strip())

    def test_ignore_tree_no_files(self):
        # Test using --ignore-tree without specified files
        result = subprocess.run(
            ["python", self.script_path, f"--cwd={self.test_dir}", "--ignore-tree"],
            stdout=subprocess.PIPE,
            text=True,
        )
        expected_output = "Warning: No content to display."
        self.assertEqual(expected_output.strip(), result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
