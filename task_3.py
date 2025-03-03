def substitution_cipher(text, key,  encrypt):
    result = ""
    key = key % 256  # Keep key within range
    for char in text:
        if encrypt:
            # ord() to get unicode value then shift character up by key and go back to char
            if char == '\n':  # Skip newline characters
                result += char
                continue
            else:
                result += chr((ord(char) + key) % 256)
        else:
            # Shift down -||-
            if char == '\n':
                result += char
                continue
            result += chr((ord(char) - key) % 256)
    return result


def transposition_cipher(text, key, encrypt):
    """
    Implement a transposition cipher.
    
    Args:
        text (str): The text to encrypt/decrypt
        key (str): The key used for encryption/decryption
        encrypt (bool): True for encryption, False for decryption
        
    Returns:
        str: The encrypted/decrypted text
    """
    # Input validation
    if not text:
        return ""
    
    if not key:
        return "Error: Key cannot be empty"
    
    # Remove duplicates from the key while preserving order
    unique_key = ""
    for char in key:
        if char not in unique_key:
            unique_key += char
    
    key_length = len(unique_key)
    
    # Create key order based on alphabetical sorting
    # First create a list of (character, position) tuples
    indexed_key = [(char, i) for i, char in enumerate(unique_key)]
    # Sort by character
    sorted_indexed_key = sorted(indexed_key, key=lambda x: x[0])
    # Create a mapping from sorted position to original position
    key_order = [item[1] for item in sorted_indexed_key]
    
    if encrypt:
        # Encryption
        # Add padding if necessary
        padded_length = ((len(text) + key_length - 1) // key_length) * key_length
        padded_text = text.ljust(padded_length)
        
        # Arrange text in a matrix with width equal to key length
        matrix = []
        for i in range(0, padded_length, key_length):
            row = padded_text[i:i+key_length]
            matrix.append(row)
        
        # Read out by columns according to key order
        result = ""
        for col_index in range(key_length):
            # Find the original column index this corresponds to
            orig_col = key_order.index(col_index)
            for row in matrix:
                if orig_col < len(row):
                    result += row[orig_col]
        
        return result
    
    else:
        # Decryption
        # Calculate the dimensions of the original matrix
        rows = (len(text) + key_length - 1) // key_length
        cols = key_length
        
        # Special case: the last row might not be complete
        last_row_size = len(text) % key_length
        if last_row_size == 0 and len(text) > 0:
            last_row_size = key_length
        
        # Create an empty matrix
        matrix = [[''] * cols for _ in range(rows)]
        
        # Calculate the number of characters in each column
        col_sizes = [rows for _ in range(cols)]
        if last_row_size > 0 and last_row_size < cols:
            # Adjust the size of columns that don't have a character in the last row
            for i in range(last_row_size, cols):
                col_sizes[key_order[i]] -= 1
        
        # Fill the matrix with the ciphertext
        index = 0
        for col_index in range(cols):
            # Find the original column this corresponds to
            orig_col = key_order.index(col_index)
            for row in range(col_sizes[orig_col]):
                matrix[row][orig_col] = text[index]
                index += 1
        
        # Read out the plaintext row by row
        result = ""
        for row in matrix:
            result += ''.join(row)
        
        # Remove any padding spaces at the end
        return result.rstrip()

# Example usage:
# test = "omg it's corn"
# key = "CIPHER"
# encrypted = transposition_cipher(test, key, True)
# decrypted = transposition_cipher(encrypted, key, False)
# print(f"Original: '{test}'")
# print(f"Encrypted: '{encrypted}'")
# print(f"Decrypted: '{decrypted}'")




def process_file(input_file, output_file, method, key, encrypt):
    # Read the input file
    try:
        with open(input_file, 'r', encoding="UTF-8") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return

    # Select enc method
    if method == 's':
        processed_text = substitution_cipher(text, key, encrypt)
    elif method == 't':
        processed_text = transposition_cipher(text, key, encrypt)
    else:
        raise ValueError("Invalid encryption method.")

    with open(output_file, 'w', encoding="UTF-8") as file:
        file.write(processed_text)


def main():
    # Get user input
    operation = input("Choose operation (encrypt(E)/decrypt(D)): ").lower()
    method = input("Choose encryption method (substitution(S)/transposition(T)): ").lower()
    key = int(input("Enter the secret key: "))
    input_file = input("Input the name of the file you want to process: ")
    file_name, _ = input_file.split(".")  # Don't you dare have more than one dot in the file name

    # Edit output file depending on decryption or encryption
    output_file = file_name + "_enc" + ".txt" if operation == 'e' else file_name + "_dec" + ".txt"

    encrypt = operation == 'e'  # Convert to bool (T/F)

    try:
        process_file(input_file, output_file, method, key, encrypt)
        print(f"File successfully {'encrypted' if encrypt else 'decrypted'} and saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
