# Testify - Generate skeleton test file from Python file.

Support Unnitests and Django tests.

## How to use this package?


```bash
python testify --help
Usage: testify.py [OPTIONS]

  Testify command line arguments.

Options:
  --file TEXT  Path to file from which to generate test file
  --type TEXT  Type of test to generate
  --help       Show this message and exit.
```

There is two commands available:
    * `--file` - Requires path to a Python file from which you want to generate the base test file.
    * `--type` - Test type, `unittest` either `django`


## Example

`data.py`

```python
class Manager:

    def manage_data(self):
        return "Managing data"

    def retrieve_data(self):
        return "Retrieved data"
```

Here is our output file.

`test_data.py`

```python
import unittest

class TestManager(unittest.TestCase):
    """TestManager."""

    def test_manage_data(self):
        """Test manage data."""

    def test_retrieve_data(self):
        """Test retrieve data."""
```
