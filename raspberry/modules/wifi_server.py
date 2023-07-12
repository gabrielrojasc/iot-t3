import socket
import time
import sys
import select
from struct import pack

from .unpacking import parse_data
from .db import get_configs


def TCP_frag_recv(conn):
    doc = b""
    while True:
        try:
            # conn.settimeout(5)
            data = conn.recv(1024)
            if data == b"\0":
                break
            else:
                doc += data
        except socket.timeout:
            conn.send(b"\0")
            raise socket.timeout
        except Exception:
            conn.send(b"\0")
            raise
        conn.send(b"\1")
    return doc


def UDP_frag_recv(s):
    doc = b""
    addr = None
    while True:
        try:
            data, addr = s.recvfrom(1024)
            if data == b"\0":
                break
            else:
                doc += data
        except socket.timeout:
            raise socket.timeout
        except Exception:
            raise
        s.sendto(b"\1", addr)
    return (doc, addr)


def send_config(socket, protocol, transport_layer):
    packet = pack("<2c", str(protocol).encode(), str(transport_layer).encode())
    socket.sendall(packet)
    print(f"Enviado: {packet}")
    current_time = time.time()
    packet = pack("<q", int(current_time))
    socket.sendall(packet)
    print(f"Enviado: {packet}")


def create_socket_UDP(host, port):
    sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet  # UDP
    sUDP.bind((host, port))
    sUDP.settimeout(5)
    return sUDP


def main(host, tcp_port, udp_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # internet  # TCP
    s.bind((host, tcp_port))
    s.listen(5)
    print(f"Listening on {host}:{tcp_port}")

    # UDP SOCKET
    sUDP = create_socket_UDP(host, udp_port)

    # TCP: 1; UDP: 0
    transport_layer = 1
    buffer = 1024

    for protocol, transport_layer in get_configs():
        print("Esperando conexión...")
        conn, addr = s.accept()
        print(f"Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}")
        send_config(conn, protocol, transport_layer)
        data = b""
        for _ in range(5):
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1)
                if key == "n":
                    break
                else:
                    print(f"Key '{key}' pressed!")

            try:
                if transport_layer == 1:  # TCP
                    data = TCP_frag_recv(conn)
                else:  # UDP
                    data, udp_addr = UDP_frag_recv(sUDP)
            except ConnectionResetError:
                break
            except socket.timeout:
                print("Timeout")
                break

            if data == b"":
                continue

            print(f"Recibido raw:\n{data}")

            parsed_data = parse_data(data, protocol)

            if parsed_data is not None:
                print(f"Recibido:\n{parsed_data}")
                transport_layer = parsed_data.get("transport_layer")

        conn.sendall(b"\2")
        conn.close()
        if transport_layer == 0:
            sUDP.sendto(b"\2", udp_addr)
            sUDP.close()
            sUDP = create_socket_UDP()

        print("Desconectado")


def run(host, tcp_port, udp_port, status, protocol):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # internet  # TCP
    s.bind((host, tcp_port))
    s.listen(5)
    print(f"Listening on {host}:{tcp_port}")

    # UDP SOCKET
    sUDP = create_socket_UDP(host, udp_port)

    # TCP: 1; UDP: 0
    status = 1
    buffer = 1024

    print("Esperando conexión...")
    conn, addr = s.accept()
    print(f"Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}")
    send_config(conn, protocol, status)
    data = b""
    for _ in range(5):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            key = sys.stdin.read(1)
            if key == "n":
                break
            else:
                print(f"Key '{key}' pressed!")

        try:
            if status == 20:  # TCP config BD
                # TODO: Implementar esto
                ...
            elif status == 21:  # TCP Continuous
                data = TCP_frag_recv(conn)
            elif status == 21:  # TCP Discontinous
                # TODO: Implementar esto
                ...
            else:  # UDP
                data, udp_addr = UDP_frag_recv(sUDP)
        except ConnectionResetError:
            break
        except socket.timeout:
            print("Timeout")
            break

        if data == b"":
            continue

        print(f"Recibido raw:\n{data}")

        parsed_data = parse_data(data, protocol)

        if parsed_data is not None:
            print(f"Recibido:\n{parsed_data}")
            status = parsed_data.get("transport_layer")

    conn.sendall(b"\2")
    conn.close()
    if status == 0:
        sUDP.sendto(b"\2", udp_addr)
        sUDP.close()
        sUDP = create_socket_UDP()

    print("Desconectado")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    TCP_PORT = 8000
    UDP_PORT = 8010
    main(HOST, TCP_PORT, UDP_PORT)
