import socket
from _thread import *
from queue import Queue

HOST = ''
PORT = 64732
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID):
    client.setblocking(1)
    msg = ""
    while True:
        msg += client.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverChannel.put(str(cID) + "_" + readyMsg)
            command = msg.split("\n")


def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
#    print("msg recv: ", msg)
    senderID, msg = int(msg.split("_")[0]), "_".join(msg.split("_")[1:])
    msg2 = serverChannel.get(True, None)
    senderID2, msg2 = int(msg2.split("_")[0]), "_".join(msg2.split("_")[1:])        
    if (msg):
        if msg2 and senderID != senderID2:
            for cID in range(len(clientele)):
                sendMsg = "playerMoved " +  str(senderID) + " " + msg + " " + str(senderID2) + " "+ msg2 + "\n"
                clientele[cID].send(sendMsg.encode())
        else:
            for cID in range(len(clientele)):
                sendMsg = "playerMoved " +  str(senderID) + " " + msg + "\n"
                clientele[cID].send(sendMsg.encode())
    serverChannel.task_done()

clientele = []
currID = 0

serverChannel = Queue(1)
start_new_thread(serverThread, (clientele, serverChannel))

while True:
    if len(clientele) < 2:
        client, address = server.accept()
        print(currID)
        clientele.append(client)
        for cID in range(len(clientele)):
            print(repr(cID), repr(currID))
            if cID == 0:
                if cID == currID:
                    clientele[cID].send(("newPlayer %d %d\n" % (currID, currID)).encode())
                else:
                    clientele[cID].send(("newPlayer %d\n" % currID).encode())
            else:
                clientele[cID].send(("newPlayer %d\n" % (0)).encode())
                clientele[cID].send(("newPlayer %d %d\n" % (currID, currID)).encode())
        print("connection recieved")
        start_new_thread(handleClient, (client,serverChannel, currID))
        currID += 1


