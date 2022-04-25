import socket


def run_server(host, port):
    """
    Runs a server that can host a new game\n
    host - host IP address\n
    port - port to run a server on
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
        print("Socket successfully created")
    except socket.error as e:
        print("Socket creation failed with error", str(e))

    s.listen()
    print("Sever started, waiting for a connection")

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
