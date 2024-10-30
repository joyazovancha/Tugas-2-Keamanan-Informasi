import socket
from implementasides import encrypt, pad_text

# Load the shared key
with open("shared_key.bin", "rb") as key_file:
    key = key_file.read()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

plain_text = input("Masukkan teks untuk dienkripsi dan dikirim: ")
padded_text = pad_text(plain_text)

cipher_bits = encrypt(padded_text, key)
cipher_text = ''.join(map(str, cipher_bits))

client_socket.send(cipher_text.encode())
print("Pesan terenkripsi telah dikirim ke server.")

client_socket.close()
