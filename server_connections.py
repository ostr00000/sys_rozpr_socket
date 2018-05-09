import threading
from typing import Dict
import socket

lock = threading.Lock()
connected_clients: Dict[socket.SocketType, socket.socket] = {}
