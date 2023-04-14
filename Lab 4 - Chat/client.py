import socket as s, threading as t

PORT = 3000
HOST_IP = '127.0.0.1'

class client(t.Thread):
  def __init__(self, host_ip=HOST_IP, port=PORT) -> None:
    t.Thread.__init__(self)
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.server_socket.connect((host_ip, port))
    self.connected = True
    while self.connected:
      user_input = input()
      self.server_socket.send(user_input.encode())
      server_response = self.server_socket.recv(1024).decode()
      print(server_response)
      if (user_input == "DISCONNECT"):
        self.server_socket.close()
        self.connected = False
        break;

def run(count=5):
  clients = []
  for i in range(count):
    c = client(HOST_IP, PORT)
    c.start()
    clients.append(c)

  for thread in clients:
    thread.join()

if __name__ == '__main__':
  run(6)