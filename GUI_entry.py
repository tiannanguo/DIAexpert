from Tkinter import *
from tkFileDialog import askopenfilenames, askopenfilename
import tkFont
from tkintertable import TableCanvas, TableModel
import GUI

def main():

    global if_select_all_samples
    if_select_all_samples = 1

    root = Tk()
    root.config(background="white")
    # root.resizable(width=False, height=False)
    # root.geometry('{}x{}'.format(800, 800))
    root.title("DIA-expert v1.0")
    row_number = 0

    GUI.show_label_title(root, "Part1. generate normalization factor table", row_number, 0)

    row_number += 1

    GUI.show_button(root, "readme", GUI.chrom_readme, row_number, 2)  #####
    Button(root, text='Generate normalization factor list', command=(lambda: chrom_extract_main(root))).grid(row=row_number, column=3, padx=2, pady=2, columnspan=2)   #####

    row_number += 1

    GUI.show_label_title(root, "Part2. chromatogram extraction", row_number, 0)

    row_number += 1

    GUI.show_button(root, "readme", GUI.chrom_readme, row_number, 2)  #####
    Button(root, text='Chromatogram extraction', command=(lambda: chrom_extract_main(root))).grid(row=row_number, column=3, padx=2, pady=2, columnspan=2)

    row_number += 1

    GUI.show_label_title(root, "Part3. Run expert system", row_number, 0)

    row_number += 1

    GUI.show_button(root, "readme", run_expert_main, row_number, 2)  #####
    Button(root, text='Run expert system', command=(lambda: run_expert_main(root))).grid(row=row_number, column=3, padx=2, pady=2, columnspan=2)

    # GUI.show_button(root, "Run expert system", GUI.chrom_browse, row_number, 3) ####

    row_number += 1

    GUI.show_label_title(root, "Part4. View plots", row_number, 0)

    row_number += 1

    GUI.show_button(root, "readme", GUI.chrom_readme, row_number, 2)  #####
    Button(root, text='View plots', command=(lambda: view_plots_main(root))).grid(row=row_number, column=3, padx=2, pady=2, columnspan=2)

    root.mainloop()


def chrom_extract_main(root):
    win = Toplevel()
    win.config(background="white")

    row_number = 0

    # step 4 view refined plot
    GUI.show_label_title(win, "Step 1. extract chromatograph", row_number, 0)


