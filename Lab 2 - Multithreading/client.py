import socket
import threading
import time

PORT = 3000
IP = '127.0.0.1'

def connect_to():
  s = socket.socket()    
  s.connect((IP, PORT))
  connected = True
  while connected:
    user_input = input()
    start = time.perf_counter()
    s.send(user_input.encode())
    server_response = s.recv(1024).decode()
    print(server_response)
    finish = time.perf_counter()
    print(f'>> Time taken: {round(finish-start, 3)} second(s)\n')
    if (user_input == "DISCONNECT"):
      s.close()
      break;

def main():
  start = time.perf_counter()
  list_of_threads = []
  for i in range(4):
    new_thread = threading.Thread(target=connect_to)
    new_thread.start()
    list_of_threads.append(new_thread)
  for thread in list_of_threads:
    thread.join()
  finish = time.perf_counter()
  print(f'Finished in {round(finish-start, 3)} second(s)\n')

if __name__ == '__main__':
  main()