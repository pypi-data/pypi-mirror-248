def extract_string_area(string, count_spaces=False):
    """
  Extracts a specific area from a string, with the number of characters determined by user input.

  Args:
      string: The string to extract from.
      count_spaces: Whether to count spaces as characters (default: False).

  Returns:
      A list containing the extracted characters.
  """

    while True:
        try:
            n = int(input("Enter the number of characters to extract: "))
            break  # Input is valid, exit the loop
        except ValueError:
            print("Invalid input. Please enter an integer.")

    if count_spaces:
        return list(string[:n])
    else:
        return [char for char in string[:n] if not char.isspace()]


# Example usage
string = str(input('Enter the string:'))

# Extract without counting spaces
extracted_area = extract_string_area(string)
print(f"Extracted area (without spaces): {extracted_area}")

# Extract with counting spaces
extracted_area_with_spaces = extract_string_area(string, count_spaces=True)
print(f"Extracted area (with spaces): {extracted_area_with_spaces}")
