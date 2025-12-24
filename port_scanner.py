import socket
import threading
import time

def scan(port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # ipv4 and tcp / even i don't mention default is this
    result = sock.connect_ex(('localhost',port))
    if result == 0:
        print(f"port {port} is open")

def main():
    threads = []
    for i in range(1,1001):
        while(threading.active_count()>=100):
            time.sleep(0.01)
        t = threading.Thread(target=scan,args=(i,))
        t.start()
        threads.append(t)
    for thread in threads: thread.join()

if __name__ == '__main__':
    main()