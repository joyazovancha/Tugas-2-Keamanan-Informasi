import socket
from implementasides import decrypt, generate_key, bit_array_to_string, unpad_text

# Generate and save the key
key = generate_key()
with open("shared_key.bin", "wb") as key_file:
    key_file.write(key)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)
print("Server siap menerima pesan terenkripsi...")

while True:
    conn, addr = server_socket.accept()
    print(f"Koneksi dari {addr}")
    
    encrypted_data = conn.recv(4096)
    encrypted_bits = list(map(int, encrypted_data.decode()))
    
    decrypted_bits = decrypt(encrypted_bits, key)
    decrypted_text = bit_array_to_string(decrypted_bits)
    unpadded_text = unpad_text(decrypted_text)
    
    print(f"Teks setelah dekripsi: {unpadded_text.strip()}")
    
    conn.close()
