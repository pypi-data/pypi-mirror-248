# pytinyxml2

Python library to wrap the [tinyxml2](https://github.com/leethomason/tinyxml2) library

## Installation

Just like other ones, just type:

```shell
pip3 install pytinyxml2
```

## Usage

You can call C method of tinyxml2 in Python:

```python3
import pytinyxml2
doc = pytinyxml2.XMLDocument()
doc.Parse("<?xml version=\"1.0\"?><element>Text</element>")
print(doc.FirstChildElement().GetText())
```
