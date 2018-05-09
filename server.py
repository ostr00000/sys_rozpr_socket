import logging
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from server_tcp import receive_from_client_tcp
from server_udp import receive_from_client_udp
from server_connections import *
from config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    executor = ThreadPoolExecutor(max_workers=3)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()

    t = Thread(target=receive_from_client_udp, name='udp_thread')
    t.daemon = True
    t.start()

    logger.debug("Server started")
    while True:
        client_socket, client_address = sock.accept()
        logger.debug("New connection accepted from {}".format(client_address))
        with lock:
            connected_clients[client_address] = client_socket
        executor.submit(receive_from_client_tcp, client_socket, client_address)
