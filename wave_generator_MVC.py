# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
import os

import sqlite3

if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import *
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
else:
    print(sys.version)
    from tkinter import *
    from tkinter import filedialog

import collections

from observer  import *

from wav_audio import *

import subprocess

#sys.path.append("./Sounds")

class Screen_wav(Observer) :    #VUE
    def __init__(self,parent,bg="white"):

        self.parent=parent
        self.frame=Frame(self.parent)
        self.choixNote=Label(self.frame, text="Choisissez une note à créer :")
        self.entryNote=Entry(self.frame)
        self.labelNote=Label(self.frame, text="Note :")
        self.num = IntVar()
        self.num.set(0)
        self.labelNum=Label(self.frame, text="Octave :")
        self.boxOctave = Spinbox(self.frame,from_=0,to=8,increment=1,textvariable=self.num,width=5)
        self.listeNote = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
        self.note = StringVar()
        self.note.set(self.listeNote[0])
        self.boxNote = OptionMenu(self.frame, self.note, *self.listeNote)
        self.labelDuree=Label(self.frame, text="Durée :")
        self.duration=Scale(self.frame, orient='horizontal', from_=0, to=4,
                                resolution=0.1, tickinterval=1, length=150)
        self.titre = ''
        self.creer=Button(self.frame, text="créer", command=lambda:ctrl.creerNote(self.note.get(), self.boxOctave.get(), self.duration.get()))
        self.box = Listbox(self.frame)

        self.lire=Button(self.frame, text="Lire", command=lambda:ctrl.lireNote())

        self.choixAccord=Label(self.frame, text="Choisissez un accord à créer :")
        self.chord1 =StringVar()
        self.chord2 =StringVar()
        self.chord3 =StringVar()
        self.chord1.set(self.listeNote[0])
        self.chord2.set(self.listeNote[0])
        self.chord3.set(self.listeNote[0])
        self.boxChord1 = OptionMenu(self.frame, self.chord1, *self.listeNote)
        self.boxChord2 = OptionMenu(self.frame, self.chord2, *self.listeNote)
        self.boxChord3 = OptionMenu(self.frame, self.chord3, *self.listeNote)
        self.numChord1 = IntVar()
        self.numChord1.set(0)
        self.boxOctaveChord1 = Spinbox(self.frame,from_=0,to=8,increment=1,textvariable=self.numChord1,width=5)
        self.numChord2 = IntVar()
        self.numChord2.set(0)
        self.boxOctaveChord2 = Spinbox(self.frame,from_=0,to=8,increment=1,textvariable=self.numChord2,width=5)
        self.numChord3 = IntVar()
        self.numChord3.set(0)
        self.boxOctaveChord3 = Spinbox(self.frame,from_=0,to=8,increment=1,textvariable=self.numChord3,width=5)
        self.creerChord=Button(self.frame, text="créer", command=lambda:ctrl.creerAccord())
        self.boxChords = Listbox(self.frame)

        self.lireChord=Button(self.frame, text="Lire", command=lambda:ctrl.lireAccord())
        self.titreChord=''

        self.espaceVide = Label(self.frame, text="")

    def updateBox(self, note):
        x = True
        for i in range(5):
            if (self.box.get(i)==note):
                x = False
        if (x):
            if(self.box.get(4) != ""):
                self.box.delete(0)
            self.box.insert(END, note)

    def updateBoxChord(self, note):
        x = True
        for i in range(5):
            if (self.boxChords.get(i)==note):
                x = False
        if (x):
            if(self.boxChords.get(4) != ""):
                self.boxChords.delete(0)
            self.boxChords.insert(END, note)

    def packing(self):
        self.frame.pack()

        self.choixNote.grid(row=0, column=0, columnspan=5)
        self.labelNote.grid(row=1, pady=2)
        self.boxNote.grid(row=1, column = 1)
        self.labelNum.grid(row=2, column = 0)
        self.boxOctave.grid(row=2, column = 1)
        self.labelDuree.grid(row=3, column = 0)
        self.duration.grid(row=3, column = 1)
        self.creer.grid(row=2, column = 3)
        self.box.grid(row=2, column = 4)
        self.lire.grid(row=2, column = 5)

        self.espaceVide.grid(row=2, column=6, padx=20)

        self.choixAccord.grid(row=0, column=7, columnspan=5)
        self.boxChord1.grid(row=1, column=7)
        self.boxChord2.grid(row=2, column=7)
        self.boxChord3.grid(row=3, column=7)
        self.boxOctaveChord1.grid(row=1, column=8)
        self.boxOctaveChord2.grid(row=2, column=8)
        self.boxOctaveChord3.grid(row=3, column=8)
        self.creerChord.grid(row=2, column=9)
        self.lireChord.grid(row=2, column=11)
        self.boxChords.grid(row=2, column=10)


