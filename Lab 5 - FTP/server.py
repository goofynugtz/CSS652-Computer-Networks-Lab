import socket as s, threading
import os

PORT = 3000
HOST_IP = '127.0.0.1'
BATCH_SIZE = 10

class server:
  def __init__(self, host_ip=HOST_IP, port=PORT):
    self.host_ip = host_ip
    self.port = port
    self.server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.server_socket.bind((self.host_ip, self.port))
    self.server_socket.listen(5)
    self.connections = []
    print(f">> Server listeing @ PORT: {self.port}")

  def handle_client(self, c, address):
    print('[!] Connection request from:', address)
    connected = True
    while connected:
      server_query = "Enter Operation:\n1. Upload\n2. Download\n"
      c.send(server_query.encode())
      client_response = c.recv(1024).decode("utf-8")

      if (client_response == '1'):
        self.client_upload(c)
      if (client_response == '2'):
        self.client_download(c)


  def client_upload(self, c):
    server_index = open(os.getcwd()+"\\server_storage\\index.txt", "a+")
    c.send("Enter filename: ".encode())
    filename = c.recv(1024).decode("utf-8")
    saved_file = open(os.getcwd()+"\\server_storage\\"+filename, "wb")
    file_size = c.recv(1024).decode()
    print("File size:", file_size)
    _size_counter = int(file_size)
    
    data = c.recv(BATCH_SIZE)
    while (_size_counter > 0):
      saved_file.write(data)
      data = c.recv(BATCH_SIZE)
      _size_counter -= BATCH_SIZE
      if (data == b'<EOF>' or _size_counter < 0):
        break
    saved_file.close()
    server_index.write(filename)
    server_index.close()
    print("[Success] File uploaded from client.")


  def client_download(self, c):
    with open(os.getcwd()+"\\server_storage\\index.txt", 'r') as server_index:
      index_file = server_index.read()
      c.send(index_file.encode())
    filename = c.recv(1024).decode("utf-8") # Recieving file name
    selected_file = open(os.getcwd()+"\\server_storage\\"+filename, "rb")
    file_size = str(len(selected_file.read()))
    print("File size:", file_size)
    c.send(file_size.encode()) # Sending file size
    selected_file.close()
    _size_counter = int(file_size)
    
    selected_file = open(os.getcwd()+"\\server_storage\\"+filename, "rb")
    buffer = selected_file.read(1024)
    while (_size_counter > 0):
      c.send(buffer)
      print(_size_counter, buffer)
      buffer = selected_file.read(1024)
      _size_counter -= 1024
    c.send("<EOF>".encode())
    selected_file.close()
    print("[Success] File downloaded to client.")


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
