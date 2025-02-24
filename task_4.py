from task_3 import substitution_cipher, transposition_cipher


def process_text(text, method, key, encrypt):
    if method == 's':
        return substitution_cipher(text, key, encrypt)
    elif method == 't':
        return transposition_cipher(text, key, encrypt)
    else:
        raise ValueError("Invalid encryption method.")


def retrieve_file_message(input_file, output_file, method, key, encrypt):
    # Read input file
    try:
        with open(input_file, 'r', encoding="UTF-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return

    # Process the content
    header = ''.join(lines[:7])
    content = ''.join(lines[7:-1])
    footer = lines[-1]

    content = process_text(content, method, key, encrypt)

    # Write to output file
    with open(output_file, 'w', encoding="UTF-8") as file:
        file.write(header)
        file.write(content)
        file.write(footer)


def main():
    operation = input("Choose operation (encrypt(E)/decrypt(D)): ").lower()
    method = input("Choose encryption method (substitution(S)/transposition(T)): ").lower()
    key = int(input("Enter the secret key: "))
    input_file = input("Input the name of the file you want to process: ")
    file_name, _ = input_file.split(".")  # Don't you dare have more than one dot in the file name
    output_file = file_name + "_enc.txt" if operation == 'e' else file_name + "_dec.txt"
    encrypt = operation == 'e'

    try:
        retrieve_file_message(input_file, output_file, method, key, encrypt)
        print(f"File successfully {'encrypted' if encrypt else 'decrypted'} and saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
