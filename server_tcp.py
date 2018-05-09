import logging
from config import buffer_size
from server_connections import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def receive_from_client_tcp(current_client_socket: socket.socket,
                            address: socket.SocketType):
    while True:
        data = current_client_socket.recv(buffer_size)
        logger.debug("{} sent message: {}".format(address, data.decode()))

        if not data:
            with lock:
                del connected_clients[address]
            return

        with lock:
            for client_address, client_socket in connected_clients.items():
                if client_address != address:
                    client_socket.send(data)
