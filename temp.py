def transposition_cipher(text, key, encrypt):
    col = len(key)
    row = (len(text) + col - 1) // col

    if encrypt:
        cipher = ""

        # Create key mapping - sort key characters and keep track of original positions
        key_mapping = sorted([(char, index) for index, char in enumerate(key)])

        # Pad the text with '_'
        text_padded = text + '_' * ((row * col) - len(text))

        # Create matrix row-wise
        matrix = [list(text_padded[i: i + col]) for i in range(0, len(text_padded), col)]

        # Read matrix column-wise using the sorted key
        for _, original_idx in key_mapping:
            for i in range(row):
                cipher += matrix[i][original_idx]

        return cipher

    else:
        # Create empty result matrix
        matrix = [[None for _ in range(col)] for _ in range(row)]
        
        # Create key mapping
        original_order = [(char, idx) for idx, char in enumerate(key)]
        key_mapping = sorted(original_order, key=lambda x: x[0])  # Sort by character
        
        # Calculate characters per column
        chars_per_col = row
        
        # Fill the matrix column by column according to the sorted key
        current_idx = 0
        for _, original_idx in key_mapping:
            for i in range(row):
                if current_idx < len(text):
                    matrix[i][original_idx] = text[current_idx]
                    current_idx += 1
        
        # Read the matrix row by row to get the original text
        plaintext = ""
        for i in range(row):
            for j in range(col):
                if matrix[i][j] is not None:
                    plaintext += matrix[i][j]
        
        # Remove padding
        return plaintext.rstrip('_')