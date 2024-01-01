# Fortuned

[![PyPI version][def]](https://pypi.org/project/fortuned/)

Fortuned is a simple Flask application that serves a random fortune from a list of fortunes. The fortunes are stored in a text file and are read and parsed by the application.

## Installation

To install Fortuned, you can use pip:

```bash
pip install fortuned
```

## Usage

After installation, you can run the application with the following command:

```bash
fortuned
```

The application will start a server and listen on <http://localhost:5000>. When you navigate to this URL in your web browser, you will be served a random fortune.

## Code Overview

The application is structured as follows:

- The `get_fortunes` function in `app.py` reads a text file containing fortunes, splits it into a list, and returns the list. The text file is assumed to have one fortune per line.

- The `main` function in `app.py` generates a list of 5 random numbers and selects a random fortune from the list of fortunes. It then renders an HTML template, passing the fortune and the list of numbers to the template.

- The application uses Flask's built-in development server. When the script is run directly (i.e., not imported as a module), the server is started in debug mode.

## Customization

You can customize the application by modifying the fortunes text file. Each line in the file represents a single fortune. The application will read the file and serve a random line as a fortune.

[def]: https://badge.fury.io/py/fortuned.svg
