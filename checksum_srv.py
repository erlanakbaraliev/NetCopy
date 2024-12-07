import socket
import select
import time

# Store checksums in a dictionary
checksum_data = {}

def cleanup_expired_checksums():
    """Remove expired checksums."""
    current_time = time.time()
    expired_ids = [file_id for file_id, (_, expiration) in checksum_data.items() if expiration < current_time]
    for file_id in expired_ids:
        del checksum_data[file_id]

def process_client_message(client_socket):
    """Handle client messages."""
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return False  # Client disconnected

        parts = data.split('|')
        if parts[0] == 'BE':  # Insert checksum
            file_id, validity, length, checksum = parts[1], int(parts[2]), int(parts[3]), parts[4]
            expiration = time.time() + validity
            checksum_data[file_id] = (checksum, expiration)
            client_socket.sendall(b'OK')
        elif parts[0] == 'KI':  # Retrieve checksum
            file_id = parts[1]
            cleanup_expired_checksums()
            if file_id in checksum_data:
                checksum, _ = checksum_data[file_id]
                client_socket.sendall(f"{len(checksum)}|{checksum}".encode())
            else:
                client_socket.sendall(b"0|")
        return True
    except Exception as e:
        print(f"Error handling client message: {e}")
        return False

def start_server(ip, port):
    """Start the checksum server."""
    # Create and bind the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()
    server_socket.setblocking(False)
    print(f"Checksum server started on {ip}:{port}")

    # Manage sockets using select
    sockets_list = [server_socket]  # List of sockets to monitor
    clients = {}  # Map of client sockets to addresses

    while True:
        # Monitor sockets for read activity
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                # Handle new client connection
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"New connection from {client_address}")
            else:
                # Handle data from an existing client
                if not process_client_message(notified_socket):
                    # Remove disconnected client
                    print(f"Connection closed from {clients[notified_socket]}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    notified_socket.close()

if __name__ == "__main__":
    import sys
    ip, port = sys.argv[1], int(sys.argv[2])
    start_server(ip, port)
