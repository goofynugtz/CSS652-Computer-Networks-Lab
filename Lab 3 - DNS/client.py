import socket
import threading, time, json

PORT = 3000
IP = '127.0.0.1'

def connect_to():
  s = socket.socket()
  s.connect((IP, PORT))
  connected = True
  while connected:
    expression = str(input())
    if expression == 'D':
      s.send('D'.encode())
      print(s.recv(1024).decode())
      connected = False
      s.close()
    else:
      expression = expression.split(" ")
      data = json.dumps({"operand_A": expression[0], 
                         "operator": expression[1], 
                         "operand_B": expression[2]})
      start = time.perf_counter()
      s.send(data.encode())
      server_response = s.recv(1024).decode()
      print(server_response)
      finish = time.perf_counter()
      print(f'>> Completed in: {round(finish-start, 3)}s\n')

def main():
  start = time.perf_counter()
  list_of_threads = []
  for i in range(1):
    new_thread = threading.Thread(target=connect_to)
    new_thread.start()
    list_of_threads.append(new_thread)
  for thread in list_of_threads:
    thread.join()
  finish = time.perf_counter()
  print(f'Finished in {round(finish-start, 3)} second(s)\n')

if __name__ == '__main__':
  main()