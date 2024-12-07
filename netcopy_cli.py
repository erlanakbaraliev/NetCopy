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

def send_to_server(file_path, srv_ip, srv_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((srv_ip, srv_port))
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                client_socket.sendall(chunk)
        client_socket.shutdown(socket.SHUT_WR)

def send_checksum(chsum_srv_ip, chsum_srv_port, file_id, checksum):
    message = f"BE|{file_id}|60|{len(checksum)}|{checksum}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as checksum_socket:
        checksum_socket.connect((chsum_srv_ip, chsum_srv_port))
        checksum_socket.sendall(message.encode())
        response = checksum_socket.recv(1024).decode()
        if response != "OK":
            print("Checksum server error")

if __name__ == "__main__":
    srv_ip, srv_port, chsum_srv_ip, chsum_srv_port, file_id, filepath = sys.argv[1:]
    srv_port, chsum_srv_port = int(srv_port), int(chsum_srv_port)
    file_id = int(file_id)

    checksum = calculate_checksum(filepath)
    send_to_server(filepath, srv_ip, srv_port)
    send_checksum(chsum_srv_ip, chsum_srv_port, file_id, checksum)
