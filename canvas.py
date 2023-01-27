from tkinter import *




def onclick():
    board.delete('all')

def draw(event):
    x1=(event.x-2)
    y1 = (event.y-2)
    x2 = (event.x+2)
    y2 = (event.y+2)
   
    
    board.create_oval(x1,y1,x2,y2,fill="blue",outline="blue")


t=Tk()

board= Canvas(t, width=600,height=600,bg='white')

board.pack()
board.bind('<B1-Motion>',draw)


button = Button(t,text="Clear Canvas",command=onclick)
button.pack()

t.mainloop()


