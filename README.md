# Port Scanner

A simple multi-threaded TCP port scanner written in Python.

This project is built to understand how port scanning works internally,
using sockets, threads, and queues — not to rely on existing tools.

---

## What this scanner does

- Scans a range of TCP ports on a target IP
- Uses `connect()` (TCP connect scan)
- Uses multiple threads for faster scanning
- Uses a queue to distribute ports safely between threads
- You can make it more faster changing sock.settimeout(1) to 0.3-0.5. but less accurate

---

## How it works (brief)

- Ports are added to a queue
- Multiple worker threads take ports from the queue
- Each thread tries to connect to a port using a TCP socket
- If the connection succeeds, the port is marked as open

---

## Usage

> ⚠️ Scan only systems you own or have permission to test.

python <file_path> <ip_addr> <start_port> <end_port>
