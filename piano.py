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

if(not(os.path.exists('./Sounds/B8.wav'))):
    print("Génération des notes du piano .wav")
    from frequencies import *
    from wav_create_notes_from_frequencies_db import *

from frequencies import *

from wav_audio import *

import subprocess

#sys.path.append("./Sounds")

class Octave(Subject) :
    def __init__(self,degree) :
        Subject.__init__(self)
        self.degree=degree
        self.set_gamme(degree)
    def set_gamme(self,degree) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]="./Sounds/"+key+str(degree)+".wav"
        return self.gamme
    def get_gamme(self) :
        return self.gamme
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)

class Screen(Observer):
    def __init__(self,parent) :
        self.parent=parent
        self.create_screen()
    def create_screen(self) :
        self.screen=Frame(self.parent,borderwidth=5,width=800,height=160,bg="pink")
        self.info=Label(self.screen,text="Appuyez sur une touche clavier ", bg="pink",font=('Arial',10))
        self.info.pack()
    def get_screen(self) :
        return self.screen
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys()  :
                raise AssertionError
        subprocess.call(["aplay", model.get_gamme()[key]])
        if self.info :
            self.info.config(text = "Vous avez joue la note : " + key + str(model.get_degree()))

class Keyboard :
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.create_keyboard()
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=Frame(self.parent,borderwidth=5,width=7*key_w,height=key_h,bg="red")
        for key in self.model.gamme.keys() :
            if  key.startswith( '#', 1, len(key) ) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=Button(self.keyboard,name=key.lower(),width=3,height=6, bg = "black")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                if key=="D" and self.model.get_degree() == 3 :
                    button=Button(self.keyboard,name=key.lower(),bg = "grey")
                else :
                    button=Button(self.keyboard,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
    def play_note(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees

class Piano :
    def __init__(self,parent,octaves) :
        self.parent=parent
        self.octaves=[]
        self.frame=Frame(self.parent,bg="yellow")
        for octave in range(octaves) :
            self.create_octave(self.frame,octave+2)
    def create_octave(self,parent,degree) :
        frame=Frame(parent,bg="green")
        model=Octave(degree)
        self.octaves.append(model)
        control=Keyboard(frame,model)
        view=Screen(frame)
        model.attach(view)
        view.get_screen().pack()
        control.get_keyboard().pack()
        frame.pack(side="left",fill="x",expand=True)
    def packing(self) :
        self.frame.pack()

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
        self.label2=Label(self.frame, text='...')

        self.lire=Button(self.frame, text="Lire", command=self.lireNote)


    def creerNote(self):
        self.titre = titre = str(self.v.get())+str(self.boiteNum.get())+"_"+str(self.duration.get())+".wav"
        self.label2.configure(text=self.titre)
        connect = sqlite3.connect("frequencies.db")
        cursor = connect.cursor()

        # Gerer les sharp :
        if (self.v.get() == 'C#' or self.v.get() == 'D#' or self.v.get() == 'F#' or self.v.get() == 'G#' or self.v.get() == 'A#'):
            f = cursor.execute("SELECT {0}{1} FROM frequencies WHERE octave = {2}".format(self.v.get()[0], "sharp", int(self.boiteNum.get()))).fetchone()
        else:
            f = cursor.execute("SELECT {0} FROM frequencies WHERE octave = {1}".format(self.v.get(), int(self.boiteNum.get()))).fetchone()

        x = wav_sinus("./noteCréée/"+self.titre, f[0], 8000, float(self.duration.get()))

    def lireNote(self):
        subprocess.call(["aplay", "./noteCréée/"+self.titre])


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
        self.label1.grid(row=1, column = 4, pady=2, padx=5)
        self.label2.grid(row=1, column = 5, pady=2, padx=5)
        self.lire.grid(row=1, column = 6, pady=2, padx=5)



if __name__ == "__main__" :
    root = Tk()

    root.geometry("700x400")
    octaves=2
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    new=choix(root)
    new.packing()
    piano=Piano(root,octaves)
    piano.packing()

    #MENU
    MenuBar= Menu(root)
    filemenu = Menu(MenuBar, tearoff=0)
    filemenu.add_command(label="Quitter",command=lambda:root.quit() if messagebox.askyesno("Quitter", "Etes-vous sûr de vouloir quitter?") else None)
    MenuBar.add_cascade(label="Fichier", menu=filemenu)

    helpmenu = Menu(MenuBar, tearoff=0)
    helpmenu.add_command(label="Read Me", command=lambda:messagebox.showinfo("Read Me", "Ajouter le contenu du Read Me"))
    helpmenu.add_command(label="Créatrices", command=lambda:messagebox.showinfo("Créatrices", "Cette application a été dévelopée par Mona Le Coz et Morgane Mulot"))
    MenuBar.add_cascade(label="A propos",menu=helpmenu)

    root.config(menu=MenuBar)

    root.mainloop()
