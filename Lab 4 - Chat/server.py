import socket as s, threading

PORT = 3000
HOST_IP = '127.0.0.1'

class server:
  def __init__(self, host_ip=HOST_IP, port=PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket()
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    print(f">> Server listeing @ PORT: {self.port}")
    self.connections = []

  def handle_client(self, c, address):
    print('[!] Connection request from:', address)
    connected = True
    while connected:
      client_request = c.recv(1024).decode("utf-8")
      print(address, ":", client_request)
      if (client_request == "DISCONNECT"):
        c.send("DISCONNECTED".encode())
        c.close()
        connected = False
        print(f"[Active connections] : {threading.active_count()-2}")
        break
      else:
        c.send("Server Acknowledgement".encode())

  def broadcast(self):
    pass

  def run(self):
    while True:
      c, address = self.server_socket.accept()
      self.connections.append(c)
      thread = threading.Thread(target=self.handle_client, args=[c,address])
      thread.start()
      print(f"[Active connections] : {threading.active_count()-1}")

if __name__ == "__main__":
  server = server(HOST_IP, PORT)
  server.run()
