from Tkinter import *
from tkFileDialog import askopenfilenames, askopenfilename
from tkintertable import TableCanvas, TableModel

def main():

    root = Tk()
    root.config(background="white")
    root.title("DIA-expert v1.0")

    # step 1

    Label(root, text="Step 1").grid(row=0)
    Label(root, text="step 2").grid(row=1)
    Label(root, text="step 3.1").grid(row=3, column=0)
    Label(root, text="step 3.2").grid(row=3, column=1)
    Label(root, text="step 4.1").grid(row=4, column=0)
    Label(root, text="step 4.2").grid(row=4, column=1)





    root.mainloop()



main()
