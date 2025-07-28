# Without the walrus operator
text = input("Enter something: ")
if len(text) > 5:
    print(f"Your input is long: {text}")

# With the walrus operator (shorter & cleaner)
if (text := input("Enter something: ")).strip() and len(text) > 5:
    print(f"Your input is long: {text}")