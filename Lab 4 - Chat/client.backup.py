import socket,threading
class myThread1(threading.Thread):
  global s
  def __init__(self,threadID,name,counter):
    threading.Thread.__init__(self)
    self.threaaID=threadID
    self.name=name
    self.counter=counter
  def run(self):
    ReceiveMsg(s)
class myThread2(threading.Thread):
  global s
  def __init__(self,threadID,name,counter):
    threading.Thread.__init__(self)
    self.threaaID=threadID
    self.name=name
    self.counter=counter
  def run(self):
    SendMsg(s)

def SendMsg(s):
  while True:
    msg=input()
    msg="Client ->"+msg
    if(msg=="END"):
        break
    s.send(msg.encode())

def ReceiveMsg(s):
  while True:
    msg=s.recv(100)
    msg=msg.decode()
    print(msg)
host='127.0.0.1'
port=7000
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
thread1=myThread1(1,"T1",1)
thread2=myThread2(2,"T2",2)
thread1.start()
thread2.start()
