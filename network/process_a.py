import socket
import time
from typing import AnyStr
from utils import simple_server

original_cad_filename = 'assets/cad_mesh.stl'
returned_cad_filename = 'assets/output.stl'

PORT_NUMBER = 8000
HOST_NAME = socket.gethostname()
SERVER_HOST_NAME = '192.168.1.162'

def main():
    # Initialize Server object
    cad_server_a = simple_server.CADServerA(port_number=PORT_NUMBER, host_name=HOST_NAME, 
                                            original_cad_filename=original_cad_filename, 
                                            new_cad_filename=returned_cad_filename)

    # Send and receive the CAD file to/from process B
    cad_server_a.send_and_receive_file()

    # Check whether the original and returned files are equivalent
    assert simple_server.is_same(original_cad_filename, returned_cad_filename)

    print("Task complete. The two files are equivalent!")

if __name__ == "__main__":
    main()
