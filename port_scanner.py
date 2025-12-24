import socket
import threading
import sys
from queue import Queue
import re

def scan(q,ip):
    while True:
        try:
            port = q.get_nowait()
        except:
            break
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(1)  # may be bad connection + 0.3s will not trigger a port. feel free to make 0.5-1s
        result = sock.connect_ex((ip,port))
        if result == 0:
            print(f"port {port} is open")
        q.task_done()

def main():
    if len(sys.argv) < 4:
        print(f"Usage python3 file_path <ip> <start_port> <end_port>")
    else:
        try:
            ip = sys.argv[1]
            pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            match = re.match(pattern,ip)
            if not match:
                raise ValueError("IP address should be in x.x.x.x form")
            start = int(sys.argv[2])
            end = int(sys.argv[3])
            if start<1 or end<1:
                raise ValueError("ports must be greater than 0")
            elif start>65535 or end>65535:
                raise ValueError("ports must be lower than 65535")
            elif start>end:
                raise ValueError("start must be lower than or equal to end")
        except ValueError as e:
            print(f"Error : {e}")
            print(f"Usage python3 file_path <ip> <start_port> <end_port>")
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)

        q = Queue()
        for i in range(start,end+1): q.put(i)
        threads = []
        for i in range(100):
            t = threading.Thread(target=scan,args=(q,ip))
            t.start()
            threads.append(t)
        for thread in threads: thread.join()
        print("Scan is completed")
    

if __name__ == '__main__':
    main()
