import socket
import time

original_cad_filename = 'assets/cad_mesh.stl'
returned_cad_filename = 'assets/output.stl'


def send_cad_file():

    # Create socket object
    s = socket.socket()

    # Choose a port to send / receive data over
    port = 8000

    # Get the host IP Address
    host_name = socket.gethostname()

    # Bind to the port
    s.bind((host_name, port))

    # Open the cad file for sending
    original_cad_file = open('assets/cad_mesh.stl', 'rb')

    # Open the new cad file for receiving
    returned_cad_file = open('assets/output.stl', 'wb')

    # Send the file 1024 bytes at a time, until the whole file is sent
    print('Sending cad data...')
    data_chunk = original_cad_file.read(1024)
    while(data_chunk):
        print("Sending cad data...")
        s.send(data_chunk)
        data_chunk = original_cad_file.read(1024)
    # Finally, close the original file
    original_cad_file.close()
    print("Done sending cad data!")

    # Signify that we're done sending data
    s.shutdown()






