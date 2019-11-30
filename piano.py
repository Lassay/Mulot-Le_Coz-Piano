# -*- coding: utf-8 -*-

from frequencies_MVC import *
from keyboard_MVC import *
from wave_generator import *

if __name__ == "__main__" :
    root = Tk()

    root.geometry("1200x800")
    octaves=2
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    new=choix(root)
    new.packing()

    piano=Piano(root,octaves)
    piano.packing()
    model=Generator()

    view=Screen_sig(root)
    view.grid(4)
    model.attach(view)
    model.generate_signal()
    ctrl=Controller(root,model,view)
    view.packing()
    ctrl.packing()
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
    helpmenu.add_command(label="Créatrices", command=lambda:messagebox.showinfo("Créatrices", "Cette application a été développée par Mona Le Coz et Morgane Mulot"))
    MenuBar.add_cascade(label="A propos",menu=helpmenu)

    root.config(menu=MenuBar)

    root.mainloop()
