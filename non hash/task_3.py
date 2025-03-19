def substitution_cipher(text, key,  encrypt):
    result = ""
    key = key % 128  # Keep key within range
    for char in text:
        if encrypt:
            # ord() to get unicode value then shift character up by key and go back to char
            if char == '/':  # Idk, just didn't want to shift it back and im not paid enough
                result += char
                continue
            else:
                result += chr((ord(char) + key) % 128)
        else:
            # Shift down -||-
            if char == '/':
                result += char
                continue
            result += chr((ord(char) - key) % 128)
    return result


def transposition_cipher(text, key, encrypt):
    # Check for inputs
    if not key:
        raise ValueError("Encryption key cannot be empty")
    if not text:
        return ""

    # Calculate number of columns based on key length
    col = len(key)

    # Calculate number of rows needed to fit the entire text
    # By a function I found online instead of using math ceil
    row = (len(text) + col - 1) // col

    if encrypt:
        # Convert text string to a BFL (Big Fucking List)
        text_lst = list(text)

        # Pad columns that aren't completely filled
        fill_null = (row * col) - len(text)
        text_lst.extend('_' * fill_null)  # Change depending on if inc. in text

        # Sort the key to determine column order
        key_lst = sorted([(char, index) for index, char in enumerate(key)])

        # Create matrix row-wise
        matrix = [text_lst[i: i + col] for i in range(0, len(text_lst), col)]

        # Encrypt by reading matrix column-wise using sorted key
        cipher = ""
        for _, curr_idx in key_lst:
            cipher += ''.join([row[curr_idx] for row in matrix])

        return cipher

    else:
        sorted_key = sorted([(char, index) for index, char in enumerate(key)])

        # Divide the cipher into chunks
        # Min to handle cases where text length not be perfectly divisible
        segments = [text[i * row: min((i + 1) * row, len(text))] for i in range(col)]

        matrix = [[''] * col for _ in range(row)]

        # Return to plaintext order
        for idx, (_, orig_col_index) in enumerate(sorted_key):
            segment = segments[idx]
            for r in range(min(row, len(segment))):
                matrix[r][orig_col_index] = segment[r]

        plaintext = ''.join(''.join(row) for row in matrix)
        return plaintext.rstrip('_')


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
