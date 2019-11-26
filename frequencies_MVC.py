from math import sin,pi

## from pylab import linspace,sin

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import *
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import *
    from tkinter import filedialog


from observer import *

class Generator(Subject) :
    def __init__(self):
        self.a,self.f,self.p=1.0,2.0,0.0
        self.signal=[]
        self.observers=[]
    def vibration(self,t,harmoniques=1,impair=True):
        a,f,p=self.a,self.f,self.p
        f=1.0
        somme=0
        for h in range(1,harmoniques+1) :
            somme=somme + (a/h)*sin(2*pi*(f*h)*t-p)
        return somme
    def generate_signal(self,period=2,samples=100):
        del self.signal[0:]
        echantillons=range(int(samples)+1)
        Tech = period/samples
        print("Tech",Tech,period,samples)
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        print(self.signal)
        self.notify()
        return self.signal
    def notify(self):
        for obs in self.observers:
            obs.update()


class Screen(Observer) :
    def __init__(self,parent,bg="white",width=600,height=300):
        self.canvas=Canvas(parent,bg=bg,width=width,height=height)
        self.signal={}
        self.units=1
        self.width,self.height=width,height
        self.canvas.bind("<Configure>",self.resize)
    def update(self):
        print("View : update()")
        #Generator.generate_signal(Generator)
        if self.signal :
            self.plot_signal(self.signal)
    def plot_signal(self,signal,color="red"):
        w,h=self.width,self.height
        signal_id=None
        if signal and len(signal) > 1:
            print(self.units)
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal]
            signal_id=self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags="sound")
        return signal_id
    def grid(self,steps=2):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")
    def resize(self,event):
        if event:
            print("event")
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            self.canvas.delete("sound")
            self.plot_signal(self.signal)
            self.grid(self.units)
    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

class Controller :
    def __init__(self,parent,model,view) :
        self.model=model
        self.view=view
        self.create_controls(parent)

    def create_controls(self,parent) :
        self.frame=LabelFrame(parent,text='Signal')
        self.amp=IntVar()
        self.amp.set(1)
        self.scaleA=Scale(self.frame,variable=self.amp,label="Amplitude",orient="horizontal",length=250,\
                            from_=0,to=5,tickinterval=1)
        self.scaleA.bind("<Button-1>",self.update_magnitude)

    def update_magnitude(self,event) :
        self.model.set_magnitude(self.amp.get())
        self.model.generate_signal()

    def packing(self) :
        self.frame.pack()

if  __name__ == "__main__" :
    root=Tk()
    root.title("Piano : Mulot Le Coz")
    model=Generator()
    view=Screen(root)
    view.grid(4)

    model.attach(view)
    model.generate_signal()
    ctrl=Controller(root,model,view)
    view.packing()
    ctrl.packing()

    root.mainloop()
