''' Contains classes & functions for server objects used for Machina Labs .stl file transport '''

import socket
import time
from typing import AnyStr, Tuple
import os
import filecmp
from . import file_utils


class TCPSocketUser():
    '''General class for object that communicates over TCP Sockets'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr):

        self.port_number = first_available_port_number
        self.first_available_port_number = first_available_port_number
        self.last_available_port_number = last_available_port_number
        self.host_name = host_name
        self.connected = False

    def bind(self):
        # Create socket object and bind to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.host_name, self.port_number))

    def connect(self):
        # Create socket object and connect to the port number
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((self.host_name, self.port_number))

    def increment_port_number(self):
        ''' Simply increments the port_number to use (until a point)'''
        if self.port_number < self.last_available_port_number:
            self.port_number += 1
        else:
            self.port_number = self.first_available_port_number

    def send_file(self, send_filename: AnyStr):
        '''Sends the contents of a file along the opened socket. '''

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
        '''Receives a file from the opened socket, saving the contents to a new file.'''

        # Listen for client connection
        self.s.listen(5)

        # Open the (new) file for receiving
        receive_file = open(receive_filename, 'wb')

        while(True):

            # Connect with client
            print('Waiting to establish TCP connection...')
            conn, addr = self.s.accept()
            self.connected = True
            print(f'Established connection with {addr}.')
            print('Receiving bytes...')

            # Receive the data (1024 bytes at a time)
            data_chunk = conn.recv(1024)
            while (True):
                print("Receiving bytes...")
                receive_file.write(data_chunk)
                if len(data_chunk) < 1024:
                    break
                data_chunk = conn.recv(1024)

            print('Done receiving bytes')

            # Finally, close the (new) file, socket, and leave the function
            receive_file.close()
            self.s.close()
            return

    def delete_file(self, filename):
        ''' Simply deletes a file (if it exists) '''
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("File to be deleted can't be found!")


class ProcessA(TCPSocketUser):
    '''Subclass of 'TCPSocketUser' that satisfies the conditions of "Process A" in Machina Labs assignment'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr, original_cad_filename: AnyStr, new_cad_filename: AnyStr):
        super().__init__(first_available_port_number, last_available_port_number, host_name)
        self.original_cad_filename = original_cad_filename
        self.new_cad_filename = new_cad_filename

    def send_file(self):
        ''' Overrides TCPSocketUser.send_file to throw an exception. '''
        raise AttributeError('\'ProcessA\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides TCPSocketUser.receive_file to add the new cad file name. '''
        raise AttributeError('\'ProcessA\' object has no attribute \'receive_file\'')

    @file_utils.function_timer
    def send_and_receive_file(self):
        ''' Simply sends and receives the file to/from Server B '''
        super().connect()
        super().send_file(self.original_cad_filename)
        super().increment_port_number()
        super().bind()
        super().receive_file(self.new_cad_filename)


class ProcessB(TCPSocketUser):
    '''Subclass of 'TCPSocketUser' that satisfies the conditions of "Process B" in Machina Labs assignment'''

    def __init__(self, first_available_port_number: int, last_available_port_number: int, host_name: AnyStr):
        super().__init__(first_available_port_number, last_available_port_number, host_name)

    def send_file(self):
        ''' Overrides TCPSocketUser.send_file to throw an exception. '''
        raise AttributeError('\'ProcessB\' object has no attribute \'send_file\'')

    def receive_file(self):
        ''' Overrides TCPSocketUser.receive_file to add the new cad file name. '''
        raise AttributeError('\'ProcessB\' object has no attribute \'receive_file\'')

    def rebound_file(self):
        ''' Performs "rebound" operation, receiving and immediately sending back file to Process A'''

        # First, receive the file
        super().bind()
        super().receive_file('temporary_file.stl')

        # TCP can take minutes to release a socket
        super().increment_port_number()

        # Then, send the file back
        super().connect()
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