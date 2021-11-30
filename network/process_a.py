import socket
from typing import AnyStr
from utils import simple_tcp_socket_communicator
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-og_cad_fname", "--original_cad_filename", help="Original CAD Filename", default='assets/cad_mesh.stl')
parser.add_argument("-new_cad_fname", "--new_cad_filename", help="New CAD Filename", default='assets/output.stl')
parser.add_argument("-start_port", "--start_port_number", help="First available port number", default=8000)
parser.add_argument("-end_port", "--end_port_number", help="Last available port number", default=8100)
parser.add_argument("-shn", "--server_host_name", help="Host Name (IP Address) of main server (Process B)", default='192.168.1.162')

LOOPBACK_HOST_NAME = '127.0.0.1'

args = parser.parse_args()


def main():
    # Initialize Server object
    process_a = simple_tcp_socket_communicator.ProcessA(first_available_port_number=args.start_port_number, 
                                            last_available_port_number=args.end_port_number, 
                                            host_name=LOOPBACK_HOST_NAME, 
                                            original_cad_filename=args.original_cad_filename, 
                                            new_cad_filename=args.new_cad_filename)    

    # Send and receive the CAD file to/from process B
    process_a.send_and_receive_file()

    # Check whether the original and returned files are equivalent
    assert simple_tcp_socket_communicator.is_same(args.original_cad_filename, args.new_cad_filename)

    print("Task complete. The two files are equivalent!")


if __name__ == "__main__":
    main()
