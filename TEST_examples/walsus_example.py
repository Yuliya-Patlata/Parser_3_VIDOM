"""A1002 – Walrus Operator (:=) Explained 🦦

The := operator, known as the walrus operator, was introduced in Python 3.8. It allows you to assign a value to a variable inside an expression, making code more concise and sometimes more efficient.
🛠 Basic Example:"""

# Without the walrus operator
text = input("Enter something: ")
if len(text) > 5:
    print(f"Your input is long: {text}")

# With the walrus operator (shorter & cleaner)
if (text := input("Enter something: ")).strip() and len(text) > 5:
    print(f"Your input is long: {text}")