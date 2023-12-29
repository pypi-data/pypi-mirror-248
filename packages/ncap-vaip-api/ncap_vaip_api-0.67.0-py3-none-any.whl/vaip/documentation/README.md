# Documentation Readme

As of January 2023, the archive_workflows/api/vaip/documentation directory houses
pydoc generated html files that serve as helper documentation for users of the Vaip API.

## Installation

The documentation included in this directory was created with pydoc, the standard
documentation model for the Python programming language. Pydoc is *included*
in all versions of Python since 2.1


## Usage

### Best Utilization - Run local pydoc server http://localhost:51593/ to dynamically generate html representation of the code
```python
python -m pydoc -b
```
### Generate pydoc for \<filename>.py
```python
# Generate a <filename>.html representing the <filename>.py file in question; omit the .py extension for the filename
python -m pydoc -w <filename>
```
### Open the HTML file
```python
open ontology.html
```

## Contributing

This work is intended to be ongoing. As code in the Vaip API changes,
so will it become necessary to update the documentation. 
Please feel encouraged to create, update, or delete as is necessary.

At the time of writing, html documentation is housed in this directory and within the archive_workflows/api/vaip/tests directory.

It is suggested that documentation be generated as code is being written in the form of docstrings just below the initialization of the class, function, or method.
The Visual Studio Code extension "autodocstring" is recommended to streamline this process, or at least the 
format executed by implementing "autodocstring" is recommended:

```python 
#docstring implementation format

def function(parameter):
"""summary:

arguments: type(parameter): parameter

returns:

"""
    some function code here..




