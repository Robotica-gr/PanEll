import serial
import time
import tkinter
from tkinter import *
import tkinter.messagebox as messagebox
import math
import random
import keyboard

gefyraxmin = 90
gefyraxmax = 950
gefyraymin = 300
gefyraymax = 680
realxmin = 40
realxmax = 1314
realymin = 22
realymax = 565

panell_master = Tk()
port = 3
portard = 4

arduino = serial.Serial(port=f'COM{portard}', baudrate=9600, timeout=5)
time.sleep(3)
print("Arduino Started")
if messagebox.askokcancel(message="Κανονική λειτουργία (ΟΚ) ή Λειτουργία διόρθωσης θέσεων (Cancel);"):
    leitourgia = 1
else:
    leitourgia = 2

panellcnc = serial.Serial(port=f'COM{port}', baudrate=115200, timeout=5)
panellcnc.readline()
panellcnc.readline()
panellcnc.readline()
#panellcnc.write(f"$1=255\r\n".encode())
#panellcnc.readline()
#panellcnc.readline()
connected = True
panell = Canvas(panell_master, bg='white', width=1366, height=768, highlightthickness=0)
panell_master.geometry("1366x768+0+0")
panell_master.overrideredirect(True)

fll = Label(panell, text='FLL 2023', font= ('Calibri 40'), foreground="RED", background='white')
fll.place(x=210, y=50)
rbtc = Label(panell, text='Robotica.gr', font= ('Calibri 40'), foreground="BLUE", background='white')
rbtc.place(x=890, y=50)
titlos = Label(panell, text='PanEll', font= ('Calibri 60'), foreground="green", background='white')
titlos.place(x=570, y=20)
upotitlos = Label(panell, text='Ρομπότ ελέγχου, συντήρησης και αντικατάστασης φωτοβολταϊκών panel', font= ('Calibri 24'), foreground="white", background='green')
upotitlos.place(x=200, y=150)
labelx = Label(panell, text='Θέση Χ του Robot:', font= ('Calibri 16'), foreground="black", background='white')
labelx.place(x=1050, y=630)
labely = Label(panell, text='Θέση Y του Robot:', font= ('Calibri 16'), foreground="black", background='white')
labely.place(x=1050, y=680)
labelxvalue = Label(panell, text='XXXX', font= ('Calibri 16'), foreground="black", background='white')
labelxvalue.place(x=1250, y=630)
labelyvalue = Label(panell, text='YYYY', font= ('Calibri 16'), foreground="black", background='white')
labelyvalue.place(x=1250, y=680)
chkbox_var = IntVar()
skoupa_chkbox = Checkbutton(panell, text="Καθαρισμός;", font=('Calibri 16'), foreground="black", background='white', variable=chkbox_var)
skoupa_chkbox.place(x=1050, y=200)

basi = panell.create_rectangle(50,230,1030,730, fill="grey70", outline="Black", width=5)
box = [[0] * 8 for i in range(4)]
box_size = 110
colors = ["none", "black", "blue", "green", "yellow", "red", "white"]
box_color = [[2] * 8 for i in range(4)]

box_color[1][0] = 3
box_color[2][0] = 4
box_color[3][0] = 5
gefyra_box_color = 0
real_pos_x = [[0] * 8 for i in range(4)]
real_pos_y = [[0] * 8 for i in range(4)]
real_pos_fix_x = [[0] * 8 for i in range(4)]
real_pos_fix_y = [[0] * 8 for i in range(4)]
box_pos_x = [[0] * 8 for i in range(4)]
box_pos_y = [[0] * 8 for i in range(4)]

my_file = open("fixes.txt","r")
for gr in range(4):
    for st in range (8):
        real_pos_fix_x[gr][st] = int(my_file.readline())
        real_pos_fix_y[gr][st] = int(my_file.readline())
my_file.close()

