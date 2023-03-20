import socket, threading as t, json

DNS_PORT = 3000
ADD_PORT = 3001
SUB_PORT = 3002
MUL_PORT = 3003
DIV_PORT = 3004
IP = '127.0.0.1'
connections_threads = []

def handle_addition(PORT):
  s = socket.socket()
  s.bind((IP, PORT))
  s.listen(5)
  print(f"PORT: {PORT} >> Addition Handler")
  while True:
    c, _ = s.accept()
    request = c.recv(1024).decode()
    data = json.loads(request)
    a = int(data.get("operand_A"))
    b = int(data.get("operand_B"))
    c.send(f"{a+b}".encode())
    c.close()

def handle_subtraction(PORT):
  s = socket.socket()
  s.bind((IP, PORT))
  s.listen(5)
  print(f"PORT: {PORT} >> Subtraction Handler")
  while True:
    c, _ = s.accept()
    request = c.recv(1024).decode()
    data = json.loads(request)
    a = int(data.get("operand_A"))
    b = int(data.get("operand_B"))
    c.send(f"{a-b}".encode())
    c.close()

def handle_multiplication(PORT):
  s = socket.socket()
  s.bind((IP, PORT))
  s.listen(5)
  print(f"PORT: {PORT} >> Multiplication Handler")
  while True:
    c, _ = s.accept()
    request = c.recv(1024).decode()
    data = json.loads(request)
    a = int(data.get("operand_A"))
    b = int(data.get("operand_B"))
    c.send(f"{a*b}".encode())
    c.close()

def handle_division(PORT):
  s = socket.socket()
  s.bind((IP, PORT))
  s.listen(5)
  print(f"PORT: {PORT} >> Division Handler")
  while True:
    c, _ = s.accept()
    request = c.recv(1024).decode()
    data = json.loads(request)
    a = int(data.get("operand_A"))
    b = int(data.get("operand_B"))
    if (b == 0):
      c.send("inf".encode())
    else:
      c.send(f"{float(float(a)/float(b))}".encode())
    c.close()

def dns_server(c, address):
  print('[!] Connection request from:', address)
  connected = True
  while connected:
    client_request = c.recv(1024)
    if (client_request.decode() == 'D'):
      connected = False
      c.send("[200] Disconnected".encode())
      print(f"[Active connections] : {t.active_count()-6}")
      c.close()
    else:
      data = json.loads(client_request.decode())
      print(address, data)
      operator = str(data.get("operator"))
      b = int(data.get("operand_B"))
      if (operator == '/' and b == 0):
        evaluated = "inf"
      else:
        s = socket.socket()
        if (operator == '+'):
          s.connect((IP, ADD_PORT))
          s.send(client_request)
          evaluated = s.recv(1024).decode()
        elif (operator == '-'):
          s.connect((IP, SUB_PORT))
          s.send(client_request)
          evaluated = s.recv(1024).decode()
        elif (operator == '*'):
          s.connect((IP, MUL_PORT))
          s.send(client_request)
          evaluated = s.recv(1024).decode()
        elif (operator == '/'):
          s.connect((IP, DIV_PORT))
          s.send(client_request)
          evaluated = s.recv(1024).decode()
      c.send(f"{evaluated}".encode())

def start_subserver_threads():
  subservers = []
  addition_subserver = t.Thread(target=handle_addition, args=[ADD_PORT])
  subtraction_subserver = t.Thread(target=handle_subtraction, args=[SUB_PORT])
  multiplication_subserver = t.Thread(target=handle_multiplication, args=[MUL_PORT])
  division_subserver = t.Thread(target=handle_division, args=[DIV_PORT])
  addition_subserver.start()
  subservers.append(addition_subserver)
  subtraction_subserver.start()
  subservers.append(subtraction_subserver)
  multiplication_subserver.start()
  subservers.append(multiplication_subserver)
  division_subserver.start()
  subservers.append(division_subserver)

def main():
  s = socket.socket()
  s.bind((IP, DNS_PORT))
  s.listen(5)
  print(f"PORT: {DNS_PORT} >> [DNS Server]")
  start_subserver_threads()
  while True:
    c, address = s.accept()
    thread = t.Thread(target=dns_server, args=[c, address])
    thread.start()
    connections_threads.append(thread)
    print(f"[Active connections] : {t.active_count()-5}")

if __name__ == '__main__':
  main()