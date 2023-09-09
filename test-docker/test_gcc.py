
'''
Checklist: 
- [ ] Check if Cython is installed using Poetry.
  - [ ] If Cython is installed on Linux, confirm and proceed.
  - [ ] If Cython is not installed on Linux, skip GCC installation.
    - [ ] If the Linux distribution is Alpine, update and install GCC.
    - [ ] If the Linux distribution is Debian-based, update and install GCC.
    - [ ] If the distribution is unsupported, display an error and exit.
  - [ ] If Cython is installed on Windows, confirm and proceed.
    - [ ] Check if Cython is installed using `pip`.
    - [ ] If Cython is installed, confirm and proceed.
    - [ ] Set up the C compiler for Windows (e.g., Visual C++ Build Tools).
  - [ ] If Cython is not installed on Windows, display a message.
- [ ] If the operating system is unsupported, display an error and exit.
'''

import docker
import pytest
import subprocess
import os

# Define a list of base images
base_images = [
    {
        "image": "python:3.11.5-alpine",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-slim-bullseye",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-slim-bookworm",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-windowsservercore-1809",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-alpine",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-slim-bullseye",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-slim-bookworm",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-windowsservercore-1809",
        "cython_installed": False
    }
]

# Define a fixture to create and remove the pyproject.toml file
@pytest.fixture(scope="function")
def cleanup_pyproject(request, tmp_path):
    # Define the path for the dynamic pyproject.toml file
    pyproject_path = tmp_path / "pyproject.toml"

    def cleanup():
        # Remove the dynamic pyproject.toml file
        pyproject_path.unlink()

    request.addfinalizer(cleanup)
    return pyproject_path

# Create the pyproject.toml file with or without Cython based on the input
def create_pyproject_with_cython(pyproject_path, cython_installed):
    with open(pyproject_path, "w") as f:
        if cython_installed:
            # Include Cython in the pyproject.toml
            f.write(
                """[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"
cython = "^0.29"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
            )
        else:
            # Exclude Cython in the pyproject.toml
            f.write(
                """[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
            )

import pytest
import subprocess
import os

# Define a list of base images
base_images = [
    {
        "image": "python:3.11.5-alpine",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-slim-bullseye",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-slim-bookworm",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-windowsservercore-1809",
        "cython_installed": True
    },
    {
        "image": "python:3.11.5-alpine",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-slim-bullseye",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-slim-bookworm",
        "cython_installed": False
    },
    {
        "image": "python:3.11.5-windowsservercore-1809",
        "cython_installed": False
    }
]

# Parametrize the test cases with base images
@pytest.mark.parametrize("base_image", base_images)
def test_cython_and_gcc_installation(base_image):
    image = base_image["image"]
    cython_installed = base_image["cython_installed"]

    # Create the Docker container by passing BASE_IMAGE as an argument
    cmd_create_container = f"docker create -it --name my_container --env BASE_IMAGE={image} my_image"
    subprocess.run(cmd_create_container, shell=True)

    # Check if Cython is installed using 'poetry show cython' within the container
    cmd_cython = "docker exec my_container poetry show cython"
    result_cython = subprocess.run(cmd_cython, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if cython_installed:
        # Assert that 'poetry show cython' output contains version information when Cython is installed
        assert "cython" in result_cython.stdout.lower() and "(" in result_cython.stdout, f"Cython is not installed in {image} when it should be."
        
        # Check if GCC is installed using 'gcc --version' within the container
        cmd_gcc = "docker exec my_container gcc --version"
        result_gcc = subprocess.run(cmd_gcc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Assert that GCC is installed when Cython is installed
        assert "gcc" in result_gcc.stdout.lower(), f"GCC is not installed in {image} when Cython is installed."

    else:
        # Assert that 'poetry show cython' output does not contain version information when Cython is not installed
        assert "cython" not in result_cython.stdout.lower() or "(" not in result_cython.stdout, f"Cython is installed in {image} when it should not be."

    # Remove the Docker container and image
    cmd_remove_container = "docker rm -f my_container"
    subprocess.run(cmd_remove_container, shell=True)
    cmd_remove_image = "docker rmi my_image"
    subprocess.run(cmd_remove_image, shell=True)

# Run the tests
if __name__ == '__main__':
    pytest.main()
