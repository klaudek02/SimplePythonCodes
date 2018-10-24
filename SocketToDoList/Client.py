import socket
import Task
import pickle

port = 8888
size = 1024
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print('Połączono z serwerem\n')
menuChoice = 0
while menuChoice != '5':
    print('========================================')
    print('1: Dodaj zadanie\n2: Pokaz zadania wg priorytetu\n'
            '3: Usun zadanie\n4: Pokaz wszystkie zadania\n5: Zamknij aplikacje')
    print('----------------')
    menuChoice = input("Wybierz: (1-5) ")
    if menuChoice == '1':
        s.send(str.encode(menuChoice))
        task = Task.Task()
        task.desc = input('Opis zadania: ')
        while 1:
            task.priority = input('Podaj priorytet (High, Normal, Low): ')
            if (task.priority == 'Low') or (task.priority == 'Normal') or (task.priority == 'High'):
                break
        s.send(pickle.dumps(task))
        received = s.recv(size)
        print(received.decode())
    elif menuChoice == '2':
        s.send(str.encode(menuChoice))
        while 1:
            priority = input('Pokaz zadania z priorytetem (High, Normal, Low): ')
            if (priority == 'Low') or (priority == 'Normal') or (priority == 'High'):
                break
        s.send(str.encode(priority))
        received = s.recv(size)
        print(received.decode())
    elif menuChoice == '3':
        s.send(str.encode(menuChoice))
        wantedID = input('Podaj ID zadania ktore chcesz usunac: ')
        s.send(str.encode(wantedID))
        received = s.recv(size)
        print(received.decode())
    elif menuChoice == '4':
        s.send(str.encode(menuChoice))
        received = s.recv(size)
        received = pickle.loads(received)
        for data in received:
            print(data)
s.close()
