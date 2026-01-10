# Skill Folder: cli-interface

## File: SKILL.md

---
name: cli-interface
description: Build user-friendly command-line interfaces with menu systems, input validation, formatted output, and error handling. Use when creating console applications, interactive CLI tools, or menu-driven programs.
---

# CLI Interface Skill

## Purpose
Create professional command-line interfaces with menu navigation, input handling, formatted output, and user-friendly interactions.

## When to Use This Skill
- Building console/terminal applications
- Creating interactive CLI tools
- Implementing menu-driven interfaces
- Need user input validation
- Display formatted tables or lists in terminal

## Core Patterns

### Pattern 1: Menu System
```python
def display_menu():
    """Display main menu with clear options"""
    print("\n" + "="*50)
    print("TODO APP - MAIN MENU".center(50))
    print("="*50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")
    print("="*50)

def get_user_choice() -> str:
    """Get and validate menu choice"""
    while True:
        choice = input("\nEnter choice (1-6): ").strip()
        if choice in ['1', '2', '3', '4', '5', '6']:
            return choice
        print("❌ Invalid choice. Please enter 1-6.")
```

### Pattern 2: Input Validation
```python
def get_string_input(prompt: str, required: bool = True, 
                     max_length: int = None) -> str:
    """Get validated string input"""
    while True:
        value = input(prompt).strip()
        
        # Check if required
        if not value and required:
            print("❌ This field is required.")
            continue
        
        # Check max length
        if max_length and len(value) > max_length:
            print(f"❌ Maximum {max_length} characters allowed.")
            continue
        
        return value

def get_integer_input(prompt: str, min_val: int = None) -> int:
    """Get validated integer input"""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val and value < min_val:
                print(f"❌ Must be at least {min_val}.")
                continue
            return value
        except ValueError:
            print("❌ Please enter a valid number.")
```

### Pattern 3: Formatted Output
```python
def display_table(tasks: list):
    """Display data in formatted table"""
    if not tasks:
        print("\n📭 No tasks found.")
        return
    
    # Header
    print("\n" + "="*80)
    header = f"{'ID':<5} {'Title':<35} {'Status':<15} {'Created':<20}"
    print(header)
    print("="*80)
    
    # Rows
    for task in tasks:
        status = "✅ Complete" if task.completed else "⏳ Pending"
        title = task.title[:33] + ".." if len(task.title) > 35 else task.title
        created = task.created_at.strftime("%Y-%m-%d %H:%M")
        
        row = f"{task.id:<5} {title:<35} {status:<15} {created:<20}"
        print(row)
    
    print("="*80)
    print(f"\nTotal: {len(tasks)} task(s)")
```

### Pattern 4: User Feedback
```python
def show_success(message: str):
    """Display success message"""
    print(f"\n✅ SUCCESS: {message}")

def show_error(message: str):
    """Display error message"""
    print(f"\n❌ ERROR: {message}")

def show_info(message: str):
    """Display info message"""
    print(f"\nℹ️  INFO: {message}")

def show_warning(message: str):
    """Display warning message"""
    print(f"\n⚠️  WARNING: {message}")
```

### Pattern 5: Confirmation Dialog
```python
def confirm_action(message: str) -> bool:
    """Get user confirmation"""
    while True:
        response = input(f"\n{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("❌ Please enter 'y' or 'n'")
```

### Pattern 6: Main Application Loop
```python
def main():
    """Main application loop"""
    print("\n🎯 Welcome to Todo App!")
    
    while True:
        try:
            display_menu()
            choice = get_user_choice()
            
            if choice == '1':
                add_task_flow()
            elif choice == '2':
                view_tasks_flow()
            elif choice == '3':
                update_task_flow()
            elif choice == '4':
                delete_task_flow()
            elif choice == '5':
                complete_task_flow()
            elif choice == '6':
                print("\n👋 Thank you for using Todo App!")
                break
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted.")
            if confirm_action("Do you want to exit?"):
                break
        except Exception as e:
            show_error(f"Unexpected error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
```

## Best Practices

1. **Clear Visual Hierarchy**
   - Use separators (lines, spacing)
   - Align text in tables
   - Use consistent formatting

2. **Helpful Error Messages**
   - Tell user what went wrong
   - Suggest how to fix it
   - Show valid options

3. **Input Validation**
   - Validate all user input
   - Handle edge cases (empty, too long)
   - Provide immediate feedback

4. **User Experience**
   - Show what's happening
   - Confirm destructive actions
   - Allow easy navigation
   - Handle Ctrl+C gracefully

5. **Visual Indicators**
   - Use emojis or symbols (✅ ❌ ℹ️ ⚠️)
   - Color if terminal supports it
   - Status indicators (pending/complete)

## Common Pitfalls to Avoid
- Don't trust user input - always validate
- Don't show technical error messages to users
- Don't let app crash on invalid input
- Don't forget to handle Ctrl+C
- Don't make users type long strings when choices work

## Example Implementation

```python
# Complete CLI example
def add_task_flow():
    """User flow for adding a task"""
    print("\n➕ Add New Task")
    print("-" * 50)
    
    # Get title
    title = get_string_input(
        "Enter task title: ",
        required=True,
        max_length=200
    )
    
    # Get description (optional)
    description = get_string_input(
        "Enter description (optional): ",
        required=False,
        max_length=1000
    )
    
    try:
        # Create task
        task = service.create_task(title, description)
        show_success(f"Task created with ID: {task.id}")
        
        # Show created task
        print(f"\n📝 Title: {task.title}")
        if task.description:
            print(f"📄 Description: {task.description}")
            
    except ValueError as e:
        show_error(str(e))
```

## Testing CLI Interfaces

Use pytest with monkeypatch for input testing:

```python
def test_get_user_choice(monkeypatch):
    """Test menu choice input"""
    # Simulate user input
    monkeypatch.setattr('builtins.input', lambda _: '1')
    
    choice = get_user_choice()
    assert choice == '1'

def test_invalid_then_valid_input(monkeypatch):
    """Test input validation with retry"""
    inputs = iter(['invalid', '99', '1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    choice = get_user_choice()
    assert choice == '1'
```
```