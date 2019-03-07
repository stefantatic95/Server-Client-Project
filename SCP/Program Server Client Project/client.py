import socket
import tkinter
from tkinter import font
from tkinter import *
import re
import matplotlib.pyplot as plt
import datetime

#glavni tkinter
root=Tk()
font=font.Font(root,family='Verdana',size=12)
root.title("Server Client Project: Client")
rtframe=Frame(root,bg='white smoke')
rmframe=Frame(root,bg='white smoke')
rtframe.pack(side=TOP,fill=X)
rmframe.pack(side=TOP,fill=X)
rbframe=Frame(root,bg='white smoke')
rbframe.pack(side=BOTTOM,fill=X)

#server tkinter
top=Tk()
top.title('Server Client Project: Server')
textop=Text(top,bg='white',fg='blue',font=font)
textop.insert(INSERT, 'Čekam...\n')

#poruke od servera
serverporuke=Tk()
serverporuke.title('Poruke od servera')

#widgeti
label1=Label(rtframe,text='Ime:',bg='white smoke',fg='blue',font=font)
label2=Label(rbframe, text='Lista registrovanih korisnika', bg='white smoke',fg='blue',font=font)

textime=StringVar()
E1=Entry(rtframe,textvariable=textime,bg='white',fg='blue',font=font)

msg=StringVar()
E2=Entry(rbframe,textvariable=msg,width=100,bg='white',fg='blue',font=font)

Lb1 = Listbox(rbframe, selectmode=SINGLE,bg='white',fg='blue',font=font,cursor='hand1',selectbackground='blue')
registrovani=[]

