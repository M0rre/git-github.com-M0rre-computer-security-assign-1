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
    col = len(key)
    row = (len(text) + col - 1) // col
    k_indx = 0


    if encrypt:
        cipher = ""

        text_lst = list(text)
        key_lst = sorted([(char, index) for index, char in enumerate(key)])

        # Pad the text with '_'
        fill_null = (row * col) - len(text)
        text_lst.extend('_' * fill_null)

        # Create matrix row-wise
        matrix = [text_lst[i: i + col] for i in range(0, len(text_lst), col)]

        # Read matrix column-wise using the sorted key
        for _, curr_idx in key_lst:
            cipher += ''.join([row[curr_idx] for row in matrix])

        return cipher

    else:
        plaintext = ""
        text_indx = 0

        key_lst = sorted([(char, index) for index, char in enumerate(key)])

        # Create an empty matrix for decrypted message
        dec_cipher = []
        for _ in range(row):
            dec_cipher += [[None] * col]

        # Fill the matrix column by column according to the key
        for _, curr_idx in key_lst:
            for j in range(row):
                if text_indx < len(text):
                    dec_cipher[j][curr_idx] = text[text_indx]
                    text_indx += 1

        # Flatten the matrix and convert it to a string
        plaintext = ''.join([char if char is not None else '' for row in dec_cipher for char in row])


        # Remove padding
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
