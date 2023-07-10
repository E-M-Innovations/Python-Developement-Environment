# Project Design

We have a few resources at our disposal for our project. The first link is a tutorial on how to integrate Cython, Sphinx and Poetry all together. This will be a great starting point for us to get our project off the ground. The second link is how to create a Poetry environment within Docker and manage dependencies. This will be a great way to ensure our environment is configured properly and that everything runs smoothly. With these two links, we should have all we need to get our project up and running.

Sources: 

- [Using Cython + Poetry + Sphinx](https://stackoverflow.com/questions/57988721/poetry-sphinx-cython)
- [Integrating Python Poetry with Docker](https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker)

## The Design Thus Far:

The main objectives are to create a design for incorporating Poetry within a Docker environment.

- Maintain separate directories for PyTest test files (`tests/`) and Sphinx documentation (`docs/`) on the host machine during development.
- Avoid directly including the test files and documentation in the Docker image.
- Utilize Poetry to manage dependencies within the Docker environment.
- Ensure that the Docker image is configured to access the test files and documentation directories from the host machine.
- Have the Sphinx output `index.html` auto-build when there are changes to the code and have it only be visible on the host machine.
- The PyTest test files (`tests/`)  could be executed within the Docker image with Cython and Python files alike.

**Context:**

Given that Docker is being employed for my development environment and Poetry for managing dependencies, it is our objective to establish a streamlined workflow whereby the PyTest test files and Sphinx documentation directories are retained on the host machine while only code and its associated dependencies reside within the Docker image. This strategy facilitates seamless testing execution in a Docker setting whilst also guaranteeing updated documentation generation by Sphinx.

**Directory Structure:**

```
Host Machine:
├── project/
|   ├── poetry.lock
|   ├── pyproject.toml
│   ├── code/
│   │   ├── file1.py
│   │   ├── file2.py
|   |   ├── cythonfile.pyx
│   │   └── ...
│   ├── tests/
│   │   ├── test_file1.py
│   │   ├── test_file2.py
│   │   └── ...
│   └── docs/
│       ├── conf.py
│       ├── index.rst
│       ├── index.html (Output)
│       └── ...
└── Dockerfile

Docker Machine:
└── code/
		├── poetry.lock
		├── pyproject.toml
    ├── file1.py
    ├── file2.py
    ├── cythonfile.pyx
    └── ...
```

We would like to figure out the design for the following:

- Setting up Poetry with Docker by
    - Pin the version of Poetry to ensure compatibility and prevent build issues.
    - Pin the version of the pyproject.toml file to maintain consistency.
    - Copy the poetry.lock and pyproject.toml files into the Docker image for dependency management.
    - Enable virtual environments to isolate dependencies within the Docker environment.
    - Separate dependencies for development and production environments by passing arguments during the build process to install the required sets of dependencies.
- Configure Cython to work seamlessly with auto-documentation using Sphinx and ensure compatibility with Pytest.
- Set up Sphinx to auto-build on the host machine, possibly by using bind mounts for efficient file synchronization.
- Configure Pytest to run tests exclusively on the Docker machine, potentially utilizing volumes for seamless access to the test files.