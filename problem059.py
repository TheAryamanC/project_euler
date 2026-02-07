"""
Project Euler - Problem 59: XOR Decryption

Each character on a computer is assigned a unique code and the preferred
standard is ASCII. For example, uppercase A = 65, asterisk (*) = 42, and
lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII,
then XOR each byte with a given value, taken from a secret key. The advantage 
with the XOR function is that using the same encryption key on the cipher text, 
restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, 
and the key is made up of random bytes. The user would keep the encrypted message 
and the encryption key in different locations, and without both "halves", it is 
impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method 
is to use a password as a key. If the password is shorter than the message, which 
is likely, the key is repeated cyclically throughout the message. The balance for 
this method is using a sufficiently long password key for security, but short enough 
to be memorable.

Your task has been made easy, as the encryption key consists of three lower
case characters. Using the cipher file containing the encrypted ASCII codes,
and the knowledge that the plain text must contain common English words,
decrypt the message and find the sum of the ASCII values in the original text.
"""

def solution():
    with open('additional_files/cipher.txt') as f:
        cipher = list(map(int, f.read().strip().split(',')))

    best_sum = 0
    
    for a in range(ord('a'), ord('z') + 1):
        for b in range(ord('a'), ord('z') + 1):
            for c in range(ord('a'), ord('z') + 1):
                key = [a, b, c]
                decrypted = []
                for i, char in enumerate(cipher):
                    decrypted.append(chr(char ^ key[i % 3]))
                
                text = ''.join(decrypted)
                # check for common words that are likely to be in the decrypted text
                ## not robust - should ideally check for multiple common words, but this is a quick heuristic
                if ' the ' in text.lower() and ' and ' in text.lower():
                    ascii_sum = sum(ord(c) for c in text)
                    if ascii_sum > best_sum:
                        best_sum = ascii_sum
    
    return best_sum

if __name__ == "__main__":
    print(solution())  # Answer: 129448