def view_plots_main(root):
    win = Toplevel()
    win.config(background="white")

    row_number = 0

    # step 4 view refined plot
    GUI.show_label_title(win, "Step 4. view plots", row_number, 0)

    row_number += 1

    GUI.show_label(win, "peptide:", row_number, 1)
    GUI.show_button(win, "readme", GUI.norm_readme, row_number, 2)  ##############re-write func
    GUI.show_button(win, "select", GUI.norm_browse, row_number, 3)  ##############re-write func
    GUI.show_button(win, "show", GUI.norm_show, row_number, 4)  ##############re-write func

    GUI.show_label(win, "samples:", row_number, 6)
    GUI.show_button(win, "readme", GUI.norm_readme, row_number, 7)  ##############re-write func
    c_all_samples = Checkbutton(win, text="all", variable=if_select_all_samples).grid(row=row_number, column=8, padx=2, pady=2)
    GUI.show_button(win, "select", GUI.norm_browse, row_number, 9)  ##############re-write func
    GUI.show_button(win, "show", GUI.norm_show, row_number, 10)  ##############re-write func

    row_number += 1

    # peak shape 2
    GUI.show_label(win, "RT range:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2) ##############re-write func
    e_view_rt_range = GUI.show_entry(win, 6, row_number, 3)

    row_number += 1

    Button(win, text="Click to View Results on the fly", command=GUI.peakRT_readme).grid(row=row_number, column=1,
                                                                                        padx=2, pady=2,
                                                                                        columnspan=3)  ##############re-write func

    Button(win, text="Click to Save all plots as png", command=GUI.peakRT_readme).grid(row=row_number, column=5,
                                                                                          padx=2, pady=2,
                                                                                          columnspan=3)  ##############re-write func

    Button(win, text="Click to Save all plots as pdf", command=GUI.peakRT_readme).grid(row=row_number, column=8,
                                                                                        padx=2, pady=2,
                                                                                        columnspan=3)  ##############re-write func

def run_expert_main(root):
    win = Toplevel()
    win.config(background="white")

    row_number = 0

    # step 1
    GUI.show_label_title(win, "Step 1. input files", row_number, 0)
    row_number += 1

    # select com_chrom file
    GUI.show_label(win, "chrom:", row_number, 1)
    GUI.show_button(win, "readme", GUI.chrom_readme, row_number, 2)
    GUI.show_button(win, "browse", GUI.chrom_browse, row_number, 3)
    GUI.show_button(win, "show", GUI.chrom_show, row_number, 4)

    # select normalization
    GUI.show_label(win, "norm:", row_number, 6)
    GUI.show_button(win, "readme", GUI.norm_readme, row_number, 7)
    GUI.show_button(win, "browse", GUI.norm_browse, row_number, 8)
    GUI.show_button(win, "show", GUI.norm_show, row_number, 9)

    row_number += 1

    # select sample file
    GUI.show_label(win, "sample:", row_number, 1)
    GUI.show_button(win, "readme", GUI.chrom_readme, row_number, 2)
    GUI.show_button(win, "browse", GUI.chrom_browse, row_number, 3)
    GUI.show_button(win, "show", GUI.chrom_show, row_number, 4)

    # select peptide ID file
    GUI.show_label(win, "pepID:", row_number, 6)
    GUI.show_button(win, "readme", GUI.pepID_readme, row_number, 7)
    GUI.show_button(win, "browse", GUI.pepID_browse, row_number, 8)
    GUI.show_button(win, "show", GUI.pepID_show, row_number, 9)

    row_number += 1

    # save file names
    GUI.show_label(win, "save files names:", row_number, 1)
    GUI.show_button(win, "readme", GUI.chrom_readme, row_number, 2)
    GUI.show_button(win, "save", GUI.chrom_browse, row_number, 3)
    GUI.show_button(win, "open", GUI.chrom_show, row_number, 4)

    row_number += 1

    # step 2
    GUI.show_label_title(win, "Step 2. parameters", row_number, 0)
    row_number += 1

    # peak RT
    GUI.show_label(win, "peak RT:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2)
    e_peak_RT = GUI.show_entry(win, 6, row_number, 3)

    # bin RT
    GUI.show_label(win, "bin RT:", row_number, 5)
    GUI.show_button(win, "readme", GUI.binRT_readme, row_number, 6)
    e_bin_RT = GUI.show_entry(win, 5, row_number, 7)

    # min fragment 1
    GUI.show_label(win, "min frag1:", row_number, 9)
    GUI.show_button(win, "readme", GUI.binRT_readme, row_number, 10)   ##############re-write func
    e_min_frag1 = GUI.show_entry(win, 5, row_number, 11)

    row_number += 1

    # min fragment 2
    GUI.show_label(win, "min frag2:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2) ##############re-write func
    e_min_frag2 = GUI.show_entry(win, 6, row_number, 3)

    # min fragment 3
    GUI.show_label(win, "min frag3:", row_number, 5)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 6) ##############re-write func
    e_min_frag3 = GUI.show_entry(win, 6, row_number, 7)


    # peak shape 1
    GUI.show_label(win, "peak shape 1:", row_number, 9)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 10) ##############re-write func
    e_peak_shape1 = GUI.show_entry(win, 6, row_number, 11)

    row_number += 1

    # peak shape 2
    GUI.show_label(win, "peak shape 2:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2) ##############re-write func
    e_peak_shape2 = GUI.show_entry(win, 6, row_number, 3)

    # peak shape 3
    GUI.show_label(win, "peak shape 3:", row_number, 5)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 6) ##############re-write func
    e_peak_shape3 = GUI.show_entry(win, 6, row_number, 7)

    # peak shape 4
    GUI.show_label(win, "peak shape 4:", row_number, 9)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 10) ##############re-write func
    e_peak_shape4 = GUI.show_entry(win, 6, row_number, 11)

    row_number += 1

    # output file good
    GUI.show_label(win, "output good:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2) ##############re-write func
    GUI.show_button(win, "directory", GUI.select_output_good_dir, row_number, 3)
    e_output_good = Entry(win, bg="white", fg="black", width=20)
    e_output_good.insert(0, "output_good_tg.txt")
    e_output_good.grid(row=row_number, column=4, padx=2, pady=2, sticky=W, columnspan=5)

    row_number += 1

    # output file poor
    GUI.show_label(win, "output poor:", row_number, 1)
    GUI.show_button(win, "readme", GUI.peakRT_readme, row_number, 2)  ##############re-write func
    GUI.show_button(win, "directory", GUI.select_output_good_dir, row_number, 3)  ##############re-write func
    e_output_good = Entry(win, bg="white", fg="black", width=20)
    e_output_good.insert(0, "output_poor_tg.txt")
    e_output_good.grid(row=row_number, column=4, padx=2, pady=2, sticky=W, columnspan=5)

    row_number += 1

    # save parameters
    GUI.show_label(win, "save parameters:", row_number, 1)
    GUI.show_button(win, "readme", GUI.chrom_readme, row_number, 2)
    GUI.show_button(win, "save", GUI.chrom_browse, row_number, 3)
    GUI.show_button(win, "open", GUI.chrom_show, row_number, 4)

    row_number += 1

    # step 3 output file
    GUI.show_label_title(win, "Step 3. run the expert system", row_number, 0)

    row_number += 1

    Button(win, text="Click to Run the Expert System", command=GUI.peakRT_readme).grid(row=row_number, column=1, padx=2, pady=2, columnspan=3)  ##############re-write func

    row_number += 1

main()
