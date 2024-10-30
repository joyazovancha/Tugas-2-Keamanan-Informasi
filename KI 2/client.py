import socket
import threading
from implementasides import encrypt, pad_text, decrypt, bit_array_to_string, unpad_text

# Load the shared key
with open("shared_key.bin", "rb") as key_file:
    key = key_file.read()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

def receive_messages():
    while True:
        encrypted_response = client_socket.recv(4096)
        if not encrypted_response:
            break
        encrypted_bits = list(map(int, encrypted_response.decode()))
        decrypted_bits = decrypt(encrypted_bits, key)
        decrypted_text = bit_array_to_string(decrypted_bits)
        unpadded_text = unpad_text(decrypted_text)
        print(f"Pesan yang diterima: {unpadded_text.strip()}")

# Start a thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    plain_text = input("Masukkan teks untuk dienkripsi dan dikirim (atau ketik 'exit' untuk keluar): ")
    if plain_text.lower() == 'exit':
        break
    
    padded_text = pad_text(plain_text)
    cipher_bits = encrypt(padded_text, key)
    cipher_text = ''.join(map(str, cipher_bits))

    client_socket.send(cipher_text.encode())
    print("Pesan terenkripsi telah dikirim.")

client_socket.close()
