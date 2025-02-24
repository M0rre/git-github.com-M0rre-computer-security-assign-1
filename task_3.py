import random


def substitution_cipher(text, key,  encrypt):
    result = ""
    key = key % 128  # Printable ASCII chars
    for char in text:
        if encrypt:
            # ord() to get unicode value then shift character up by key and go back to char
            if char == '\n':  # Skip newline characters
                result += char
                continue
            else:
                result += chr((ord(char) + key) % 128)
        else:
            # Shift down -||-
            if char == '\n':
                result += char
                continue
            result += chr((ord(char) - key) % 128)
    return result


def transposition_cipher(text, key, encrypt):
    # Set seed for reproducible shuffle
    random.seed(key) 
    num_cols = key
    num_rows = (len(text) + num_cols - 1) // num_cols

    # Create matrix and fill row-wise
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    for i, char in enumerate(text):
        row = i // num_cols
        col = i % num_cols
        matrix[row][col] = char

    # Shuffle columns
    col_order = list(range(num_cols))
    random.shuffle(col_order)

    # Encryption: Read in shuffled column order
    if encrypt:
        plaintext = ''
        for col in col_order:
            for row in range(num_rows):
                plaintext += matrix[row][col]

    # Decryption: Reverse the shuffle to read columns in original order
    else:
        # Reverse shuffle to find original columns
        original_order = [0] * num_cols
        for i, col in enumerate(col_order):
            original_order[col] = i

        # Fill columns in reverse order
        idx = 0
        for col in original_order:
            for row in range(num_rows):
                if idx < len(text):
                    matrix[row][col] = text[idx]
                    idx += 1

        # Convert rows to one string
        plaintext = ''.join([''.join(row) for row in matrix])

    return plaintext


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
        encrypted_text = substitution_cipher(text, key, encrypt)
    elif method == 't':
        encrypted_text = transposition_cipher(text, key, encrypt)
    else:
        raise ValueError("Invalid encryption method.")

    with open(output_file, 'w', encoding="UTF-8") as file:
        file.write(encrypted_text)


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
