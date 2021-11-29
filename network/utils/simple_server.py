''' Contains classes & functions for server objects used for Machina Labs .stl file transport '''

import socket
import time
from typing import AnyStr
import os
import filecmp
from . import file_utils


class Server():
    '''General class for Server object that communicates over TCP Sockets'''

    def __init__(self, port_number: AnyStr, host_name: AnyStr):
        self.port_number = port_number
        self.host_name = host_name

        # Create socket object and bind to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        self.s.listen(2)

        while(True):

            # Connect with client
            print('Waiting to establish TCP connection...')
            conn, addr = self.s.accept()
            print(f'Established connection with {addr}.')
            print('Receiving bytes...')

            # Receive the data (1024 bytes at a time)
            data_chunk = conn.recv(1024)
            while (data_chunk):
                print("Receiving bytes...")
                receive_file.write(data_chunk)
                data_chunk = conn.recv(1024)

                print('Done receiving bytes')

            # Finally, close the (new) file and leave the function
            receive_file.close()
            return

    def delete_file(self, filename):
        ''' Simply deletes a file (if it exists) '''
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File to be deleted can't be found!")


class CADServerA(Server):
    '''Subclass of 'Server' that satisfies the conditions of "Process A" in Machina Labs assignment'''

    def __init__(self, port_number: AnyStr, host_name: AnyStr, original_cad_filename: AnyStr, new_cad_filename: AnyStr):
        # Call the superclass constructor for a basic server
        super().__init__(port_number, host_name)

        # Set the filenames for the CAD files
        self.original_cad_filename = original_cad_filename
        self.new_cad_filename = new_cad_filename

    @file_utils.function_timer
    def send_and_receive_file(self):
        ''' Simply sends and receives the file to/from Server B '''
        super().send_file(self.original_cad_filename)
        super().receive_file(self.new_cad_filename)


class CADServerB(Server):
    '''Subclass of 'Server' that satisfies the conditions of "Process B" in Machina Labs assignment'''

    def __init__(self, port_number: AnyStr, host_name: AnyStr):

        # TODO: Better Docs
        self.port_number = port_number
        self.host_name = host_name

        # Create socket objeƒserverct and bind to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((self.host_name, self.port_number))

    def send_file(self):
        ''' Overrides Server.send_file to throw an exception. '''
        raise AttributeError('\'CADServerB\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides Server.receive_file to add the new cad file name. '''
        raise AttributeError('\'CADServerB\' object has no attribute \'receive_file\'')

    def rebound_file(self):
        # First, receive the file
        super().receive_file('temporary_file.stl')

        # Then, send the file back
        super().send_file('temporary_file.stl')

        # Finally, delete the file
        super().delete_file('temporary_file.stl')


def is_same(filename1: AnyStr, filename2: AnyStr) -> bool:
    '''Check whether two files are equivalent'''
    return filecmp.cmp(filename1, filename2)

def function_timer(func):
    def wrapper_function(*args, **kwargs):
        t1 = time.time()
        func(*args,  **kwargs)
        t2 = time.time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
    return wrapper_function