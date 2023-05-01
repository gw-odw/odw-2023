import json
import sys
import re
import yaml
from yaml.loader import SafeLoader
import glob


env_file = "environment.yml"
requirements_file = "requirements.txt"

# Read in the environment yaml file
with open(env_file) as f:
    environment = yaml.load(f, Loader=SafeLoader)

# Read in the requirements file
requirements = {}
with open(requirements_file) as f:
    for line in f:
        module, version = line.split("==")
        requirements[module] = version.rstrip("\n")


# Extract the dependencies and versions
dependencies = {}
for element in environment["dependencies"]:
    module, version = element.split("=")
    dependencies[module] = version


# Check requirements and dependencies match
# Note requirements.txt is a subset of the full environment.yml
for module, version in requirements.items():
    if version != dependencies[module]:
        raise ValueError("Mismatch in versions between environment.yml and requirements.txt")


files = glob.glob("Tutorials/Day_*/*ipynb")
errors = []
for fname in files:
    print(f"Checking {fname}")
    with open(fname, "r") as file:
        content = json.load(file)

    for cell in content["cells"]:
        code = "\n".join(cell["source"])
        if "pip install "in code:
            pip_installs = re.findall("([a-z]+==[0-9\.]+)", code)
            for element in pip_installs:
                module, version = element.split("==")
                if module in dependencies:
                    if dependencies[module] != version:
                        msg = f"Failed: {fname} has a version mismatch in {module}: {version} != {dependencies[module]}"
                        errors.append(msg)
                    else:
                        msg = f"Passed: {fname} uses {module}: {version}"
                        print(msg)
                else:
                    msg = f"Failed: {fname} needs {module}: {version}, but it is not in the environment.yml file"
                    errors.append(msg)

if len(errors) > 0:
    errors = "\n".join(errors)
    msg = f"\nVersion issues: {errors}"
    print(msg)
    sys.exit(1)
