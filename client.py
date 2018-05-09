import socket
import struct
from threading import Thread
import logging
from config import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

nickname = "anonymous"


def end():
    global end_flag
    end_flag = True


def set_name():
    global nickname
    nickname = input("Get name:")
    print("Name is changed to: '{}'".format(nickname))


def change_send_type(send_typ):
    protocols = {'T': "Tcp", 'U': "Udp", 'M': "Multicast"}

    def inner():
        global send_type
        send_type = send_typ
        print("Currently using protocol is: {}".format(protocols[send_typ]))

    return inner


actions = {
    'Q': end,
    'R': set_name,
    'T': change_send_type('T'),
    'U': change_send_type('U'),
    'M': change_send_type('M'),
}


def send_tcp(msg):
    tcp.send(msg)


def send_udp(msg):
    udp.sendto(msg, server_address)


def send_multicast(msg):
    multicast.sendto(msg, multicast_address)


send_functions = {
    'T': send_tcp,
    'U': send_udp,
    'M': send_multicast,
}


def receive_from_server(soc: socket.socket):
    while True:
        rec_data, adr = soc.recvfrom(buffer_size)
        logger.debug("adr:{}".format(adr))
        print("{}".format(rec_data.decode()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(server_address)
    Thread(target=receive_from_server, args=(tcp,), daemon=True).start()

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(tcp.getsockname())
    Thread(target=receive_from_server, args=(udp,), daemon=True).start()

    multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    group = socket.inet_aton(multicast_address[0])
    mem_req = struct.pack('4sL', group, socket.INADDR_ANY)

    multicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    multicast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    multicast.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mem_req)
    multicast.bind(('', 12345))
    Thread(target=receive_from_server, args=(multicast,), daemon=True).start()

    send_type = 'T'
    end_flag = False
    logger.debug("Client is started")

    while not end_flag:
        data = input()

        if len(data) == 1 and data.upper() in actions:
            logger.debug("Execution action {}".format(data))
            actions[data.upper()]()

        else:
            data = nickname + ":" + data[:buffer_size - len(nickname) - 1]
            if send_type != 'M':
                print("{}".format(data))
            send_functions[send_type](data.encode())
