"""
[THIS SOFTWARE IF PUBLISHED UNDER THE MIT LICENCE]
------------------------------------------
Copyright (c) 2024 OverclockedD2

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-----------------------------------------

This is the source code of the easier_sockets library made by OverclockedD2.
This library makes Python sockets even easier to use and is great for beginners
to understand the basics of networking. The code is pretty simple to understand, but
if in case it is still unclear, then check out the documentation here: https://github.com/OverclockedD2/easier_sockets/.
"""

import socket as s
import rsa

class client:
    def __init__(self, server_port: int, server_name: str = "127.0.0.1", name: str = None, port: int = None, encrypted: bool = False, rsa_key_size: int = 2048, packet_size: int = 8192, timeout: float = 600):
        self.name = name
        self.port = port
        self.server_name = server_name
        self.server_port = server_port
        self.encrypted = encrypted
        self.rsa_key_size = rsa_key_size
        self.packet_size = packet_size
        self.timeout = timeout

        self.client = s.socket(s.AF_INET, s.SOCK_STREAM)
        if self.name is not None and self.port is not None:
            self.client.bind((self.name, self.port))
        self.client.settimeout(self.timeout)

        self.server_public_key = None
        self.own_public_key = None
        self.own_private_key = None
    def send_packet(self, content: str):
        if self.encrypted:
            self.client.send(rsa.encrypt(content.encode("utf-8"), self.server_public_key).hex().encode("utf-8"))
        else:
            self.client.send(content.encode("utf-8"))
    def receive_packet(self):
        if self.encrypted:
            return rsa.decrypt(bytes.fromhex(self.client.recv(4096).decode("utf-8")), self.own_private_key).decode("utf-8")
        else:
            return self.client.recv(4096).decode("utf-8")
    def connect(self):
        self.client.connect((self.server_name, self.server_port))

        if self.encrypted:
            # Exchanging public keys
            self.own_public_key, self.own_private_key = rsa.newkeys(self.rsa_key_size)
            response = self.client.recv(4096).decode("utf-8").split()
            self.server_public_key = rsa.key.PublicKey(int(response[0]), int(response[1]))
            self.client.send(f"{self.own_public_key.n} {self.own_public_key.e}".encode("utf-8"))
    def disconnect(self):
        self.client = s.socket(s.AF_INET, s.SOCK_STREAM)
        if self.name is not None and self.port is not None:
            self.client.bind((self.name, self.port))
        self.client.settimeout(self.timeout)
    def terminate(self):
        self.client.close()

    # Shortcuts for even easier and faster use
    def s(self, content: str): self.send_packet(content)
    def r(self): return self.receive_packet()
    def c(self): self.connect()
    def d(self): self.disconnect()
    def t(self): self.terminate()

class server:
    def __init__(self, port: int = 0, name: str = "0.0.0.0", client_name: str = None, client_port: int = None, encrypted: bool = False, rsa_key_size: int = 2048, packet_size: int = 8192, queue_size: int = 8, timeout: float = 600):
        self.name = name
        self.port = port
        self.client_name = client_name
        self.client_port = client_port
        self.encrypted = encrypted
        self.rsa_key_size = rsa_key_size
        self.packet_size = packet_size
        self.queue_size = queue_size
        self.timeout = timeout

        self.server = None
        self.client_info = None
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.bind((self.name, self.port))
        self.socket.settimeout(self.timeout)
        self.socket.listen(self.queue_size)
        self.name = self.socket.getsockname()[0]
        self.port = self.socket.getsockname()[1]

        self.client_public_key = None
        self.own_public_key = None
        self.own_private_key = None
    def send_packet(self, content: str):
        if self.encrypted:
            self.server.send(rsa.encrypt(content.encode("utf-8"), self.client_public_key).hex().encode("utf-8"))
        else:
            self.server.send(content.encode("utf-8"))
    def receive_packet(self):
        if self.encrypted:
            return rsa.decrypt(bytes.fromhex(self.server.recv(self.packet_size).decode("utf-8")), self.own_private_key).decode("utf-8")
        else:
            return self.server.recv(self.packet_size).decode("utf-8")
    def accept(self):
        self.server, self.client_info = self.socket.accept()
        if (self.client_name, self.client_port) != (None, None) and self.client_info != (self.client_name, self.client_port):
            self.kick()
        if self.encrypted:
            # Exchanging public keys
            self.own_public_key, self.own_private_key = rsa.newkeys(self.rsa_key_size)
            self.server.send(f"{self.own_public_key.n} {self.own_public_key.e}".encode("utf-8"))
            response = self.server.recv(self.packet_size).decode("utf-8").split()
            self.client_public_key = rsa.key.PublicKey(int(response[0]), int(response[1]))
    def kick(self):
        self.server.close()
        self.client_info = None
    def terminate(self):
        self.server.close()
        self.socket.close()

    # Shortcuts for even easier and faster use
    def s(self, content: str): self.send_packet(content)
    def r(self): return self.receive_packet()
    def c(self): self.accept()
    def d(self): self.kick()
    def t(self): self.terminate()
