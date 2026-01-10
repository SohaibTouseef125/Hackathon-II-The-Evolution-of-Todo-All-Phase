# Skill Folder: data-validation

## File: SKILL.md

```markdown
---
name: data-validation
description: Implement comprehensive input validation with clear error messages, type checking, and business rules. Use when validating user input, API data, form data, or any untrusted data in Python applications.
---

# Data Validation Skill

## Purpose
Create robust data validation with type checking, business rules, and helpful error messages to ensure data integrity.

## When to Use This Skill
- Validating user input in console apps
- Checking API request/response data
- Validating form data
- Enforcing business rules
- Preventing invalid data in storage

## Basic Validation Functions

### String Validation
```python
from typing import Optional

def validate_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate task title
    Returns: (is_valid, error_message)
    """
    # Check type
    if not isinstance(title, str):
        return False, "Title must be a string"
    
    # Check not empty
    title = title.strip()
    if not title:
        return False, "Title cannot be empty"
    
    # Check length
    if len(title) > 200:
        return False, "Title cannot exceed 200 characters"
    
    return True, None

def validate_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
    """Validate task description"""
    # None is OK (optional field)
    if description is None:
        return True, None
    
    # Check type
    if not isinstance(description, str):
        return False, "Description must be a string"
    
    # Check length
    if len(description) > 1000:
        return False, "Description cannot exceed 1000 characters"
    
    return True, None
```

### Number Validation
```python
def validate_task_id(task_id: any) -> tuple[bool, Optional[str]]:
    """Validate task ID"""
    # Try to convert to int
    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        return False, "Task ID must be a number"
    
    # Check positive
    if task_id <= 0:
        return False, "Task ID must be positive"
    
    return True, None
```

## Validator Class Pattern

```python
from typing import Any, Callable, Dict, List

class Validator:
    """Flexible validation class for multiple fields"""
    
    def __init__(self):
        self.errors: Dict[str, str] = {}
    
    def validate_field(self, field: str, value: Any,
                      rules: List[Callable]) -> bool:
        """
        Validate a field against multiple rules
        Returns: True if all rules pass
        """
        for rule in rules:
            is_valid, error = rule(value)
            if not is_valid:
                self.errors[field] = error
                return False
        return True
    
    def is_valid(self) -> bool:
        """Check if all validations passed"""
        return len(self.errors) == 0
    
    def get_errors(self) -> Dict[str, str]:
        """Get all validation errors"""
        return self.errors.copy()
    
    def get_error_message(self) -> str:
        """Get formatted error message"""
        if not self.errors:
            return ""
        return "; ".join(f"{field}: {msg}" for field, msg in self.errors.items())
    
    def clear(self):
        """Clear all errors"""
        self.errors.clear()

# Usage
validator = Validator()
validator.validate_field('title', title, [validate_title])
validator.validate_field('description', desc, [validate_description])

if not validator.is_valid():
    raise ValueError(validator.get_error_message())
```

## Reusable Validation Rules

### Required Field
```python
def required(value: Any) -> tuple[bool, Optional[str]]:
    """Check if value is provided"""
    if value is None:
        return False, "This field is required"
    if isinstance(value, str) and not value.strip():
        return False, "This field cannot be empty"
    return True, None
```

### Length Validators
```python
def min_length(min_len: int):
    """Create minimum length validator"""
    def validator(value: str) -> tuple[bool, Optional[str]]:
        if len(value) < min_len:
            return False, f"Must be at least {min_len} characters"
        return True, None
    return validator

def max_length(max_len: int):
    """Create maximum length validator"""
    def validator(value: str) -> tuple[bool, Optional[str]]:
        if len(value) > max_len:
            return False, f"Cannot exceed {max_len} characters"
        return True, None
    return validator

def length_range(min_len: int, max_len: int):
    """Create length range validator"""
    def validator(value: str) -> tuple[bool, Optional[str]]:
        length = len(value)
        if length < min_len or length > max_len:
            return False, f"Must be {min_len}-{max_len} characters"
        return True, None
    return validator

# Usage
validate_field('title', title, [
    required,
    min_length(1),
    max_length(200)
])
```

### Type Validators
```python
def is_type(expected_type: type):
    """Create type validator"""
    def validator(value: Any) -> tuple[bool, Optional[str]]:
        if not isinstance(value, expected_type):
            return False, f"Must be of type {expected_type.__name__}"
        return True, None
    return validator

def is_string(value: Any) -> tuple[bool, Optional[str]]:
    """Check if value is string"""
    return is_type(str)(value)

def is_integer(value: Any) -> tuple[bool, Optional[str]]:
    """Check if value is integer"""
    return is_type(int)(value)

def is_boolean(value: Any) -> tuple[bool, Optional[str]]:
    """Check if value is boolean"""
    return is_type(bool)(value)
```

### Range Validators
```python
def min_value(min_val: int):
    """Create minimum value validator"""
    def validator(value: int) -> tuple[bool, Optional[str]]:
        if value < min_val:
            return False, f"Must be at least {min_val}"
        return True, None
    return validator

def max_value(max_val: int):
    """Create maximum value validator"""
    def validator(value: int) -> tuple[bool, Optional[str]]:
        if value > max_val:
            return False, f"Cannot exceed {max_val}"
        return True, None
    return validator

def in_range(min_val: int, max_val: int):
    """Create range validator"""
    def validator(value: int) -> tuple[bool, Optional[str]]:
        if value < min_val or value > max_val:
            return False, f"Must be between {min_val} and {max_val}"
        return True, None
    return validator
```

### Pattern Validators
```python
import re

def matches_pattern(pattern: str, message: str = "Invalid format"):
    """Create regex pattern validator"""
    regex = re.compile(pattern)
    def validator(value: str) -> tuple[bool, Optional[str]]:
        if not regex.match(value):
            return False, message
        return True, None
    return validator

# Example: Email validation
email_validator = matches_pattern(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "Invalid email format"
)
```

## Validation Decorator

```python
from functools import wraps
import inspect

def validate_input(**validations):
    """
    Decorator to automatically validate function inputs
    
    Usage:
    @validate_input(
        title=validate_title,
        task_id=validate_task_id
    )
    def update_task(task_id: int, title: str):
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments to parameter names
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            # Validate each specified parameter
            for param_name, validator_func in validations.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    is_valid, error = validator_func(value)
                    if not is_valid:
                        raise ValueError(f"{param_name}: {error}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@validate_input(
    task_id=validate_task_id,
    title=validate_title
)
def update_task(task_id: int, title: str):
    """Update task with automatic validation"""
    # Validation happens automatically before this code runs
    return store.update(task_id, title=title)
