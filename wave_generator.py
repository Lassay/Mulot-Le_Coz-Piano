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

from frequencies import *

from wav_audio import *

import subprocess

#sys.path.append("./Sounds")

class choix :
    def __init__(self,parent) :
        self.parent=parent
        self.frame=Frame(self.parent)
        self.label_Choix=Label(self.parent, text="Choisissez une note à créer :")

        self.entryNote=Entry(self.frame)
        self.labelNote=Label(self.frame, text="Note :")
        self.num = 0
        self.labelNum=Label(self.frame, text="Octave :")
        self.boiteNum = Spinbox(self.frame,from_=0,to=8,increment=1,textvariable=self.num,width=5)
        self.listeNote = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
        self.v = StringVar()
        self.v.set(self.listeNote[0])
        self.boxNote = OptionMenu(self.frame, self.v, *self.listeNote)
        self.labelDuree=Label(self.frame, text="Durée :")
        self.duration=Scale(self.frame, orient='horizontal', from_=0, to=4,
                            resolution=0.1, tickinterval=1, length=150)
        self.titre = ''

        self.creer=Button(self.frame, text="créer", command=self.creerNote)
        self.label1=Label(self.frame, text="Note créée :")
        self.box = Listbox(self.frame)
        self.box.configure(height = 5)


        self.lire=Button(self.frame, text="Lire", command=self.lireNote)



    def creerNote(self):
        self.titre = titre = str(self.v.get())+str(self.boiteNum.get())+"_"+str(self.duration.get())+".wav"
        self.updateBox(self.titre)
        connect = sqlite3.connect("frequencies.db")
        cursor = connect.cursor()
                # Gerer les sharp :
        if (self.v.get() == 'C#' or self.v.get() == 'D#' or self.v.get() == 'F#' or self.v.get() == 'G#' or self.v.get() == 'A#'):
            f = cursor.execute("SELECT {0}{1} FROM frequencies WHERE octave = {2}".format(self.v.get()[0], "sharp", int(self.boiteNum.get()))).fetchone()
        else:
            f = cursor.execute("SELECT {0} FROM frequencies WHERE octave = {1}".format(self.v.get(), int(self.boiteNum.get()))).fetchone()

        x = wav_sinus("./noteCréée/"+self.titre, f[0], 8000, float(self.duration.get()))

    def updateBox(self, note):
        self.box.insert(END, note)


    def lireNote(self):
        subprocess.call(["aplay", "./noteCréée/"+(self.box.get(self.box.curselection()))])

    def packing(self):
        self.label_Choix.pack()

        self.frame.pack()
        self.labelNote.grid(row=0, pady=2, padx=5)
        self.boxNote.grid(row=0, column = 1, pady=2, padx=5)
        self.labelNum.grid(row=1, column = 0, pady=2, padx=5)
        self.boiteNum.grid(row=1, column = 1, pady=2,padx=5)
        self.labelDuree.grid(row=2, column = 0, pady=2, padx=5)
        self.duration.grid(row=2, column = 1, pady=2, padx=5)
        self.creer.grid(row=1, column = 3,pady=2, padx=5)
        #self.label1.grid(row=1, column = 4, pady=2, padx=5)
        self.box.grid(row=1, column = 4,pady=2, padx=5)
        self.lire.grid(row=1, column = 8, pady=2, padx=5)




if __name__ == "__main__" :
    root = Tk()
    root.geometry("700x400")
    new=choix(root)
    new.packing()

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

    helpmenu.add_command(label="Read Me", command=read_me))
    helpmenu.add_command(label="Créatrices", command=lambda:messagebox.showinfo("Créatrices", "Cette application a été dévelopée par Mona Le Coz et Morgane Mulot"))
    MenuBar.add_cascade(label="A propos",menu=helpmenu)

    root.config(menu=MenuBar)
    root.mainloop()
