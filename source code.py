import cv2
import time
import sqlite3
import webbrowser
from io import BytesIO
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from cvzone.ClassificationModule import Classifier
from PIL import Image, ImageTk

classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
con = sqlite3.connect('enviromate.db')
cursor = con.cursor()

fh = open('Model/labels.txt')
class_lst = fh.readlines()
classes = []
for i in class_lst:
    j = i.split()[-1]
    classes.append(j)
    
win = Tk()
win.geometry("1300x700")
win.title("Start")
win.config(bg='#6BD275')

page1 = PhotoImage(file='Image/page1.png')
page2 = PhotoImage(file='Image/page2.png')
strt_img = PhotoImage(file='Image/start.png')
sett_img = PhotoImage(file='Image/settings.png')
exit_img = PhotoImage(file='Image/exit.png')
scan_img = PhotoImage(file='Image/scan.png')
carbFoot_img = PhotoImage(file='Image/footprint.png')
bin_img = PhotoImage(file='Image/bin.png')
locate_img = PhotoImage(file='Image/locate.png')

win1 = Frame(win, height=700, width=1300)
win1.pack()
img1 = Label(win1, image=page1)
img1.pack()

def image_tk(img):
    tk_image = PhotoImage(file=img)
    return tk_image

def back_to_menu(window,cam = False):
    window.destroy()
    if cam != False:
        cam[0].release()
        cam[1].destroy()  
    start()
    
def map_locate(link):
    webbrowser.open(link)

def start():
    win1.destroy()
    win.title("Menu")
    win2 = Frame(win, height=700, width=1300)
    win2.pack()
    img2 = Label(win2, image=page2)
    img2.pack()

    def Scan():
        win2.destroy()
        win.title("Scanner")
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        global c, load
        c = 0
        load = False
        predictions = []
        def update():
            _, frame = cap.read()
            if _:
                global frame_res
                frame_res = cv2.resize(frame, (422, 377))
                rgb_img = cv2.cvtColor(frame_res, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_img)
                tk_img = ImageTk.PhotoImage(pil_img)
                vid.config(image=tk_img)
                vid.image = tk_img
                vid.after(10, update)
                if load == True:
                    return 0

        def Scanner():
            global frame_res
            prog_lab = Label(win, bg='#A1F2A5', text="", font=("Times New Roman", 23), fg="#6BD275")
            prog_lab.place(relx=0.63, rely=0.558)
            
            for i in range(1,11):
                update()
                predictions.append(frame_res)
                prog_var = IntVar()
              
                prog_lab.config(text="Analyzing"+('.')*i)
                prog = Progressbar(win, orient=HORIZONTAL, length=300, mode='determinate', variable=prog_var)
                prog.place(relx=0.585, rely=0.678)

                for j in range(100):
                    prog_var.set((j / 100) * 100)
                    win.update_idletasks()
                    time.sleep(0.008)  

                prog_var.set(100)
                prog.start()

                prog.destroy() 
            cap.release()
            vid.destroy()
            
            def information(category):
                win3.destroy()
                fram.destroy()
                scan.destroy()
                prog_lab.destroy()
                win.title(category.capitalize())
                win4 = Frame(win, height=700, width=1300)
                win4.pack()
                cursor.execute("select image from information where category = '%s'"%(category))
                image_data = cursor.fetchall()[0][0]
                image = Image.open(BytesIO(image_data))
                pred_image = ImageTk.PhotoImage(image)
                img4 = Label(win4, image=pred_image)
                img4.pack()

                cursor.execute("select link from information where category = '%s'"%(category))
                url = cursor.fetchall()[0][0]
                
                if url != None:
                    loc = Button(image=locate_img,command=lambda:map_locate(url),bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
                    loc.place(relx=0.6215,rely=0.73)
                
                back = ttk.Button(text='Back',command=lambda:back_to_menu(win4))
                back.place(x=0,y=0)
                win4.mainloop()
                
            if predictions:
                predicts = []
                dict_pred = {}
                for img in predictions:
                    prediction, confidence = classifier.getPrediction(img)
                    predicts.append(classes[confidence])
                for i in list(dict.fromkeys(predicts)):
                    dict_pred[i] = predicts.count(i)
                Class = max(dict_pred.values())    
            
                if Class > 5 :
                    for i in dict_pred.keys():
                        if dict_pred[i] == Class:
                            Class = i
                    prog_lab.config(text="")
                    prog_lab.config(text=Class)
                    information(Class)
                else:
                    messagebox.showerror("ERROR","TRY AGAIN !")
            else:
                messagebox.showerror("ERROR","Please restart and try !")


        pag = PhotoImage(file='Image/page3.png')
        win3 = Label(win, image=pag)
        win3.pack()
        
        fram = Frame(win, height=430, width=480, bg='#BFF2B7')
        fram.place(x=183, y=176)
        vid = Label(fram, bg='#BFF2B7')
        vid.pack()

        back = ttk.Button(text='Back',command=lambda:back_to_menu(win3,[cap,fram]))
        back.place(x=0,y=0)
        scan = Button(win, command=Scanner, image=scan_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
        scan.place(relx=0.58, rely=0.409)
        update()
        win.mainloop()

    def footprint():
        pass

    def yourBin():
        pass

    scan = Button(win2, command=Scan, image=scan_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
    scan.place(relx=0.3815, rely=0.353)
    footPrint = Button(win2, command=footprint, image=carbFoot_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
    footPrint.place(relx=0.3789, rely=0.4885)
    Bin = Button(win2, command=yourBin, image=bin_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
    Bin.place(relx=0.38, rely=0.624)
    win2.mainloop()

def settings():
    pass

strt = Button(win1, command=start, image=strt_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
strt.place(relx=0.3787, rely=0.353)
setng = Button(win1, command=settings, image=sett_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
setng.place(relx=0.3787, rely=0.484)
Exit = Button(win1, command=quit, image=exit_img, bd=0, relief=FLAT, bg="#A1F2A5", fg="#A1F2A5")
Exit.place(relx=0.3787, rely=0.6195)

win1.mainloop()
win.mainloop()
