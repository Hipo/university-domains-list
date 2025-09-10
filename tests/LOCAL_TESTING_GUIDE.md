# Local Testing Guide

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r tests/requirements.txt
```

## Running Tests

### Individual Tests
```bash
# JSON structure validation
python -m unittest tests.test_domains

# Field trimming validation  
python -m unittest tests.test_trimming
```

### All Tests
```bash
python -m unittest discover tests/
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