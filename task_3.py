def substitution_cipher(text, key, encrypt=True):
    result = ""
    key = key % 256  # Keeps key withing bounds
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


def transposition_cipher(text, key, encrypt=True):
    if encrypt:  # Encrypt
        # Calculate the number of rows needed
        rows = (len(text) + key - 1) // key

        # Create a matrix with the calculated number of rows
        matrix = [['' for _ in range(key)] for _ in range(rows)]

        # Fill the matrix row-wise
        for i, char in enumerate(text):
            row = i // key
            col = i % key
            matrix[row][col] = char

        # Read the matrix column-wise to get the ciphertext
        ciphertext = ''
        for col in range(key):
            for row in range(rows):
                ciphertext += matrix[row][col]

        return ciphertext

    else:  # Decrypt
        # Calculate the number of rows needed
        rows = (len(text) + key - 1) // key

        # Create a matrix with the calculated number of rows
        matrix = [['' for _ in range(key)] for _ in range(rows)]

        # Fill the matrix column-wise
        index = 0
        for col in range(key):
            for row in range(rows):
                if index < len(text):
                    matrix[row][col] = text[index]
                    index += 1

        # Read the matrix row-wise to get the plaintext
        plaintext = ''
        for row in range(rows):
            for col in range(key):
                plaintext += matrix[row][col]

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
