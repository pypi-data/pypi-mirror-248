import socket
import threading
from queue import Queue
from typing import List


def scan(target: str, start=0, stop=1023, threads=500) -> List[int]:
    def port_scan(target: str, port: int) -> bool:
        try:
            # IPV4, TCP
            sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sckt.connect((target, port))
            return True
        except:
            return False

    def populate_queue(queue: Queue, port_list: List[int]) -> None:
        for port in port_list:
            queue.put(port)

    def evaluate_next_port(queue: Queue, open_ports: List[int], target: str) -> None:
        while not queue.empty():
            port = queue.get()
            if port_scan(target, port):
                open_ports.append(port)

    port_list = range(start, stop + 1)
    port_queue = Queue()
    open_ports = []
    populate_queue(port_queue, port_list)

    thread_list = []
    for i in range(threads):
        thread = threading.Thread(target=evaluate_next_port, args=(port_queue, open_ports, target))
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    return open_ports

