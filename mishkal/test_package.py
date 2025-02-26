from pathlib import Path


def test_has_no_breakpoint():
    files = Path(__file__).parent.glob("**/*.py")
    for file in files:
        # Skip files that start with 'test'
        if file.name.startswith("test"):
            continue

        with open(file, "r") as f:
            content = f.readlines()
        for line_number, line in enumerate(content, 1):
            if "breakpoint()" in line:
                print(f"Error in {file}:{line_number} - 'breakpoint()' found")
                assert False, f"Error in {file}:{line_number} - 'breakpoint()' found"
            if "print(" in line:
                print(f"Error in {file}:{line_number} - 'print(' found")
                assert False, f"Error in {file}:{line_number} - 'print(' found"
