import os
import hashlib

def md5(filename):
    hasher = hashlib.md5()
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def extract_version(script_filename):
    version = None
    with open(script_filename, "r") as script_file:
        for line in script_file:
            if line.strip().startswith("version ="):
                version = line.split("=")[1].strip().replace('"', "")
                break
    return version

exe_filename = "hawkeye.exe"
script_filename = "__main__.py"
md5_hash = md5(exe_filename)
version = extract_version(script_filename)
os.environ["RELEASE_VERSION"] = version
body = f"""This release was built by GitHub Actions using untouched source code.
**Version:** {version}
**MD5:** {md5_hash}"""
with open("body.md", "w") as f:
    f.write(body)
