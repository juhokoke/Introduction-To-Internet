#!/usr/bin/python
# -*- coding: utf-8 -*-

# The modules required
import sys
import socket
import struct
import string
'''
Simple udp and tcp client for "Introduction To Internet" course.

It takes 3 commandline arguments and calls function send_and_receive_tcp.
You can execute this file with the command:
python3 tcp-udp.py <ip> <port> <message>

This template doesn't have any extra features, implement them by yourself. ;)
'''
def send_and_receive_tcp(address, port, message):
    print("You gave arguments: {} {} {}".format(address, port, message))
    # create TCP socket
    s = socket.socket()
    # connect socket to given address and port
    s.connect((address, port))
    # python3 sendall() requires bytes like object. encode the message with str.encode() command
    message = message.encode() # Could have used the "utf-8" encoding here aswell
    # send given message to socket
    s.sendall(message)
    # receive data from socket
    message = s.recv(1024)
    # data you received is in bytes format. turn it to string with .decode() command
    message = message.decode()
    # print received data
    print("Recived data: ", message)
    # close the socket
    s.close()
    # Get your CID and UDP port from the message
    message = message.split()
    cid = message[1]
    port = message[2]
    # Continue to UDP messaging. You might want to give the function some other parameters like the above mentioned cid and port.
    send_and_receive_udp(address, port, cid)
    return


def send_and_receive_udp(address, port, cid):
    '''
    Implement UDP part here.
    '''
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "Hello from "+cid
    print("Sending message: ", message) 
    msg_length = len(message)
    ack = True
    eom = False
    remaining = 0
    cid_e = cid.encode("utf-8")
    message = message.encode("utf-8")
    msg = struct.pack("!8s??HH128s", cid_e, ack, eom, remaining, msg_length, message)

    s.sendto(msg, (address, port))

    while True:
        message_r, _ = s.recvfrom(2048)
        
        _, _, eom_r, _, lenght, message = struct.unpack("!8s??HH128s", message_r)
        message = message.decode("utf-8")
        print("Recived message: ", message)

        if eom_r == True:
            break
        else:
            message = message[0:lenght]
            message = message.split()
            temp = ""
            ln = len(message)
            for i in range(ln):
                temp = temp+message[ln-1]+" "
                ln = ln-1
            # Here you could use the previous "message" variable to save 1kb of ram.
            message_s = temp.rstrip(" ")

            print("Sending message: ", message_s)
            msg_length = len(message_s)
            message_s = message_s.encode("utf-8")
            msg = struct.pack("!8s??HH128s", cid_e, ack, eom, remaining, msg_length, message_s)
            s.sendto(msg, (address, port))

    s.close
    return


def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]

    try:
        # Get the server address, port and message from command line arguments
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
        # Print usage instructions and exit if we didn't get proper arguments
        sys.exit(USAGE)

    send_and_receive_tcp(server_address, server_tcpport, message)


if __name__ == '__main__':
    # Call the main function when this script is executed
    main()