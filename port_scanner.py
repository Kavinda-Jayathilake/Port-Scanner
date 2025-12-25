import socket
import threading
import sys
from queue import Queue
import re
import multiprocessing

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


def valid(num):
    if(num<1 or num>65535): return False
    return True


def take_flags(lst,ip,q,s_r,e_r):

    if len(sys.argv)<2:
        print("Error: py file_path.py -h for Usage")
        return
    
    try:
        var = sys.argv[1]
        pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        match = re.match(pattern,var)
        if not match:
            raise ValueError("IP address should be in x.x.x.x form")
        for flg in sys.argv[2:]:
            if(flg[:2] == '-R'):
                start,end = map(int,flg[2:].split(","))
                if(valid(start) and valid(end)):
                    s_r,e_r = start,end
                else:
                    raise ValueError("Invalid port range")
            elif(flg[:2] == '-p'):
                temp = map(int,flg[2:].split(","))
                for prt in temp:
                    if valid(prt): q.put(prt)
                    else:
                        raise ValueError("Invalid port range")
            elif(flg[:2] == "-P"):
                pass
            elif(flg[:2] == '-t'):
                match(flg[2:]):
                    case '1': lst[0] = 0.3
                    case '2': lst[0] = 0.5
                    case '4': lst[0] = 1.5
                    case '5': lst[0] = 2
                    case '3': lst[0] = 1
                    case _  : raise ValueError("Error: py file_path.py -h for Usage")
            elif(flg[:2] == '-threads'):
                match(flg[2:]):
                    case '2': lst[1] = 40
                    case '3': lst[1] = 60
                    case '4': lst[1] = 80
                    case '5': lst[1] = 100
                    case '1': lst[1] = 20
                    case _  : raise ValueError("Error: py file_path.py -h for Usage")
            elif(flg[:2] == '-proc'):
                match(flg[2:]):
                    case '2': lst[2] = 3
                    case '3': lst[2] = 5
                    case '4': lst[2] = 7
                    case '5': lst[2] = 10
                    case '1': lst[2] = 1
                    case _  : raise ValueError("Error: py file_path.py -h for Usage")

    except ValueError as e:
        print(e)
    except Exception:
        print("Error: py file_path.py -h for Usage")


def worker(que,ip,timeout,thread_cnt):
    threads = []
    for i in range(thread_cnt):
        t = threading.Thread(target=scan,args=(que,ip,timeout))
        t.start()
        threads.append(t)
    for thread in threads: thread.join()

def manager(s_r,cnt,ip,timeout,thread_cnt):
    que = Queue()
    for i in range(s_r,s_r+cnt): que.put(i)
    worker(que,ip,timeout,thread_cnt)

def main():
    processing_units = [1,20,1]
    q = Queue()
    s_r,e_r = 0,0
    ip = 'localhost'
    take_flags(processing_units,ip,q,s_r,e_r)
    if not q.empty():
        worker(q,ip,processing_units[0],processing_units[1])
    else:
        work_cnt = int((e_r-s_r)/processing_units[2])+1
        procs = []
        for i in range(processing_units[2]):
            p = multiprocessing.Process(target=manager, args=(s_r,work_cnt,ip,processing_units[0],processing_units[1]))
            p.start()
            procs.append(p)
        for proc in procs: proc.join()

    

if __name__ == '__main__':  
    main()
