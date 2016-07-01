__author__ = 'Tiannan Guo, ETH Zurich 2016'
from Tkinter import *
from tkFileDialog import askopenfilenames, askopenfilename, askdirectory
from tkintertable import TableCanvas, TableModel







def show_label_title(root, label_text, row_number, column_num):

    Label(root, text=label_text, bg="white", fg="blue").grid(row=row_number, column=column_num, columnspan=3, sticky=W)

def show_label(root, label_text, row_number, column_num):

    Label(root, text=label_text, bg="white", fg="black").grid(row=row_number, column=column_num, padx=2, pady=2, sticky=W)


def show_button(root, label_text, function_name, row_number, column_num):

    Button(root, text=label_text, command=function_name).grid(row=row_number, column=column_num, padx=2, pady=2)

def show_entry(root, default_value, row_number, column_num):

    e_peak_RT = Entry(root, bg="white", fg="black", width=2)
    e_peak_RT.insert(0, default_value)
    e_peak_RT.grid(row=row_number, column=column_num, padx=2, pady=2, sticky=W)
    return e_peak_RT



# chrom file
def chrom_readme():
    win = Toplevel()
    Label(win, text="combined chromatogram file").pack()
    Button(win, text="close", command=win.destroy).pack()

def chrom_browse():
    global com_chrom_file_name
    file = askopenfilename()
    com_chrom_file_name = file

def chrom_show():
    #if 'com_chrom_file_name' in globals():
        # show the first 10 lines of the file in a new window, preferable in a table
    print "to do: show the first lines of ", com_chrom_file_name

# norm file
def norm_readme():
    win = Toplevel()
    Label(win, text="normalization file").pack()
    Button(win, text="close", command=win.destroy).pack()

def norm_browse():
    global norm_file_name
    file = askopenfilename()
    norm_file_name = file

def norm_show():
    #if 'com_chrom_file_name' in globals():
        # show the first 10 lines of the file in a new window, preferable in a table
    print "to do: show the first lines of ", norm_file_name

# sample file
def sample_readme():
    win = Toplevel()
    Label(win, text="sample annotation file").pack()
    Button(win, text="close", command=win.destroy).pack()

def sample_browse():
    global sample_file_name
    file = askopenfilename()
    sample_file_name = file

def sample_show():
    #if 'com_chrom_file_name' in globals():
        # show the first 10 lines of the file in a new window, preferable in a table
    print "to do: show the first lines of ", sample_file_name

# pepID file
def pepID_readme():
    win = Toplevel()
    Label(win, text="peptide identification file").pack()
    Button(win, text="close", command=win.destroy).pack()

def pepID_browse():
    global pepID_file_name
    file = askopenfilename()
    pepID_file_name = file

def pepID_show():
    #if 'com_chrom_file_name' in globals():
        # show the first 10 lines of the file in a new window, preferable in a table
    print "to do: show the first lines of ", pepID_file_name


# peak RT file
def peakRT_readme():
    win = Toplevel()
    Label(win, text="peak group retention time (RT) tolerance").pack()
    Button(win, text="close", command=win.destroy).pack()

# bin RT file
def binRT_readme():
    win = Toplevel()
    Label(win, text="binning retention time value tolerance").pack()
    Button(win, text="close", command=win.destroy).pack()


def select_output_good_dir():
    global output_good_dir
    dir = askdirectory()
    output_good_dir = dir

def run_expert():

    print "run expert"

def view_plots():
    print "view plots"
