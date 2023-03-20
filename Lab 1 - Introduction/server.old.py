import socket
import threading

PORT = 3000
s = socket.socket()
print ("Socket successfully created")
s.bind(("", PORT))
print ("socket binded to %s" %(PORT))
s.listen(5)

server_threads = []

def handle_client(c, address):
  print ('Got connection from', address)
  connected = True
  while connected:
    msg = c.recv(1024).decode("utf-8")
    if (msg == "!DISCONNECT"):
      connected = False
  c.close()

while True:
  c, address = s.accept()
  thread = threading.Thread(target=handle_client, args=[c,address])
  thread.start()
  server_threads.append(thread)
  print(f"[Active connections] : {threading.active_count()-1}")