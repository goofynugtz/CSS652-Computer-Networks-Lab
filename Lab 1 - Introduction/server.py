import socket

PORT = 3000
IP = '127.0.0.1'

s = socket.socket()
s.bind((IP, PORT))
print("Socket created and bound to PORT: %s" %(PORT))
s.listen(5)

while True:
  c, address = s.accept()
  print('[!] Connection request from:', address)
  print(c.recv(1024).decode())
  c.send('>> Server sends acknowledgement.\n'.encode())
  c.close()