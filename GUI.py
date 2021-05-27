from tkinter import *

def showGUI():
    root = Tk()
    w = Label(root, text='Raindrop-Removal-With-Light-Field-Image-Using-Image-Inpaintin')
    w.pack()
    frame = Frame(root)
    frame.pack()
    # bottomframe = Frame(root)
    # bottomframe.pack( side = BOTTOM )
    redbutton = Button(frame, text = 'Run With Sample Image (From Verification Set)', fg ='red')
    # redbutton.pack( side = LEFT)
    redbutton.pack()
    greenbutton = Button(frame, text = 'Run With Random Image (From Verification Set)', fg='brown')
    # greenbutton.pack( side = LEFT )
    greenbutton.pack()
    bluebutton = Button(frame, text ='Perform Verification Using Verification Set', fg ='blue')
    # bluebutton.pack( side = LEFT )
    bluebutton.pack()
    blackbutton = Button(frame, text ='Run With Array of Images (From Verification Set)', fg ='black')
    # bluebutton.pack( side = LEFT )
    bluebutton.pack()
    blackbutton = Button(frame, text ='Run With Array of Random Images (From Verification Set)', fg ='black')
    # blackbutton.pack( side = BOTTOM)
    blackbutton.pack()
    root.mainloop()

if __name__ == "__main__":
    showGUI()
