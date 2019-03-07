import socket
import time
import datetime
import re
import math

s=socket.socket()
s.bind(('0.0.0.0',12345))
s.listen(5)
porukad={}
posiljalac={}
registered=[]

while True:
    print('Čekam...')
    c, addr = s.accept()
    print('Nova naredba od adrese: ',addr)
    poruka = c.recv(1024).decode()
    print(poruka)
    count = 0
    for x in poruka:
        if x == ':':
            count += 1
    if count == 1:
        name, order = poruka.split(':')

        if order == 'vreme':
            vreme = time.ctime(time.time())
            vremeporuka = 'Trenutrno vreme je: ', vreme, ', korisniče: ', name
            vp = ''.join(vremeporuka)
            c.sendall(vp.encode())

        elif order == 'mailbox':
            if porukad.get(name) == None:
                nope = 'Nema nove poruke.'
                c.sendall(nope.encode())
            else:
                jeste ='Nova poruka od: ',  posiljalac[name], ' glasi: ', porukad[name]
                jest = ''.join(jeste)
                c.sendall(jest.encode())

        elif order == 'register':
            if name=='':
                loseime='Molim Vas da unesete ime pre nego što se registrujete.'
                c.sendall(loseime.encode())
            if (name in registered)==True:
                imaga='Korisnik: ',name,' je već registrovan.'
                imagaporuka=''.join(imaga)
                c.sendall(imagaporuka.encode())
            else:
                registered.append(name)
                print(registered)
                msgreg = 'Korisnik: ', name, ' je uspešno registrovan.'
                mr = ''.join(msgreg)
                c.sendall(mr.encode())

        elif order == 'update':
            upmsg=''

            for x in registered:
                upmsg += x + ","

            updatemsg=''.join(upmsg)
            c.sendall(updatemsg.encode())

    elif count ==2:
        name,order,datum=poruka.split(':')
        godina,mesec,dan=datum.split('-')
        birthday = datetime.date(int(godina), int(mesec), int(dan))
        today=datetime.date.today()
        yphyper = []
        yintper = []
        yemoper = []

        for i in range(0,10):
            t = (today - birthday).days
            phy = 100 * (math.sin(2 * math.pi * t / 23))
            inte = 100 * (math.sin(2 * math.pi * t / 33))
            emo = 100 * (math.sin(2 * math.pi * t / 28))
            yphyper.append(int(phy))
            yintper.append(int(inte))
            yemoper.append(int(emo))
            today += datetime.timedelta(days=1)

        phyporuka=''
        inteporuka=''
        emoporuka=''

        for x in yphyper:
            phyporuka+=str(x)+','

        for x in yintper:
            inteporuka+=str(x)+','

        for x in yemoper:
            emoporuka+=str(x)+','

        fporuka=phyporuka,':',inteporuka,':',emoporuka
        msgporuka=''.join(fporuka)
        c.sendall(msgporuka.encode())

    elif count == 3:
        key, value, key2, value2 = poruka.split(':')
        dict2 = {key2: value2}
        dict3={key2:key}
        porukad.update(dict2)
        posiljalac.update(dict3)
        print('Nova poruka za:  ', key2, ' je dodata i ona glasi: ', porukad[key2])
        uspesno='Korisniče ', key, ', vaša poruka je uspešno poslata.'
        uspesnomsg=''.join(uspesno)
        c.sendall(uspesnomsg.encode())