import socket
import hashlib
import sys

def calculate_checksum(filepath):
    """Calculate MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_checksum(chsum_srv_ip, chsum_srv_port, file_id):
    message = f"KI|{file_id}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checksum_socket:
        checksum_socket.connect((chsum_srv_ip, chsum_srv_port))
        checksum_socket.sendall(message.encode())
        response = checksum_socket.recv(1024).decode()
        if response == "0|":
            return None
        return response.split('|')[1]

def start_server(srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((srv_ip, srv_port))
        server_socket.listen()
        print(f"Netcopy server listening on {srv_ip}:{srv_port}")

        conn, addr = server_socket.accept()
        with conn:
            with open(filepath, "wb") as file:
                while chunk := conn.recv(8192):
                    file.write(chunk)
        
        local_checksum = calculate_checksum(filepath)
        remote_checksum = get_checksum(chsum_srv_ip, chsum_srv_port, file_id)

        if local_checksum == remote_checksum:
            print("CSUM OK")
        else:
            print("CSUM CORRUPTED")

if __name__ == "__main__":
    srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath = sys.argv[1:]
    srv_port, chsum_srv_port = int(srv_port), int(chsum_srv_port)
    file_id = int(file_id)

    start_server(srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath)
