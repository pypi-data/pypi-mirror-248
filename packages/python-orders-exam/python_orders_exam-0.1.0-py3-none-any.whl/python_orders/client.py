import socket


def run_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((host, port))

        while True:
            # Get user input
            message = input("Enter your message (type 'quit' to exit): ")

            # Send the message to the server
            s.sendall(message.encode())

            if message.lower() == "quit":
                break

            # Receive response from the server
            data = s.recv(1024)
            print("Received from server:", data.decode())

        s.close()


if __name__ == "__main__":
    HOST = "localhost"  # The server's hostname or IP address
    PORT = 15555  # The port used by the server

    run_client(HOST, PORT)
