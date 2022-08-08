import argparse
import socket

def basic_client(port=5000, max_length=1440):
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1',port))
    message = input(' -> ')
    while message.lower().strip() != 'exit':
        if len(message) >= max_length:
            print("message is too long, try less verbose message")
            continue
        data = message.encode()
        client_socket.send(data)
        print(f"sent: {data}")
        message = input(' -> ')
    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="example socket server")
    parser.add_argument("-p","--port",type=int,default=5000,help="port")
    parser.add_argument("-l","--max_length",type=int,default=1440,help="maximum number of bytes to read and write per message")
    args = vars(parser.parse_args())
    basic_client(args["port"],args["max_length"])
    print('exiting program')
