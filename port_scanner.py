import socket
import threading
import sys
from queue import Queue
import re
import multiprocessing
import time
import os

def scan(q,ip,timeout):
    while True:
        try:
            port = q.get_nowait()
        except:
            break
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip,port))
        if result == 0:
            print(f"port {port} is open")
        q.task_done()
        sock.close()


def valid(num):
    if(num<1 or num>65535): return False
    return True


def take_flags(lst,ip,q):
    global s_r,e_r

    if len(sys.argv)<2:
        print("Error: py file_path.py -h for help")
        sys.exit(1)
    
    try:
        var = sys.argv[1]
        if var == '-h':
            file_path = os.path.join(os.getcwd(),'help.txt')
            try:
                with open(file_path,'r') as file:
                    print(file.read())
            except FileNotFoundError:
                print("File not found.visit : git@github.com:Kavinda-Jayathilake/Port-Scanner.git")
            finally:
                sys.exit(1)
        else:
            pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            match = re.match(pattern,var)
            if not match:
                raise ValueError("IP address should be in x.x.x.x form")
        for flg in sys.argv[2:]:
            if(flg[:2] == '-r'):
                start,end = map(int,flg[2:].split(","))
                if(valid(start) and valid(end)):
                    s_r,e_r = start,end
                else:
                    raise ValueError("Invalid port range")
            elif len(flg)>5 and flg[:5] == '-proc':
                match flg[5:]:
                    case '2': lst[2] = 3
                    case '3': lst[2] = 5
                    case '4': lst[2] = 7
                    case '5': lst[2] = 10
                    case '1': lst[2] = 1
                    case _  : raise ValueError()
            elif flg[:2] == '-p':
                temp = map(int,flg[2:].split(","))
                for prt in temp:
                    if valid(prt): q.put(prt)
                    else:
                        raise ValueError("Invalid port range")
            elif flg[:2] == '-P':
                pass
            elif len(flg)>7 and flg[:7] == '-thread':
                match flg[7:]:
                    case '2': lst[1] = 40
                    case '3': lst[1] = 60
                    case '4': lst[1] = 80
                    case '5': lst[1] = 100
                    case '1': lst[1] = 20
                    case _  : raise ValueError()
            elif(flg[:2] == '-t'):
                match flg[2:]:
                    case '1': lst[0] = 0.3
                    case '2': lst[0] = 0.5
                    case '4': lst[0] = 1.5
                    case '5': lst[0] = 2
                    case '3': lst[0] = 1
                    case _  : raise ValueError()
            else:
                raise Exception()

    except Exception:
        print("Error: py <file path> -h for help")
        sys.exit(1)


def worker(que,ip,timeout,thread_cnt):
    threads = []
    for i in range(thread_cnt):
        t = threading.Thread(target=scan,args=(que,ip,timeout))
        t.start()
        threads.append(t)
    for thread in threads: thread.join()

def manager(s_r,cnt,ip,timeout,thread_cnt):
    que = Queue()
    for i in range(s_r,s_r+cnt):
        if i <65536:
            que.put(i)
    worker(que,ip,timeout,thread_cnt)

def main():
    global q,s_r,e_r,ip
    take_flags(processing_units,ip,q)
    if not q.empty():
        worker(q,ip,processing_units[0],processing_units[1])
    else:
        work_cnt = int(((e_r+1)-s_r)/processing_units[2])+1
        procs = []
        for i in range(processing_units[2]):
            p = multiprocessing.Process(target=manager, args=(s_r,work_cnt,ip,processing_units[0],processing_units[1]))
            p.start()
            procs.append(p)
            s_r+=work_cnt
        for proc in procs: proc.join()

if __name__ == '__main__':
    processing_units = [1,20,1]
    q = Queue()
    s_r,e_r = 1,1000
    ip = 'localhost'
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Scanned for {round(end-start,2)} seconds...")
