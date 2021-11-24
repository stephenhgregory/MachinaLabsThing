import socket
import time
from typing import AnyStr
import os

original_cad_filename = 'assets/cad_mesh.stl'
returned_cad_filename = 'assets/output.stl'


class Server():

    def __init__(self, port_number: AnyStr, host_name: AnyStr):
        self.port_number = port_number
        self.host_name = host_name

        # Create socket object and bind to the port number
        self.s = socket.socket()
        self.s.bind((self.host_name, self.port_number))

    def send_file(self, send_filename: AnyStr):

        # Open the file for sending
        send_file = open(send_filename, 'rb')

        # Send the file 1024 bytes at a time, until the whole file is sent
        print('Sending cad data...')
        data_chunk = send_file.read(1024)
        while(data_chunk):
            print("Sending cad data...")
            self.s.send(data_chunk)
            data_chunk = send_file.read(1024)
        # Finally, close the original file
        send_file.close()
        print("Done sending cad data!")

    def receive_file(self, receive_filename: AnyStr):

        # Open the (new) file for receiving
        receive_file = open(receive_filename, 'wb')

        # Listen for the client connection
        self.s.listen(5)

        # Connect with client
        c, addr = self.s.accept()
        print(f'Established connection with {addr}.')
        print('Receiving bytes...')

        # Receive the data (1024 bytes at a time)
        data_chunk = c.recv(1024)
        while (data_chunk):
            print("Receiving bytes...")
            receive_file.write(data_chunk)
            data_chunk = c.recv(1024)

            print('Done receiving bytes')

        # Finally, close the (new) file
        receive_file.close()

    def delete_file(self, filename):
        ''' Simply deletes a file (if it exists) '''
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File to be deleted can't be found!")


class CADServerA(Server):

    def __init__(self, port_number: AnyStr, host_name: AnyStr, original_cad_filename: AnyStr, new_cad_filename: AnyStr):
        # Call the superclass constructor for a basic server
        super().__init__(port_number, host_name)

        # Set the filenames for the CAD files
        self.original_cad_filename = original_cad_filename
        self.new_cad_filename = new_cad_filename

    def send_file(self):
        ''' Overrides Server.send_file to add the original cad file name. '''
        super().send_file(self, self.original_cad_filename)

    def receive_file(self):
        ''' Overrides Server.receive_file to add the new cad file name. '''
        super().receive_file(self, self.new_cad_filename)


class CADServerB(Server):

    def __init__(self, port_number: AnyStr, host_name: AnyStr, original_cad_filename: AnyStr, new_cad_filename: AnyStr):
        # Call the superclass constructor for a basic server
        super().__init__(port_number, host_name)

        # Set the filenames for the CAD files
        self.original_cad_filename = original_cad_filename
        self.new_cad_filename = new_cad_filename

    def send_file(self):
        ''' Overrides Server.send_file to throw an exception. '''
        raise AttributeError('\'CADServerB\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides Server.receive_file to add the new cad file name. '''
        raise AttributeError('\'CADServerB\' object has no attribute \'receive_file\'')

    def rebound_file(self):
        # First, receive the file
        super().receive_file(self, 'temporary_file.stl')

        # Then, send the file back
        super().send_file(self, 'temporary_file.stl')

        # Finally, delete the file
        super().delete_file('temporary_file.stl')