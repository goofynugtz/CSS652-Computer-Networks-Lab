import socket, threading

PORT = 3000
IP = '127.0.0.1'

s = socket.socket()
s.bind((IP, PORT))
s.listen(5)
print(f">> Server listeing @ PORT: {PORT}")

server_threads = []

def handle_client(c, address):
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
      break;
    else:
      c.send("Server Acknowledgement".encode())

while True:
  c, address = s.accept()
  thread = threading.Thread(target=handle_client, args=[c,address])
  thread.start()
  server_threads.append(thread)
  print(f"[Active connections] : {threading.active_count()-1}")