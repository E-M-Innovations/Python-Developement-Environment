# Project Design

We have a few resources at our disposal for our project. The first link is a tutorial on how to integrate Cython, Sphinx and Poetry all together. This will be a great starting point for us to get our project off the ground. The second link is how to create a Poetry environment within Docker and manage dependencies. This will be a great way to ensure our environment is configured properly and that everything runs smoothly. With these two links, we should have all we need to get our project up and running.

Sources: 

- [Using Cython + Poetry + Sphinx](https://stackoverflow.com/questions/57988721/poetry-sphinx-cython)
- [Integrating Python Poetry with Docker](https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker)
- [Docker Sphinx Image](https://hub.docker.com/r/sphinxdoc/sphinx)
- [Multi-stage Dockerfile for testing](https://docs.docker.com/language/java/run-tests/#multi-stage-dockerfile-for-testing)

## Project Specifications:

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
└── app/
    ├── poetry.lock
    ├── pyproject.toml
    ├── file1.py
    ├── file2.py
    ├── cythonfile.pyx
    └── test/
        ├── test_file1.py
        ├── test_file2.py
        └── ...
```

## Design Structure 

This setup ensures compatibility and consistency by pinning versions and files. It uses Docker to isolate dependencies, supports Cython with GCC compiler, auto-builds Sphinx documentation, and enables interactive Pytest testing while optionally removing containers upon exit. `base` Image consists of setting up `Poetry`, `Cython` , and `Sphinx`. The `test` image contains the `base` image with the `pytest` testing capabilities 

- **Setting up `Poetry`:**
To ensure compatibility and consistency, pin the Poetry version and `pyproject.toml` file. Add `/src` to the Python path and copy `poetry.lock` and `pyproject.toml` files for dependency management. Enable virtual environments for isolating dependencies within Docker. Separate development and production dependencies using build process arguments for precise installation.
    - Pin the version of Poetry to ensure compatibility and prevent build issues.
    - Pin the version of the `pyproject.toml` file to maintain consistency.
        - Add  `/src` directory to the Python path
    - Copy the `poetry.lock` and `pyproject.toml` files into the Docker image for dependency management.
    - Enable virtual environments to isolate dependencies within the Docker environment.
    - Separate dependencies for development and production environments by passing arguments during the build process to install the required sets of dependencies.
- **Setting up `Cython`:**
    - Install the GCC compiler from the Dockerfile
    - pip install `Cython`(from `poetry.lock` or `pyproject.toml`)
- **Setting up `Sphinx` to auto-build documentation:**
Utilize the official Sphinx Docker image to generate HTML documentation automatically by running `docker run --rm -v /path/to/document:/docs sphinxdoc/sphinx make html`. The command binds the local `/path/to/document` to the `/docs` directory in the container, producing output in `/path/to/document/_build/html`.
    - Create sphinx documents in docker: [Sphinx-Docker](https://hub.docker.com/r/sphinxdoc/sphinx)
        - We could create a bash command when the user runs sphinx make html it could execute the command: `docker run --rm -v /path/to/document:/docs sphinxdoc/sphinx make html`
            - `docker run`: Run a Docker container.
            - `-rm`: Automatically remove the container after it exits.
            - `v /path/to/document:/docs`: Bind mount the local directory `/path/to/document` into the container at `/docs`.
            - `sphinxdoc/sphinx`: Use the official Sphinx Docker image.
            - `make html`: Generate HTML documentation using Sphinx, output placed in `/path/to/document/_build/html`.
- **Setting up `Pytest`:**
This Dockerfile employs a multi-stage setup to configure `Pytest` interactively by adding **`/tests`** to the Python path. It facilitates running tests in detached mode, enabling additional test execution, and optionally, ensures automatic removal of the Docker container upon exit using `--rm`.
    - Inherits from the **`base`** stage.
    - Sets an environment variable **`PYTHONPATH`** to include **`/tests`** on the Python path.
    - Copies the entire application source code (including tests) to the **`/app`** directory.
    - Use a `CMD` command for `bash -c` to run pytest in interactive mode and (**`tail -f /dev/null`**) to keep the container running in detached mode.
    - **Optional:** have the Docker Container be immediately removed after exiting with the use of `--rm` during the run stage.

**Requirements:** `Cython(.pyx)` and `Python(.py)` files should be compatible.
