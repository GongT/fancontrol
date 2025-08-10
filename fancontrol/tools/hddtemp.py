import socket
from posixpath import basename
from traceback import print_exc

from .temp import StaticTemp, Temp


def hddtemp_client():
    text = _read()
    line_num = 0
    temps: list[Temp] = []
    for line in text.strip("|").split("||"):
        try:
            line_num += 1
            parts = line.split("|")

            block_device = parts[0]
            title = parts[1]
            value = parts[2].strip()
        except Exception as e:
            print(f"[hddtemp] failed parse line [{line}]: {e}")
            continue

        if value == "SLP":
            continue

        if value == "ERR":
            print(f"failed detect temperature of {block_device}({title}): {value}")
            continue

        if value in ["NA", "UNK", "NOS"]:
            # print(f"device module did not support {block_device}({title}): {value}")
            continue

        try:
            v = int(value)
        except:
            print(f"device module did not support {block_device}({title}): {value}")
            continue

        tmp = StaticTemp(
            index=line_num,
            name=basename(block_device),
            device="SATA",
            degree=v,
        )
        temps.append(tmp)

    return temps


def _read():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 7634))
        return _recv(sock)
    except ConnectionRefusedError as e:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.connect(("localhost", 7634))
        return _recv(sock)


def _recv(sock: socket.socket):
    text = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            # Unreliable
            break
        else:
            text += chunk

    return text.decode("utf-8", "ignore")