varb = StringVar()
R1 = Radiobutton(rbframe,text='Vreme', variable=varb, value='vreme',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')
R2 = Radiobutton(rbframe,text='Poruka', variable=varb, value='poruka',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')
R3 = Radiobutton(rbframe,text='Mojbox', variable=varb, value='mailbox',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')
R4 = Radiobutton(rmframe,text='Registruj se', variable=varb, value='register',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')
R5 = Radiobutton(rbframe,text='Updejtuj listu registrovanih', variable=varb, value='update',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')
R6 = Radiobutton(rmframe,text='Bioritam(DD\MM\GGGG)', variable=varb, value='bioritam',bg='white smoke',fg='blue',tristatevalue='x',font=('Verdana','14','bold'),cursor='target',activebackground='blue',activeforeground='white')

dan=StringVar()
Edan=Entry(rmframe,textvariable=dan,bg='white',fg='blue',font=font,width=3)

mesec=StringVar()
Emesec=Entry(rmframe,textvariable=mesec,bg='white',fg='blue',font=font,width=3)

godina=StringVar()
Egodina=Entry(rmframe,textvariable=godina,bg='white',fg='blue',font=font,width=5)

onoff=IntVar()
C1=Checkbutton(rbframe,bg='white smoke',fg='blue',text='Dodaj smajli',variable=onoff,onvalue=1,offvalue=0,font=font,cursor='dotbox',activebackground='blue',activeforeground='white')

text = Text(serverporuke,bg='white',fg='blue',font=font)

def send(event):
    textic=re.sub(':','',textime.get())

    if varb.get()=='poruka':
        if onoff.get()==0:
            s = socket.socket()
            s.connect(('localhost', 12345))
            newmsg = re.sub(':', '', msg.get())
            porukat = textic,':',varb.get(),':',str(Lb1.get(ACTIVE)),':',newmsg
            porukas=''.join(porukat)
            s.send(porukas.encode())
            textop.insert(INSERT, porukas + '\n')
            textop.insert(INSERT, 'Čekam...\n')
            uspesno = s.recv(1024).decode()
            text.insert(INSERT, uspesno + '\n')
            s.close()

        elif onoff.get()==1:
            s = socket.socket()
            s.connect(('localhost', 12345))
            newmsg = re.sub(':', '', msg.get())
            porukat = textic, ':', varb.get(), ":", str(Lb1.get(ACTIVE)), ':( ° ͜ʖ °)',' ',newmsg
            porukas = ''.join(porukat)
            s.send(porukas.encode())
            textop.insert(INSERT, porukas + '\n')
            textop.insert(INSERT, 'Čekam...\n')
            uspesno = s.recv(1024).decode()
            text.insert(INSERT, uspesno + '\n')
            s.close()

    elif varb.get()=='update':
        s = socket.socket()
        s.connect(('localhost', 12345))
        porukat = textic, ':', varb.get()
        porukas = ''.join(porukat)
        s.send(porukas.encode())
        textop.insert(INSERT, porukas + '\n')
        textop.insert(INSERT, 'Čekam...\n')
        updateporuka = s.recv(1024).decode()
        s.close
        updatelista=[]
        updatelista = re.sub('[^\w]', ' ', updateporuka).split()
        i=0

        for x in updatelista:
            if (x in registrovani)==False:
                registrovani.append(x)
                Lb1.insert(i, x)
                i + 1

    elif varb.get() == 'bioritam':
        plt.close()
        try:
            birthdaycheck = datetime.date(int(godina.get()), int(mesec.get()), int(dan.get()))
        except ValueError:
            text.insert(INSERT, 'Uneli ste pogrešnu vrednost za datum. Unesite odogvarajuće vrednosti za datum' + '\n')

        else:
            birthporuka = godina.get(), '-', mesec.get(), '-', dan.get()
            birthdayfinal = ''.join(birthporuka)
            s = socket.socket()
            s.connect(('localhost', 12345))
            porukat = textic, ':', varb.get(), ':', birthdayfinal
            porukas = ''.join(porukat)
            s.send(porukas.encode())
            textop.insert(INSERT, porukas + '\n')
            textop.insert(INSERT, 'Čekam...\n')
            serverporuka = s.recv(1024).decode()
            s.close()

            phy, inte, emo = serverporuka.split(':')
            yphyper = re.sub(',', ' ', phy).split()
            yintper = re.sub(',', ' ', inte).split()
            yemoper = re.sub(',', ' ', emo).split()

            for x in range(0, len(yphyper)):
                yphyper[x] = int(yphyper[x])

            for x in range(0, len(yintper)):
                yintper[x] = int(yintper[x])

            for x in range(0, len(yemoper)):
                yemoper[x] = int(yemoper[x])

            xdani = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

            plt.figure('Bioritam')
            plt.title('Bioriam za narednih 10 dana\nUnesen dan rođenja: ' + dan.get() + '/' + mesec.get() + '/' + godina.get())
            plt.plot(xdani, yphyper, color='green', label='Fizički bioritam')
            plt.plot(xdani, yintper, color='blue', label='Intelektualni bioritam')
            plt.plot(xdani, yemoper, color='red', label='Emocionalni bioritam')
            plt.xlabel('Dani')
            plt.ylabel(('Vrednosti u %\nMax: 100%,min: -100%'))
            plt.legend()
            plt.show()


    else:
        s = socket.socket()
        s.connect(('localhost', 12345))
        porukat = textic, ':', varb.get()
        porukas = ''.join(porukat)
        s.send(porukas.encode())
        textop.insert(INSERT, porukas + '\n')
        textop.insert(INSERT, 'Čekam...\n')
        serverporuka = s.recv(1024).decode()
        text.insert(INSERT, serverporuka+'\n')
        s.close()

B = tkinter.Button(rbframe, text ='ŠALJI',bg='blue',fg='white',font=('Verdana','20','bold'),cursor='hand1',activebackground='blue',activeforeground='white')
B.bind("<Button-1>",send)

#slike/menu
photo=PhotoImage(file='sc.gif')
photo2 = PhotoImage(file='redpanda.gif')
photo3 = PhotoImage(file='traumatic.gif')
picture=Label(rtframe, image=photo,bg='blue')

def classic():
    rtframe.configure(bg='white smoke')
    rmframe.configure(bg='white smoke')
    rbframe.configure(bg='white smoke')
    B.configure(bg='blue',fg='white',activebackground='blue',activeforeground='white')
    label1.configure(bg='white smoke',fg='blue')
    label2.configure(bg='white smoke', fg='blue')
    C1.configure(bg='white smoke',fg='blue',activebackground='blue',activeforeground='white')
    R1.configure(bg='white smoke',fg='blue',activebackground='blue',activeforeground='white')
    R2.configure(bg='white smoke', fg='blue',activebackground='blue',activeforeground='white')
    R3.configure(bg='white smoke', fg='blue',activebackground='blue',activeforeground='white')
    R4.configure(bg='white smoke', fg='blue',activebackground='blue',activeforeground='white')
    R5.configure(bg='white smoke', fg='blue',activebackground='blue',activeforeground='white')
    R6.configure(bg='white smoke', fg='blue', activebackground='blue', activeforeground='white')
    Egodina.configure(bg='white', fg='blue')
    Emesec.configure(bg='white', fg='blue')
    Edan.configure(bg='white', fg='blue')
    E1.configure(bg='white',fg='blue')
    E2.configure(bg='white',fg='blue')
    text.configure(bg='white',fg='blue')
    textop.configure(bg='white', fg='blue')
    Lb1.configure(bg='white',fg='blue',selectbackground='blue')
    picture.configure(image=photo,bg='blue')

def redpanda():
    rtframe.configure(bg='#FF8033')
    rmframe.configure(bg='#FF8033')
    rbframe.configure(bg='#FF8033')
    B.configure(bg='#662B00', fg='#FF8033',activebackground='#662B00',activeforeground='#FF8033')
    label1.configure(bg='#FF8033', fg='#662B00')
    label2.configure(bg='#FF8033', fg='#662B00')
    C1.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R1.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R2.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R3.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R4.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R5.configure(bg='#FF8033', fg='#662B00',activebackground='#662B00',activeforeground='#FF8033')
    R6.configure(bg='#FF8033', fg='#662B00', activebackground='#662B00', activeforeground='#FF8033')
    Egodina.configure(bg='white', fg='#662B00')
    Emesec.configure(bg='white', fg='#662B00')
    Edan.configure(bg='white', fg='#662B00')
    E1.configure(bg='white',fg='#662B00')
    E2.configure(bg='white',fg='#662B00')
    text.configure(bg='#FF8033',fg='#662B00')
    textop.configure(bg='#FF8033', fg='#662B00')
    Lb1.configure(bg='white',fg='#662B00',selectbackground='#662B00')
    picture.configure(image=photo2,bg='#662B00')

def traumatic():
    rtframe.configure(bg='#050100')
    rmframe.configure(bg='#050100')
    rbframe.configure(bg='#050100')
    B.configure(bg='#D62C2C', fg='#050100',activebackground='#D62C2C',activeforeground='#050100')
    label1.configure(bg='#050100', fg='#D62C2C')
    label2.configure(bg='#050100', fg='#D62C2C')
    C1.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R1.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R2.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R3.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R4.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R5.configure(bg='#050100', fg='#D62C2C',activebackground='#D62C2C',activeforeground='#050100')
    R6.configure(bg='#050100', fg='#D62C2C', activebackground='#D62C2C', activeforeground='#050100')
    Egodina.configure(bg='white', fg='#D62C2C')
    Emesec.configure(bg='white', fg='#D62C2C')
    Edan.configure(bg='white', fg='#D62C2C')
    E1.configure(bg='white', fg='#D62C2C')
    E2.configure(bg='white', fg='#D62C2C')
    text.configure(bg='#050100', fg='#D62C2C')
    textop.configure(bg='#050100', fg='#D62C2C')
    Lb1.configure(bg='white', fg='#D62C2C',selectbackground='#D62C2C')
    picture.configure(image=photo3,bg='#D62C2C')

menubar=Menu(root)
thememenu=Menu(menubar)
menubar.add_cascade(label='Theme', menu=thememenu)
thememenu.add_command(label='Classic', command=classic)
thememenu.add_command(label='Red panda', command=redpanda)
thememenu.add_command(label='Traumatic', command=traumatic)
root.config(menu=menubar)

#pozicije roota
picture.pack()
label1.pack(side=LEFT,anchor=W)
E1.pack(side=LEFT,anchor=W)
R4.pack(anchor=W)
R1.pack(anchor=W)
R6.pack(side=LEFT,anchor=W)
Edan.pack(side=LEFT,anchor=W)
Emesec.pack(side=LEFT,anchor=W)
Egodina.pack(side=LEFT,anchor=W)
R2.pack(anchor=W)
E2.pack(anchor=W)
C1.pack(anchor=W)
label2.pack(anchor=E)
Lb1.pack(anchor=E)
R5.pack(anchor=W)
R3.pack(anchor=W)
B.pack()
text.pack()

#pozicije topa
textop.pack()

serverporuke.mainloop()
root.mainloop()
top.mainloop()