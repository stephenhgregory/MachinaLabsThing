import socket
import time
from typing import AnyStr
from utils import simple_server


ORIGINAL_CAD_FILENAME = 'assets/cad_mesh.stl'
RETURNED_CAD_FILENAME = 'assets/output.stl'
PORT_NUMBER = 8000
HOST_NAME = socket.gethostname()
LOOPBACK_HOST_NAME = '127.0.0.1'
SERVER_HOST_NAME = '192.168.1.162'


def main():
    # Initialize Server object
    cad_server_a = simple_server.CADServerA(port_number=PORT_NUMBER, host_name=SERVER_HOST_NAME, 
                                            original_cad_filename=ORIGINAL_CAD_FILENAME, 
                                            new_cad_filename=RETURNED_CAD_FILENAME)

    # Send and receive the CAD file to/from process B
    cad_server_a.send_and_receive_file()

    # Check whether the original and returned files are equivalent
    assert simple_server.is_same(ORIGINAL_CAD_FILENAME, RETURNED_CAD_FILENAME)

    print("Task complete. The two files are equivalent!")

if __name__ == "__main__":
    main()
