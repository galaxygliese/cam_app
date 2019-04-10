#-*- coding:utf-8 -*-

from PIL import Image, ImageTk
import threading as th
import tkinter as tk
import numpy as np
import cv2

class CamApp(tk.Frame):
     def __init__(self, W, H, S, master=None, Dir='./'):
         super().__init__(master)

         self.cam = 0
         self.Dir = Dir
         self.W = W       
         self.H = H       
         self.S = S       
 
         self.imgx = int(0.5*(W-S))
         self.imgy = int(50)

         self.cap = None
         self.path = None
         self.image = None
         self.cont = True
         self.thread = None

         self.pack()
         self.create_widgets()

     def create_widgets(self):
         x = 4
         self.button0 = tk.Button(self, text='start', command=self.start)
         self.button0.place(x=x, y=50, width=150, height=50 )
         self.button0.pack(side=tk.LEFT) #, padx=10)
 
         x += 4+4+100
         self.button1 = tk.Button(self, text='shutter', command=self.freeze_img)
         self.button1.place(x=x, y=50, width=100, height=50 )
         self.button1.pack(side=tk.LEFT, fill=tk.X) #, padx=10)
 
         x += 4+4+100
         self.la = tk.Label(self, text='Image Path:')
         self.la.pack(side=tk.LEFT)

         x += 4+4+100
         self.entry = tk.Entry(self)
         self.entry.place(x=x, y=50, width=100)
         self.entry.pack(side=tk.LEFT)          

         x += 4+4+100
         self.button2 = tk.Button(self, text='save', command=self.button2_pushed)
         self.button2.place(x=x, y=50, width=100, height=50 )
         self.button2.pack(side=tk.LEFT, fill=tk.X) 

         x += 4+4+100
         self.button3 = tk.Button(self, text='quit', command=self.end)
         self.button3.place(x=x, y=50, width=100, height=50 )
         self.button3.pack(side=tk.LEFT, fill=tk.X )

         x += 4+4+100
         self.la2 = tk.Label(self, text=' ')
         self.la2.place(x=x, y=50, width=100, height=50 )
         self.la2.pack(side=tk.LEFT)

     def videoloop(self):
         self.cap = cv2.VideoCapture(self.cam)
         self.cap.set(3, self.S)
         self.cap.set(4, self.S) 
         while True:
             ret, frame = self.cap.read()
             if ret and  self.cont:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.image = image
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                panel = tk.Label(image=image)
                panel.image = image
                panel.place(x=self.imgx, y=self.imgy) 
         return panel

 
     def start(self):
         self.thread = th.Thread(target=self.videoloop, args=())
         self.thread.start()

     def end(self):
         if self.cap is not None:
            self.cap.release()
         self.quit()

     def freeze_img(self):
         self.cont = not self.cont
         if self.cont:
            self.button1.config(text='shutter')
         else :
            self.button1.config(text='continue')

     def button2_pushed(self):
         self.path = self.entry.get()
         cv2.imwrite(self.Dir+'/'+self.path+'.jpg', self.image)
         self.la2['text'] = self.path+'.jpg is written'



H = 640
W = 1080
S = 640
root = tk.Tk()
root.geometry(str(W)+'x'+str(H))
app = CamApp(W, H, S, master=root, Dir='./images')
app.master.title('Camera App')
app.mainloop()
