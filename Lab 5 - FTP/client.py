import socket as s
import os 

PORT = 3000
HOST_IP = '127.0.0.1'
BATCH_SIZE = 10

class client:
  def __init__(self, host_ip=HOST_IP, port=PORT):
    self.host_ip = host_ip
    self.port = port
    self.client_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    self.client_socket.connect((self.host_ip, self.port))
    self.connected = True
    while self.connected:
      server_query = self.client_socket.recv(1024).decode()
      print(server_query)
      client_input = str(input())
      self.client_socket.send(client_input.encode())

      # Upload
      if (client_input == "1"):
        print("Enter filename: ", end="")
        file_input = input()
        self.client_socket.send(file_input.encode())
        selected_file = open(os.getcwd()+"\\client_storage\\"+file_input, "rb")
        file_size = str(len(selected_file.read()))
        print(file_size)
        self.client_socket.send(file_size.encode())
        selected_file.close()
        _size_counter = int(file_size)
        selected_file = open(os.getcwd()+"\\client_storage\\"+file_input, "rb")
        buffer = selected_file.read(BATCH_SIZE)
        while (_size_counter > 0):
          self.client_socket.send(buffer)
          print(_size_counter, buffer)
          buffer = selected_file.read(BATCH_SIZE)
          _size_counter -= BATCH_SIZE
        self.client_socket.send("<EOF>".encode())
        print("[Success] File uploaded to server.")

        
      # Download
      if (client_input == "2"):
        server_index = self.client_socket.recv(1024)
        client_index = open(os.getcwd()+"\\client_storage\\index.txt", "a+")
        print(server_index)
        print("Enter filename to download:", end=" ")
        filename = str(input())
        self.client_socket.send(filename.encode())
        saved_file = open(os.getcwd()+"\\client_storage\\"+filename, "wb")
        file_size = self.client_socket.recv(1024).decode()
        print("File size:", file_size)
        _size_counter = int(file_size)

        data = self.client_socket.recv(1024)
        while (_size_counter > 0):
          saved_file.write(data)
          data = self.client_socket.recv(1024)
          _size_counter -= 1024
          print(_size_counter,data)
          if (data == b'<EOF>'):
            break
        saved_file.close()
        client_index.write(filename)
        client_index.close()
        print("[Success] File downloaded from server.")


if __name__ == "__main__":
  client = client(HOST_IP, PORT)
  client.run()