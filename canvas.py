from tkinter import *




def onclick():
    board.delete('all')

def draw(event):
   
    x2,y2 = (event.x+1),(event.y+1)
    x1,y1 = (event.x-1),(event.y-1)
    
    board.create_oval(x1,y1,x2,y2,fill="blue",outline="blue")


t=Tk()

board= Canvas(t, width=600,height=600,bg='white')

board.pack(expand =YES,fill=BOTH)
board.bind('<B1-Motion>',draw)


button = Button(t,text="Clear Canvas",command=onclick)
button.pack()

t.mainloop()


