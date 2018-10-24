import socket
import json
import pickle


def saveToJson():
    save = json.dumps(taskDict)
    with open('TaskList.json', 'w') as file:
        file.write(save)
    file.close()


def loadFromJson():
    f = open('TaskList.json', 'r')
    load = f.read()
    load = json.loads(load)
    f.close()
    return load


print('Uruchomiono serwer ')
taskDict = loadFromJson()
nextID = int(taskDict['NextID'])
host = ''
port = 8888
size = 1024
backlog = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(backlog)

client, address = s.accept()
print('Połączono z : ' + str(address))
while True:
    received = client.recv(size)
    if not received:
        break
    received = received.decode()
    if received == '1':
        task = client.recv(size)
        task = pickle.loads(task)
        task.id = nextID
        taskDict[task.priority].append([task.id, task.desc])
        nextID = nextID + 1
        taskDict['NextID'] = nextID
        client.send(str.encode('Dodano nowe zadanie'))
        saveToJson()
    elif received == '2':
        priority = client.recv(size)
        priority = priority.decode()
        tasks = str(taskDict[priority])
        client.send(str.encode(tasks))
    elif received == '3':
        usun = client.recv(size)
        usun = int(usun.decode())
        taskDict['High'] = [i for i in taskDict['High'] if i[0] != int(usun)]
        taskDict['Normal'] = [i for i in taskDict['Normal'] if i[0] != int(usun)]
        taskDict['Low'] = [i for i in taskDict['Low'] if i[0] != int(usun)]
        saveToJson()
        client.send(str.encode('Zakończono'))
    elif received == '4':
        stringList = []
        for data in taskDict["High"]:
            stringList.append("id: " + str(data[0]) + " opis: " +
                data[1] + " priorytet: High")
        for data in taskDict["Normal"]:
            stringList.append("id: " + str(data[0]) + " opis: " +
                data[1] + " priorytet: Normal")
        for data in taskDict["Low"]:
            stringList.append("id: " + str(data[0]) + " opis: " +
                data[1] + " priorytet: Low")
        client.send(pickle.dumps(stringList))
print("Wylaczono serwer")
client.close()
