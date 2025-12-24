import socket
import threading
import time
from queue import Queue

def scan(q):
    while True:
        try:
            port = q.get_nowait()
        except:
            break
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(0.3)  # may be bad connection + 0.3s will not trigger a port. feel free to make 0.5-1s
        result = sock.connect_ex(("localhost",port))
        if result == 0:
            print(f"port {port} is open")
        q.task_done()

def main():
    q = Queue()
    for i in range(1,1001): q.put(i)
    threads = []
    for i in range(100):
        t = threading.Thread(target=scan,args=(q,))
        t.start()
        threads.append(t)
    for thread in threads: thread.join()

if __name__ == '__main__':
    main()
