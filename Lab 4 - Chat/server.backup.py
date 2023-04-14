import sys
import socket
import threading

class thread1 (threading.Thread):
  global s, con
  def __init__(self, threadID, name, counter):
    threading.Thread.__init__(self)
    self.threadlD = threadID
    self.name = name
    self.counter = counter
  def run(self):
    msgRecv(s,con)

class thread2 (threading.Thread):
  global s, con
  def __init__(self, threadID, name, counter):
    threading.Thread.__init__(self)
    self.threadlD = threadID
    self.name = name
    self.counter = counter
  def run(self):
    msgSend(s,con)

def msgRecv(s, con):
  while (1):
    data = con.recv(50)
    print(data)
    if (data == 'quit'):
      con.close()
      exit(1)

def msgSend(s, con):
  global name
  while(1):
    print(name)
    string = input()
    msg = name + ", " + string
    con.send(msg)
    if (string == 'quit'):
      con.close()
      exit(1)

IP = 'localhost'
PORT = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(10)
name = input("Enter name: ")
name = "@"+name+">"
print(name, " waiting...")

con, ad = s.accept()

thread1 = thread1(1, 'Thread-1', 1)
thread2 = thread2(2, 'Thread-2', 2)

thread1.start()
thread2.start()