import random

def transposition_cipher(text, key, encrypt=True):
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
        ciphertext = ''
        for col in col_order:
            for row in range(num_rows):
                ciphertext += matrix[row][col]
        return ciphertext

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

# Example usage:
key = 5
text = """HELLOWORLD
test with newlines"""

# Encrypt
encrypted_text = transposition_cipher(text, key, encrypt=True)
print("Encrypted:", encrypted_text)

# Decrypt
decrypted_text = transposition_cipher(encrypted_text, key, encrypt=False)
print("Decrypted:", decrypted_text)