import socket
import threading
import time

PORT = 3000
IP = '127.0.0.1'

def connect_to():
  s = socket.socket()
  s.connect((IP, PORT))
  s.send(">> Client sends request.\n".encode())
  print(s.recv(1024).decode())
  s.close()

def main():
  start = time.perf_counter()
  clients = []
  for i in range(5):
    client = threading.Thread(target=connect_to)
    client.start()
    clients.append(client)
  for thread in clients:
    thread.join()
  finish = time.perf_counter()
  print(f'\n\nFinished in {round(finish-start, 2)} second(s)\n')

if __name__ == '__main__':
  main()