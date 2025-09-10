# Local Testing Guide

To run the project tests:

1. **Set up a virtual environment** (recommended)

```bash
# Create a virtual environment (if not already created)
python -m venv venv

# Activate the environment
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows
```

2. **Install test dependencies**

```bash
pip install -r tests/requirements.txt
```

3. **Run tests using unittest**

   ```bash
   # From the tests directory
   python -m unittest discover

   # Or from the project root
   python -m unittest discover tests
   ```

## Test Coverage

- **Structure validation**: Validates JSON schema and field types
- **Domain validation**: Checks domain format using validators library
- **URL validation**: Validates web page URLs
- **Field trimming**: Ensures no leading/trailing whitespace
- **Country code validation**: Verifies 2-character alpha codes

## Adding Custom Tests

Create new test files in `tests/` directory following the existing pattern:

```python
import json
import unittest
import os

class CustomTests(unittest.TestCase):
    def setUp(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(script_dir), "world_universities_and_domains.json")
        with open(json_path, encoding="utf-8") as json_file:
            self.data = json.load(json_file)
    
    def test_custom_validation(self):
        # Your test logic here
        pass
```