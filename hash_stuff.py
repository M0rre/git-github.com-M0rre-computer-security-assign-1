import os
import matplotlib.pyplot as plt


def simple_hash(line, hash_size=256):
    hash_value = 0
    for char in line:
        # Add the ASCII value of each character to the hash value of the line
        hash_value = (hash_value + ord(char)) % hash_size
    return hash_value


def hash_file(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return []

    hash_values = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            hash_values.append(simple_hash(line))
    return hash_values


def uniformity_test(filename):
    hashes = hash_file(filename)
    plt.hist(hashes, bins=256, range=(0, 256))
    plt.title("Uniformity Test")
    plt.xlabel("Hash Value (0-255)")
    plt.ylabel("Frequency")
    plt.show()


def avalanche_test(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    differences = []
    for i in range(0, len(lines), 2):
        line1 = lines[i].strip()
        line2 = lines[i + 1].strip()
        hash1 = simple_hash(line1)
        hash2 = simple_hash(line2)
        # Calculate the number of differing bits
        diff_bits = bin(hash1 ^ hash2).count('1')  # Found online
        differences.append(diff_bits)

    plt.hist(differences, bins=range(9))
    plt.title("Avalanche Test")
    plt.xlabel("Number of Differing Bits")
    plt.ylabel("Frequency")
    plt.show()


avalanche_test("a.txt")
uniformity_test("u.txt")