```

## Custom Exception for Validation

```python
class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")
    
    @classmethod
    def from_dict(cls, errors: Dict[str, str]):
        """Create from multiple errors"""
        messages = [f"{field}: {msg}" for field, msg in errors.items()]
        return cls("validation", "; ".join(messages))
```

## Complete Validation Example

```python
def create_task(title: str, description: Optional[str] = None) -> Task:
    """Create task with comprehensive validation"""
    validator = Validator()
    
    # Validate title
    validator.validate_field('title', title, [
        required,
        is_string,
        min_length(1),
        max_length(200)
    ])
    
    # Validate description if provided
    if description is not None:
        validator.validate_field('description', description, [
            is_string,
            max_length(1000)
        ])
    
    # Check if valid
    if not validator.is_valid():
        raise ValidationError.from_dict(validator.get_errors())
    
    # Create task
    return Task(title=title, description=description)
```

## Testing Validation

```python
import pytest

def test_validate_title_success():
    """Test valid title passes"""
    is_valid, error = validate_title("Buy groceries")
    assert is_valid is True
    assert error is None

def test_validate_title_empty():
    """Test empty title fails"""
    is_valid, error = validate_title("")
    assert is_valid is False
    assert "empty" in error.lower()

def test_validate_title_too_long():
    """Test long title fails"""
    long_title = "a" * 201
    is_valid, error = validate_title(long_title)
    assert is_valid is False
    assert "200" in error

@pytest.mark.parametrize("title,expected", [
    ("Valid Title", True),
    ("", False),
    ("a" * 201, False),
    ("   ", False),
    ("A", True),
])
def test_title_validation_cases(title, expected):
    """Test multiple title cases"""
    is_valid, _ = validate_title(title)
    assert is_valid == expected

def test_validator_class():
    """Test Validator class"""
    validator = Validator()
    
    # Test invalid
    validator.validate_field('title', "", [validate_title])
    assert not validator.is_valid()
    assert 'title' in validator.get_errors()
    
    # Test clear and valid
    validator.clear()
    validator.validate_field('title', "Valid", [validate_title])
    assert validator.is_valid()
    assert len(validator.get_errors()) == 0
```

## Best Practices

1. **Validate Early** - Check at entry points before processing
2. **Clear Messages** - Tell user what's wrong and how to fix
3. **Type Safety** - Always check types before operations
4. **Business Rules** - Encode all rules as validators
5. **Reusable Rules** - Create composable validation functions
6. **Test Thoroughly** - Test valid, invalid, and edge cases
7. **Fail Fast** - Return on first error or collect all errors

## Common Pitfalls to Avoid
- Don't trust any external data
- Don't show technical errors to users
- Don't forget to trim/sanitize strings
- Don't validate in multiple places (centralize)
- Don't skip validation for "trusted" sources

## Validation Checklist
- [ ] All user inputs validated
- [ ] Type checking performed
- [ ] Length/range constraints enforced
- [ ] Business rules applied
- [ ] Clear error messages provided
- [ ] Edge cases handled (None, empty, whitespace)
- [ ] Tests cover all rules
```