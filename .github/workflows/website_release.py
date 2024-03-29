import os
import re
import hashlib
import sys

def md5(filename):
    hasher = hashlib.md5()
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def extract_version(script_filename):
    version = None
    with open(script_filename, "r") as script_file:
        for line in script_file.read().splitlines():
            if line.strip().startswith("__version__ ="):
                version = line.split("=")[1].strip().replace('"', "")
                break
    return version

if len(sys.argv) != 5:
    print("Usage: website_release.py <executable_filename> <script_filename> <repository> <branch>")
    sys.exit(1)

exe_filename = sys.argv[1]
script_filename = sys.argv[2]
repository_name = sys.argv[3]
branch_name = sys.argv[4]

md5_hash = md5(exe_filename)
version = extract_version(script_filename)
body = f"""# Tierlist Hawkeye version {version}

## This release was provided by the GitHub Actions runner.

**MD5:** {md5_hash}
[Download version {version}](https://nightly.link/{repository_name}/workflows/build/{branch_name}/build.zip)
"""
with open("index.md", "w") as f:
    f.write(body)