class Choix(Subject) : #MODEL
     def __init__(self):
        self.observers=[]

     def creerNote(self,note,octave,duration):
        view.titre = titre = str(note)+str(octave)+"_"+str(duration)+".wav"
        self.notify()
        connect = sqlite3.connect("frequencies.db")
        cursor = connect.cursor()
                # Gerer les sharp :
        if (note == 'C#' or note == 'D#' or note == 'F#' or note == 'G#' or note == 'A#'):
            f = cursor.execute("SELECT {0}{1} FROM frequencies WHERE octave = {2}".format(note[0], "sharp", int(octave))).fetchone()
        else:
            f = cursor.execute("SELECT {0} FROM frequencies WHERE octave = {1}".format(note, int(octave))).fetchone()

        x = wav_sinus("./noteCréée/"+view.titre, f[0], 8000, float(duration))

     def creerAccord(self):
        data1,framerate1 = open_wav('Sounds/'+str(view.chord1.get())+str(view.boxOctaveChord1.get())+'.wav')
        data2,framerate2 = open_wav('Sounds/'+str(view.chord2.get())+str(view.boxOctaveChord2.get())+'.wav')
        data3,framerate3 = open_wav('Sounds/'+str(view.chord3.get())+str(view.boxOctaveChord3.get())+'.wav')
        data = []
        for i in range(len(data1)):
            data.append((1/3.0)*(data1[i]+data2[i]+data3[i]))
        view.titreChord = str(view.chord1.get())+str(view.boxOctaveChord1.get())+str(view.chord2.get())+str(view.boxOctaveChord2.get())+str(view.chord3.get())+str(view.boxOctaveChord3.get())+'.wav'
        self.notify()
        save_wav('noteCréée/'+view.titreChord,data,framerate1)

     def notify(self):
        for obs in self.observers:
            obs.updateBox(view.titre)
            obs.updateBoxChord(view.titreChord)

class Controller :
    def __init__(self,parent,model,view) :
        self.model=model
        self.view=view
        view.box.configure(height = 5)
        view.boxChords.configure(height = 5)

    def creerNote(self,note,octave,duration):
        model.creerNote(note,octave,duration)

    def creerAccord(self):
        model.creerAccord()

    def lireNote(self):
        subprocess.call(["aplay", "./noteCréée/"+(view.box.get(view.box.curselection()))])

    def lireAccord(self):
        subprocess.call(["aplay", "./noteCréée/"+(view.boxChords.get(view.boxChords.curselection()))])



if __name__ == "__main__" :
    root = Tk()
    root.geometry("1200x400")
    root.title("Générateur de notes et d'accords")

    model = Choix()
    view = Screen_wav(root)

    model.attach(view)
    ctrl=Controller(root,model,view)
    view.packing()

    #MENU
    MenuBar= Menu(root)
    filemenu = Menu(MenuBar, tearoff=0)
    filemenu.add_command(label="Quitter",command=lambda:root.quit() if messagebox.askyesno("Quitter", "Etes-vous sûr de vouloir quitter?") else None)
    MenuBar.add_cascade(label="Fichier", menu=filemenu)

    helpmenu = Menu(MenuBar, tearoff=0)

    def read_me():
        file = open("./README.txt", 'r')
        alltext = file.read()
        file.close()
        messagebox.showinfo("Read Me", alltext)

    helpmenu.add_command(label="Read Me", command=read_me)
    helpmenu.add_command(label="Créatrices", command=lambda:messagebox.showinfo("Créatrices", "Cette application a été dévelopée par Mona Le Coz et Morgane Mulot"))
    MenuBar.add_cascade(label="A propos",menu=helpmenu)

    root.config(menu=MenuBar)
    root.mainloop()
