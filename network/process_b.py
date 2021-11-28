import socket
import time
from utils import simple_server

PORT_NUMBER = 8000
HOST_NAME = socket.gethostname()
CLIENT_HOST_NAME = '192.168.1.106'


def main():
    # Initialize Server object
    cad_server_b = simple_server.CADServerB(port_number=PORT_NUMBER, host_name=CLIENT_HOST_NAME)

    # Rebound the file from process A
    cad_server_b.rebound_file()

if __name__ == "__main__":
    main()