if leitourgia == 1:
    for gr in range(4):
        for st in range (8):
            real_pos_x[gr][st] = real_pos_fix_x[gr][st] + (realxmax - realxmin)//7 * st + realxmin
            real_pos_y[gr][st] = real_pos_fix_y[gr][st] + realymax - (realymax - realymin)//3 * gr
else:
    for gr in range(4):
        for st in range (8):
            real_pos_x[gr][st] = (realxmax - realxmin)//7 * st + realxmin
            real_pos_y[gr][st] = realymax - (realymax - realymin)//3 * gr

for gr in range(4):
    for st in range(8):
        box_pos_x[gr][st] = 120 * st + 120
        box_pos_y[gr][st] = 120 * gr + 300
for gr in range(4):
    for st in range(8):
        box[gr][st] = panell.create_rectangle(box_pos_x[gr][st] - box_size//2, box_pos_y[gr][st] - box_size//2, box_pos_x[gr][st] + box_size//2, box_pos_y[gr][st] + box_size//2, fill = colors[2])
gefyra_box = panell.create_rectangle(58 - 45,295 - 45,58 + 45,295 + 45, fill=colors[1])
gefyra = panell.create_polygon([(28,230),(88,230),(88,240),(68,240), (68,550), (88,550), (88,560), (28,560), (28,550), (48,550), (48,240), (28,240)], fill="brown", smooth=0)
skoupa = panell.create_rectangle(43,280,73,310, fill="brown2")
skoupa2 = panell.create_rectangle(58- 3,295 - 3,58 + 3,295 - 3, fill="red")
show1 = Button(panell, text = "Κανονική Λειτουργία - Καθαρισμός", width=30, height=1, fg="green", bg="white", font= ('Calibri 14'), command="x=0")
show1.place(x=1050, y=250)
show2 = Button(panell, text = "Απόρριψη Σπασμένου Panel", width=30, height=1, fg="black", bg="white", font= ('Calibri 14'), command="x=0")
show2.place(x=1050, y=320)
show3 = Button(panell, text = "Απόρριψη Panel χαμηλής απόδοσης", width=30, height=1, fg="black", bg="white", font= ('Calibri 14'), command="x=0")
show3.place(x=1050, y=390)
show4 = Button(panell, text = "Απόρριψη Βραχυκυκλωμένου Panel", width=30, height=1, fg="black", bg="white", font= ('Calibri 14'), command="x=0")
show4.place(x=1050, y=460)
show5 = Button(panell, text = "Τοποθέτηση νέου Panel", width=30, height=1, fg="black", bg="white", font= ('Calibri 14'), command="x=0")
show5.place(x=1050, y=540)
starttime = time.time()
gefyrax = 0
gefyray = 0
panell_master.update_idletasks()
panell_master.update()
time.sleep(3)

mode = 5
def operation_mode(mode):
    if mode == 0:
        show1.config(fg="white", bg="green")
        show2.config(fg="black", bg="white")
        show3.config(fg="black", bg="white")
        show4.config(fg="black", bg="white")
        show5.config(fg="black", bg="white")
    elif mode == 1:
        show1.config(fg="green", bg="white")
        show2.config(fg="white", bg="black")
        show3.config(fg="black", bg="white")
        show4.config(fg="black", bg="white")
        show5.config(fg="black", bg="white")
    elif mode == 2:
        show1.config(fg="green", bg="white")
        show2.config(fg="black", bg="white")
        show3.config(fg="white", bg="black")
        show4.config(fg="black", bg="white")
        show5.config(fg="black", bg="white")
    elif mode == 3:
        show1.config(fg="green", bg="white")
        show2.config(fg="black", bg="white")
        show3.config(fg="black", bg="white")
        show4.config(fg="white", bg="black")
        show5.config(fg="black", bg="white")
    elif mode == 4:
        show1.config(fg="green", bg="white")
        show2.config(fg="black", bg="white")
        show3.config(fg="black", bg="white")
        show4.config(fg="black", bg="white")
        show5.config(fg="white", bg="black")
    else:
        show1.config(fg="green", bg="white")
        show2.config(fg="black", bg="white")
        show3.config(fg="black", bg="white")
        show4.config(fg="black", bg="white")
        show5.config(fg="black", bg="white")

def look_color():
    global color, red, green, blue
    arduino.flush()
    arduino.write("1\n".encode())
    color = str(arduino.readline())[2:-5]
    color = color.split(';')
    red = int(color[0])
    green = int(color[1])
    blue = int(color[2])
    if green < red and green < blue:
        color = 3
    elif red / 1.4 < blue:
        if green - red < blue - green:
            color = 4
        else:
            color = 5
    else:
        color = 2

def update_display(gefyrax, gefyray):
    global gefyra, skoupa, box, box_pos_x, box_pos_y , skoupa2
    global box_color, box_size, colors, gefyra_box, mode, color
    labelxvalue.config(text=int(gefyrax))
    labelyvalue.config(text=int(gefyray))
    if mode == 0 and skoupa_on == False and chkbox_var.get():
        skoupa_ard(True)
    elif mode != 0 and skoupa_on == True:
        skoupa_ard(False)
    if mode == 0:
        for gr in range(4):
            if abs(real_pos_y[gr][0] - gefyray) < 40:
                for st in range(1,8):
                    if real_pos_x[gr][st] - gefyrax > 80 and real_pos_x[gr][st] - gefyrax < 90:
                        look_color()
                        if color != 2:
                            box_color[gr][st] = 0	
                    if real_pos_x[gr][st] - gefyrax > -10 and real_pos_x[gr][st] - gefyrax < 5:
                        look_color()
                        if box_color[gr][st] == 2:
                            box_color[gr][st] = color
    operation_mode(mode)
    for gr in range(4):
        for st in range(8):
            panell.delete(box[gr][st])
    for gr in range(4):
        for st in range(8):
            if box_color[gr][st] != 0:
                box[gr][st] = panell.create_rectangle(box_pos_x[gr][st] - box_size//2, box_pos_y[gr][st] - box_size//2, box_pos_x[gr][st] + box_size//2, box_pos_y[gr][st] + box_size//2, fill = colors[box_color[gr][st]])
    gefyrax = ((gefyraxmax - gefyraxmin)/realxmax) * gefyrax + gefyraxmin
    gefyray = gefyraymax - (((gefyraymax - gefyraymin)/realymax) * gefyray)
    panell.delete(gefyra_box)
    panell.delete(gefyra)
    panell.delete(skoupa)
    panell.delete(skoupa2)
    if gefyra_box_color != 0:
        gefyra_box = panell.create_rectangle(gefyrax - 45,gefyray - 45,gefyrax + 45,gefyray + 45, fill=colors[gefyra_box_color])
    gefyra = panell.create_polygon([(gefyrax-30,225),(gefyrax+30,225),(gefyrax+30,235),(gefyrax+10,235), (gefyrax+10,725), (gefyrax+30,725), (gefyrax+30,735), (gefyrax-30,735), (gefyrax-30,725), (gefyrax-10,725), (gefyrax-10,235), (gefyrax-30,235)], fill="brown", smooth=0)
    skoupa = panell.create_rectangle(gefyrax - 15,gefyray - 15,gefyrax + 15,gefyray + 15, fill="brown2")
    if int(time.time()/2) % 2 == 0:
        skoupa2 = panell.create_rectangle(gefyrax - 8,gefyray - 8,gefyrax + 8,gefyray + 8, fill="red")
    else:
        skoupa2 = panell.create_rectangle(gefyrax - 8,gefyray - 8,gefyrax + 8,gefyray + 8, fill="white")
    panell_master.update_idletasks()
    panell_master.update()

def rdln():
    try:
        return panellcnc.readline()
    except Exception:
        return "error"

def connectcnc(comport):
    global panellcnc, connected
    if connected != True:
        panellcnc = serial.Serial(port=f'COM{comport}', baudrate=115200)
        print(rdln())
        print(rdln())
        print(rdln())
        connected = True

def disconnectcnc():
    global connected, panellcnc
    if connected:
        connected = False
        panellcnc.close()

def speedacc(speed, acc):
    if speed != 0:
        panellcnc.write(f"$110={speed}\r\n".encode())
        temp = rdln()
        temp = rdln()
        panellcnc.write(f"$111={speed}\r\n".encode())
        temp = rdln()
        temp = rdln()
    if acc != 0:
        panellcnc.write(f"$120={acc}\r\n".encode())
        temp = rdln()
        temp = rdln()
        panellcnc.write(f"$121={acc}\r\n".encode())
        temp = rdln()
        temp = rdln()

prevx = 0
prevy = 0
def go(y,x):
    global prevx, prevy, connected, exit_var
    if exit_var > 0:
        exit_prog()
    pos = f'x{x}y{y}\r\n'
    panellcnc.write(pos.encode())
    rstr = rdln()
    xnow = prevx
    ynow = prevy
    while xnow!=float(x) or ynow!=float(y):
        panellcnc.write("?\r\n".encode())
        rstr = rdln()
        rstr = rdln()
        try:
            rstr2 = rstr.split(b'|')
            rstr2 = rstr2[1][5::]
            rstr2 = rstr2.split(b',')
            xnow = float(rstr2[0])
            ynow = float(rstr2[1])
            update_display(ynow,xnow)
        except Exception:
            pass
        rstr = rdln()
        time.sleep(0.05)
    rstr = rdln()
    prevx = x
    prevy = y

def gohome():
    global prevx, prevy
    thesixcalib = 0
    thesiycalib = 0
    prevthesixcalib = 0
    prevthesiycalib = 0
    speedcalib = 100
    while keyboard.is_pressed('ctrl') != True:
        if keyboard.is_pressed('s'):
            if keyboard.is_pressed('shift'):
                thesixcalib = thesixcalib - 10
                speedcalib = 5000
            else:
                thesixcalib = thesixcalib - 1
                speedcalib = 100
            pos = f'g1 x{thesixcalib}f{speedcalib}\r\n'
            panellcnc.write(pos.encode())
            rstr = rdln()
            while keyboard.is_pressed('s') == True:
                temp = 0
        if keyboard.is_pressed('w'):
            if keyboard.is_pressed('shift'):
                thesixcalib = thesixcalib + 10
                speedcalib = 5000
            else:
                thesixcalib = thesixcalib + 1
                speedcalib = 100
            pos = f'g1 x{thesixcalib}f{speedcalib}\r\n'
            panellcnc.write(pos.encode())
            rstr = rdln()
            while keyboard.is_pressed('w') == True:
                temp = 0
        if keyboard.is_pressed('a'):
            if keyboard.is_pressed('shift'):
                thesiycalib = thesiycalib - 10
                speedcalib = 5000
            else:
                thesiycalib = thesiycalib - 1
                speedcalib = 100
            pos = f'g1 y{thesiycalib}f{speedcalib}\r\n'
            panellcnc.write(pos.encode())
            rstr = rdln()
            while keyboard.is_pressed('a') == True:
                temp = 0
        if keyboard.is_pressed('d'):
            if keyboard.is_pressed('shift'):
                thesiycalib = thesiycalib + 10
                speedcalib = 5000
            else:
                thesiycalib = thesiycalib + 1
                speedcalib = 100
            pos = f'g1 y{thesiycalib}f{speedcalib}\r\n'
            panellcnc.write(pos.encode())
            rstr = rdln()
            while keyboard.is_pressed('d') == True:
                temp = 0
        if (prevthesixcalib != thesixcalib or prevthesiycalib != thesiycalib):
            print(thesixcalib, " ", thesiycalib)
        prevx = thesixcalib
        prevy = thesiycalib
        prevthesixcalib = thesixcalib
        prevthesiycalib = thesiycalib
        update_display(thesiycalib,thesixcalib)
    panellcnc.write("!\r\n".encode())
    temp = rdln()
    temp = rdln()
    disconnectcnc()
    connectcnc(port)

exit_var = 0
def exit_num():
    global exit_var
    exit_var = exit_var + 1
    exitpr.place_forget()

def exit_prog():
    global mode
    mode = 5
    arduino.write("34\n".encode())
    arduino.readline()
    arduino.write("46\n".encode())
    skoupa_ard(False)
    pos = f'x0y0\r\n'
    panellcnc.write(pos.encode())
    xnow = 100
    ynow = 100
    while xnow!=0 or ynow!=0:
        panellcnc.write("?\r\n".encode())
        rstr = rdln()
        rstr = rdln()
        try:
            rstr2 = rstr.split(b'|')
            rstr2 = rstr2[1][5::]
            rstr2 = rstr2.split(b',')
            xnow = float(rstr2[0])
            ynow = float(rstr2[1])
        except Exception:
            pass
        time.sleep(0.05)
    panell_master.destroy()
    quit()

skoupa_on = False
def skoupa_ard(temp):
    global skoupa_on
    arduino.flush()
    if temp:
        arduino.write("21\n".encode())
        skoupa_on = True
    else:
        arduino.write("22\n".encode())
        skoupa_on = False

def dump(fromgr, fromst):
    global mode, gefyra_box_color
    skoupa_ard(False)
    if box_color[fromgr][fromst] == 3:
        temp = 1
    elif box_color[fromgr][fromst] == 4:
        temp = 2
    else:
        temp = 3
    mode = temp
    speedacc(5000,250)
    go(real_pos_x[fromgr][fromst],real_pos_y[fromgr][fromst])
    arduino.flush()
    arduino.write("385\n".encode())
    arduino.readline()
    arduino.write("55\n".encode())
    arduino.readline()
    arduino.write("43\n".encode())
    time.sleep(0.3)
    arduino.flush()
    arduino.write("34\n".encode())
    arduino.readline()
    gefyra_box_color = box_color[fromgr][fromst]
    box_color[fromgr][fromst] = 0
    go(real_pos_x[temp][0],real_pos_y[temp][0]+3)
    arduino.write("365\n".encode())
    arduino.readline()
    arduino.write("46\n".encode())
    gefyra_box_color = 0
    time.sleep(1)
    arduino.write("34\n".encode())
    arduino.readline()
    time.sleep(1)

def place_new(togr, tost):
    global mode, gefyra_box_color
    skoupa_ard(False)
    mode = 4
    speedacc(5000,250)
    go(real_pos_x[0][0],real_pos_y[0][0])
    look_color()
    while color != 2:
        go(real_pos_x[2][2]-80,real_pos_y[2][2]-80)
        arduino.write("52\n".encode())
        koumpi = int(arduino.readline())
        while koumpi == 0:
            arduino.write("52\n".encode())
            koumpi = int(arduino.readline())
        go(real_pos_x[0][0],real_pos_y[0][0])
        look_color()
    arduino.flush()
    arduino.write("385\n".encode())
    arduino.readline()
    arduino.write("55\n".encode())
    arduino.readline()
    arduino.write("43\n".encode())
    time.sleep(0.3)
    arduino.flush()
    arduino.write("34\n".encode())
    arduino.readline()
    gefyra_box_color = 2
    go(real_pos_x[togr][tost],real_pos_y[togr][tost]+3)
    arduino.write("372\n".encode())
    arduino.readline()
    arduino.write("46\n".encode())
    gefyra_box_color = 0
    box_color[togr][tost] = 2
    time.sleep(1)
    arduino.write("34\n".encode())
    arduino.readline()
    time.sleep(1)


exitpr = Button(panell, text = "Έξοδος", width=10, height=1, fg="black", bg="white", font= ('Calibri 14'), command=exit_num)
exitpr.place(x=1250, y=150)
panell.pack()

while leitourgia == 2:
    testinput = int(input("Δώσε εντολή: "))
    if testinput == 100:
        gohome()
    if testinput == 200:
        dosegrammi = int(input('Δώσε γραμμή 0-3:'))
    if testinput == 8:
        real_pos_fix_y[dosegrammi][dosestili] = real_pos_fix_y[dosegrammi][dosestili] + 2
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 80:
        real_pos_fix_y[dosegrammi][dosestili] = real_pos_fix_y[dosegrammi][dosestili] + 5
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 4:
        real_pos_fix_x[dosegrammi][dosestili] = real_pos_fix_x[dosegrammi][dosestili] - 2
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 40:
        real_pos_fix_x[dosegrammi][dosestili] = real_pos_fix_x[dosegrammi][dosestili] - 5
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 6:
        real_pos_fix_x[dosegrammi][dosestili] = real_pos_fix_x[dosegrammi][dosestili] + 2
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 60:
        real_pos_fix_x[dosegrammi][dosestili] = real_pos_fix_x[dosegrammi][dosestili] + 5
        go(real_pos_x[dosegrammi][dosestili] + real_pos_fix_x[dosegrammi][dosestili],real_pos_y[dosegrammi][dosestili] + real_pos_fix_y[dosegrammi][dosestili])
    if testinput == 0:
        go(0,0)
    if testinput == 5:
        my_file = open("fixes.txt","w")
        for gr in range(4):
            for st in range (8):
                my_file.write(str(real_pos_fix_x[gr][st]))
                my_file.write("\n")
                my_file.write(str(real_pos_fix_y[gr][st]))
                my_file.write("\n")
        my_file.close()
    if testinput == 500:
        go(0,0)
        quit()
    if testinput == 1:
        arduino.flush()
        arduino.write("385\n".encode())
        arduino.readline()
    if testinput == 7:
        arduino.flush()
        arduino.write("34\n".encode())
        arduino.readline()
    if testinput == 900:
        go(real_pos_x[0][1],real_pos_y[0][1])
        look_color()
        print(red, end=" ")
        print(green, end=" ")
        print(blue, end=" ")
        print(red+green+blue)
        for i  in range(4):
            time.sleep(1)
            go(real_pos_x[i][0],real_pos_y[i][0])
            look_color()
            print(red, end=" ")
            print(green, end=" ")
            print(blue, end=" ")
            print(red+green+blue)
    



while leitourgia == 1:
    for scangr in range(4):
        mode = 5
        speedacc(7000,250)
        go(real_pos_x[scangr][0],real_pos_y[scangr][0])
        mode = 0
        speedacc(3000,250)
        go(real_pos_x[scangr][7],real_pos_y[scangr][7])
        for i in range(1,8):
            if box_color[scangr][i] != 2:
                if box_color[scangr][i] != 0:
                    dump(scangr,i)
                place_new(scangr,i)
    for gr in range(4):
        for st in range (1,8):
            box_color[gr][st] = 2

'''
$110=200 ταχύτητα στον άξονα Χ
$111=200 ταχύτητα στον άξονα Υ
$120=1200 επιτάχυνση στον άξονα Χ
$121=1200 επιτάχυνση στον άξονα Υ
X100 κίνηση στον άξονα Χ
Υ100 κίνηση στον άξονα Υ
X100Υ100 ταυτόχρονη κίνηση στον άξονα Χ και Υ
$$ αποθηκευμένες ρυθμίσεις
$1=255 φρένο όταν δεν κινείται
$1=0 ελεύθερο όταν δεν κινείται
'''