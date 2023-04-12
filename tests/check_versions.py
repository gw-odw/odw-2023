import json
import sys
import re
import yaml
from yaml.loader import SafeLoader
import glob


env_file = "environment.yml"

# Read in the environemtn yaml file
with open(env_file) as f:
    environment = yaml.load(f, Loader=SafeLoader)

# Extract the dependencies and versions
dependencies = {}
for element in environment["dependencies"]:
    module, version = element.split("=")
    dependencies[module] = version


files = glob.glob("Tutorials/*/*ipynb")
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
