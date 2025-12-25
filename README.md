# Port Scanner

A TCP port scanner written in Python using sockets, threading, and multiprocessing.

This project is built as a learning exercise to understand how port scanners work internally,
including concurrency, timeouts, and task distribution.

---

## Features

- TCP connect-based port scanning
- Multi-threaded scanning using a queue
- Optional multi-process scanning
- Custom timeout control
- Scan specific ports or port ranges
- Basic command-line flag handling

---

## How it works

- Ports are added to a queue
- Worker threads take ports from the queue and attempt TCP connections
- Optionally, multiple processes are used to split the port range
- Open ports are printed when a connection succeeds

---

## Usage

> ⚠️ Scan only systems you own or have permission to test.

python scanner.py <ip> [options]
