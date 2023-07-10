# Python Dev Environment with Docker, Sphinx, Pytest, Cython & Poetry Dependency Management

This project aims to create a containerized Python Development environment that incorporates automated documentation, seamless unit testing, and efficient dependency management. The environment utilizes popular tools like Sphinx, pytest, and poetry to enhance the development workflow.

## Features

The Python Development environment offers the following key features:

- **Automated Documentation:** The environment integrates Sphinx, a widely-used documentation generator. It automates the process of generating documentation for Python code. Developers can write human-readable documentation alongside their code and effortlessly generate documentation in various formats, such as HTML or PDF.

- **Seamless Unit Testing:** The environment incorporates pytest, a popular testing framework in the Python ecosystem. Developers can write expressive test cases using pytest's syntax, run tests, and obtain comprehensive test reports. This ensures the reliability and correctness of their code, leading to more robust software development.

- **Efficient Dependency Management:** The environment leverages poetry, a powerful dependency management tool for Python. Poetry simplifies the process of defining and resolving dependencies, allowing developers to manage project dependencies, handle versioning, and ensure consistency across different environments.

- **Containerized Environment:** The Python Development environment is containerized using Docker. This encapsulates all the necessary components, including the tools (Sphinx, pytest, poetry) and their dependencies, ensuring portability, consistency, and easy distribution across different systems and platforms.

## Usage

To utilize this Python Development environment:

1. Install Docker on your system if not already installed.
2. Clone this repository to your local machine.
3. Build the Docker image using the provided Dockerfile.
4. Run the Docker container based on the built image.
5. Start coding in the containerized environment, taking advantage of the automated documentation, seamless unit testing, and efficient dependency management features.

## Directory Structure

The directory structure for this project is as follows:

```
- /project
  - Dockerfile
  - /src
    - main.py
    - cython.pyx
    - ...
  - /tests
    - test_main.py
    - ...
  - /docs
    - conf.py
    - index.rst
    - index.html 
    - ...
  - poetry.lock
  - pyproject.toml
```

- The `/src` directory contains the main Python code files.
- The `/tests` directory houses the test cases written using pytest.
- The `/docs` directory includes the Sphinx documentation files.

## Contributions

Contributions to this project are welcome. If you have any suggestions or improvements, please feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to the open-source community for providing the tools and frameworks used in this project, including Sphinx, pytest, poetry, and Docker.
