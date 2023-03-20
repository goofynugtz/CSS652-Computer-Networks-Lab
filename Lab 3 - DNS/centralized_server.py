import socket, threading, json

PORT = 3000
IP = '127.0.0.1'

s = socket.socket()
s.bind((IP, PORT))
s.listen(5)
print(f">> Server listeing @ PORT: {PORT}")

server_threads = []

def evaluate_expression(c, address):
  print('[!] Connection request from:', address)
  connected = True
  while connected:
    client_request = c.recv(1024)
    data = json.loads(client_request.decode())
    print(address, data)
    a = int(data.get("operand_A"))
    operator = str(data.get("operator"))
    b = int(data.get("operand_B"))
    if (operator == '/' and b == 0):
      evaluated = "inf"
    else:
      if (operator == str('+')):
        evaluated = a + b
      elif (operator == '-'):
        evaluated = a - b
      elif (operator == '*'):
        evaluated = a * b
      elif (operator == '/'):
        evaluated = float(float(a)/float(b))
    c.send(f"{evaluated}".encode())


while True:
  c, address = s.accept()
  thread = threading.Thread(target=evaluate_expression, args=[c,address])
  thread.start()
  server_threads.append(thread)
  print(f"[Active connections] : {threading.active_count()-1}")