import logging
from config import *
from server_connections import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def receive_from_client_udp():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(server_address)

    while True:
        data, address = udp.recvfrom(buffer_size)
        logger.debug("{} sent message: {}".format(address, data.decode()))

        with lock:
            for client_address, client_socket in connected_clients.items():
                if client_address != address:
                    udp.sendto(data, client_address)
