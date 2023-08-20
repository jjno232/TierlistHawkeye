import os
import re
import hashlib
import sys

def tag_convert(string):
    trimmed = string.replace(" ", "").replace("(", "").replace(")", "")
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', trimmed)
    valid = re.sub(r'_+', '_', cleaned).strip('_')
    return valid

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

if len(sys.argv) != 3:
    print("Usage: release_body.py <executable_filename> <script_filename>")
    sys.exit(1)

exe_filename = sys.argv[1]
script_filename = sys.argv[2]

md5_hash = md5(exe_filename)
version = extract_version(script_filename)
os.environ["RELEASE_VERSION"] = tag_convert(version)
body = f"""This release was built by GitHub Actions using untouched source code.
**Version:** {version}
**MD5:** {md5_hash}"""
with open("body.md", "w") as f:
    f.write(body)
