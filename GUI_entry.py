from Tkinter import *
from tkFileDialog import askopenfilenames, askopenfilename
from tkintertable import TableCanvas, TableModel

def select_com_chrom_files(chrom_file_entry):
    global com_chrom_file_name
    file = askopenfilename()
    com_chrom_file_name = file
    chrom_file_entry.delete(0, END)
    chrom_file_entry.insert(0, com_chrom_file_name)


def select_library_file(library_file_entry):
    global library_file_name
    file = askopenfilename()
    library_file_name = file
    library_file_entry.delete(0, END)
    library_file_entry.insert(0, library_file_name)

def select_sample_file(sample_file_entry):
    global sample_file_name
    file = askopenfilename()
    sample_file_name = file
    sample_file_entry.delete(0, END)
    sample_file_entry.insert(0, sample_file_name)

def select_nf_file(nf_file_entry):
    global nf_file_name
    file = askopenfilename()
    nf_file_name = file
    nf_file_entry.delete(0, END)
    nf_file_entry.insert(0, nf_file_name)

def select_pepID_file(pepID_file_entry):
    global pepID_file_name
    file = askopenfilename()
    pepID_file_name = file
    pepID_file_entry.delete(0, END)
    pepID_file_entry.insert(0, pepID_file_name)

def run_expert():

    print "run expert"

def view_plots():
    print "view plots"

def main():

    root = Tk()
    root.config(background="white")
    # root.resizable(width=False, height=False)
    # root.geometry('{}x{}'.format(800, 800))
    root.title("DIA-expert v1.0")
    row_number = 0

    # step 1
    Label(root, text="Step 1. specify input files", bg="white", fg="black", relief=RIDGE).grid(
        row=row_number)
    row_number += 1

    # select com_chrom file
    Label(root, text="select com_chrom file:", bg="white", fg="blue").grid(row=row_number, column=0, padx=2, pady=2)
    chrom_file_button = Button(root, text='browse...', command=(lambda: select_com_chrom_files(chrom_file_entry)))
    chrom_file_button.grid(row=row_number, column=1, padx=2, pady=2)
    chrom_file_entry = Entry(root, bg="white", fg="black", width=20)
    chrom_file_entry.insert(0, 'paste the directory and file name')
    chrom_file_entry.grid(row=row_number, column=2, padx=2, pady=2)
    row_number += 1

    # select sample file
    Label(root, text="select sample name file:", bg="white", fg="blue").grid(row=row_number, column=0,
                                                                                              padx=2, pady=2)
    sample_file_button = Button(root, text='browse...', command=(lambda: select_sample_file(sample_file_entry)))
    sample_file_button.grid(row=row_number, column=1, padx=2, pady=2)
    sample_file_entry = Entry(root, bg="white", fg="black", width=20)
    sample_file_entry.insert(0, 'paste the directory and file name')
    sample_file_entry.grid(row=row_number, column=2, padx=2, pady=2)
    row_number += 1

    # select library file
    Label(root, text="select library file:", bg="white", fg="blue").grid(row=row_number, column=0, padx=2, pady=2)
    library_file_button = Button(root, text='browse...', command=(lambda: select_library_file(library_file_entry)))
    library_file_button.grid(row=row_number, column=1, padx=2, pady=2)
    library_file_entry = Entry(root, bg="white", fg="black", width=20)
    library_file_entry.insert(0, 'paste the directory and file name')
    library_file_entry.grid(row=row_number, column=2, padx=2, pady=2)
    row_number += 1

    # select normalization factor file
    Label(root, text="select normalization factor file:", bg="white", fg="blue").grid(row=row_number, column=0, padx=2,
                                                                                              pady=2)
    nf_file_button = Button(root, text='browse...', command=(lambda: select_nf_file(nf_file_entry)))
    nf_file_button.grid(row=row_number, column=1, padx=2, pady=2)
    nf_file_entry = Entry(root, bg="white", fg="black", width=20)
    nf_file_entry.insert(0, 'paste the directory and file name')
    nf_file_entry.grid(row=row_number, column=2, padx=2, pady=2)
    row_number += 1

    # select peptide identification file
    Label(root, text="select peptide identification files:", bg="white", fg="blue").grid(row=row_number,
                                                                                                           column=0,
                                                                                                           padx=2,
                                                                                                           pady=2)

    pepID_file_button = Button(root, text='browse...', command=(lambda: select_pepID_file(pepID_file_entry)))
    pepID_file_button.grid(row=row_number, column=1, padx=2, pady=2)
    pepID_file_entry = Entry(root, bg="white", fg="black", width=20)
    pepID_file_entry.insert(0, 'paste the directory and file name')
    pepID_file_entry.grid(row=row_number, column=2, padx=2, pady=2)
    row_number += 1

    # step 2
    Label(root, text="", bg="white").grid(row=row_number)
    row_number += 1
    Label(root, text="Step 2. set parameters", bg="white", fg="black", relief=RIDGE).grid(
        row=row_number)
    row_number += 1

    #peak RT tolerance
    Label(root, text="peak RT tolerance (s):", bg="white", fg="blue").grid(row=row_number,
                                                                                    column=0, padx=2,pady=2)
    peak_rt_tol_entry = Entry(root, bg="white", fg="black", width=4)
    peak_rt_tol_entry.insert(0, '6')
    peak_rt_tol_entry.grid(row=row_number, column=1, padx=2, pady=2)

    # MIN_FRAGMENTS
    Label(root, text="min fragment number:", bg="white", fg="blue").grid(row=row_number, column=2,
                                                                                               padx=2,
                                                                                               pady=2)
    min_fragment_entry = Entry(root, bg="white", fg="black", width=4)
    min_fragment_entry.insert(0, '4')
    min_fragment_entry.grid(row=row_number, column=3, padx=2, pady=2)
    row_number += 1

    #     MIN_FRAGMENTS_HIGHER_THAN_INPUT_NO_MS1
    Label(root, text="MIN_FRAGMENTS_HIGHER_THAN_INPUT_NO_MS1:", bg="white", fg="blue").grid(row=row_number, column=0,
                                                                                             padx=2,pady=2)
    min_fragment_higher_than_input_no_ms1_entry = Entry(root, bg="white", fg="black", width=4)
    min_fragment_higher_than_input_no_ms1_entry.insert(0, '4')
    min_fragment_higher_than_input_no_ms1_entry.grid(row=row_number, column=1, padx=2, pady=2)

    #         MIN_FRAGMENTS_HIGHER_THAN_INPUT_UNIQUE_MS1
    Label(root, text="MIN_FRAGMENTS_HIGHER_THAN_INPUT_UNIQUE_MS1:", bg="white", fg="blue").grid(row=row_number,
                                                                                                                column=2,
                                                                                                                padx=2,
                                                                                                                pady=2)
    min_fragment_higher_than_input_uni_ms1_entry = Entry(root, bg="white", fg="black", width=4)
    min_fragment_higher_than_input_uni_ms1_entry.insert(0, '4')
    min_fragment_higher_than_input_uni_ms1_entry.grid(row=row_number, column=3, padx=2, pady=2)
    row_number += 1

    #             MAX_PEAK_WIDTH
    Label(root, text="MAX_PEAK_WIDTH:", bg="white", fg="blue").grid(
        row=row_number,column=0,padx=2,pady=2)
    max_peak_width_entry = Entry(root, bg="white", fg="black", width=4)
    max_peak_width_entry.insert(0, '4')
    max_peak_width_entry.grid(row=row_number, column=1, padx=2, pady=2)

    #                 PEAK_WIDTH_FOLD_VARIATION
    Label(root, text="PEAK_WIDTH_FOLD_VARIATION:", bg="white", fg="blue").grid(
        row=row_number, column=2, padx=2, pady=2)
    peak_width_tol_entry = Entry(root, bg="white", fg="black", width=4)
    peak_width_tol_entry.insert(0, '2.0')
    peak_width_tol_entry.grid(row=row_number, column=3, padx=2, pady=2)
    row_number += 1

    #                     PEAK_SHAPE_FOLD_VARIATION
    Label(root, text="PEAK_SHAPE_FOLD_VARIATION:", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)
    peak_shape_tol_entry = Entry(root, bg="white", fg="black", width=4)
    peak_shape_tol_entry.insert(0, '2.5')
    peak_shape_tol_entry.grid(row=row_number, column=1, padx=2, pady=2)

    #                         PEAK_SHAPE_FOLD_VARIATION_CRUDE
    Label(root, text="PEAK_SHAPE_FOLD_VARIATION_CRUDE:", bg="white", fg="blue").grid(
        row=row_number, column=2, padx=2, pady=2)
    peak_shape_tol_crude_entry = Entry(root, bg="white", fg="black", width=4)
    peak_shape_tol_crude_entry.insert(0, '2.0')
    peak_shape_tol_crude_entry.grid(row=row_number, column=3, padx=2, pady=2)
    row_number += 1

    #                             BINNING_RT_VALUE_TOLERANCE
    Label(root, text="BINNING_RT_VALUE_TOLERANCE:", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)
    binning_rt_tol_entry = Entry(root, bg="white", fg="black", width=4)
    binning_rt_tol_entry.insert(0, '5')
    binning_rt_tol_entry.grid(row=row_number, column=1, padx=2, pady=2)

    #                                 PEAK_BOUNDARY_RT_LEFT_RIGHT_RATIO_TOLERANCE
    Label(root, text="PEAK_BOUNDARY_RT_LEFT_RIGHT_RATIO_TOLERANCE:", bg="white", fg="blue").grid(
        row=row_number, column=2, padx=2, pady=2)
    peak_boundary_ratio_tol_entry = Entry(root, bg="white", fg="black", width=4)
    peak_boundary_ratio_tol_entry.insert(0, '0.6')
    peak_boundary_ratio_tol_entry.grid(row=row_number, column=3, padx=2, pady=2)
    row_number += 1

    # step 3
    Label(root, text="", bg="white").grid(row=row_number)
    row_number += 1
    Label(root, text="Step 3. Run DIA expert", bg="white", fg="black", relief=RIDGE).grid(
        row=row_number)
    row_number += 1

    # output_chrom_file_name
    Label(root, text="output_chrom_file_name:", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)
    output_chrom_file_entry = Entry(root, bg="white", fg="black", width=20)
    output_chrom_file_entry.insert(0, 'type in the file name')
    output_chrom_file_entry.grid(row=row_number, column=1, padx=2, pady=2)
    row_number += 1

    # not_selected_tg
    Label(root, text="not_selected_tg_file_name:", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)
    not_selected_tg_file_entry = Entry(root, bg="white", fg="black", width=20)
    not_selected_tg_file_entry.insert(0, 'type in the file name')
    not_selected_tg_file_entry.grid(row=row_number, column=1, padx=2, pady=2)
    row_number += 1
    # run the expert program
    run_expert_button = Button(root, text="run expert", command=run_expert).grid(row=row_number, column=0)
    row_number += 1

    # step 4
    Label(root, text="", bg="white").grid(row=row_number)
    row_number += 1
    Label(root, text="Step 4. View plots", bg="white", fg="black", relief=RIDGE).grid(
        row=row_number)
    row_number += 1

    # list of tg
    Label(root, text="list of tg", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)

    selected_tg_entry = Entry(root, bg="white", fg="black", width=20)
    selected_tg_entry.insert(0, 'type in the file name')
    selected_tg_entry.grid(row=row_number, column=1, padx=2, pady=2)
    row_number += 1

    # list of samples
    Label(root, text="list of samples", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)

    selected_samples_text = Text(root, height=10, bg="white", fg="black", width=20)
    selected_samples_text.insert(INSERT, 'put sample names, each sample per line')
    selected_samples_text.grid(row=row_number, column=1, padx=2, pady=2)
    row_number += 1

    # range of RT
    Label(root, text="range of RT", bg="white", fg="blue").grid(
        row=row_number, column=0, padx=2, pady=2)
    view_rt_range_entry = Entry(root, bg="white", fg="black", width=20)
    view_rt_range_entry.insert(0, 'type in the file name')
    view_rt_range_entry.grid(row=row_number, column=1, padx=2, pady=2)
    row_number += 1

    # run the expert program
    view_plots_button = Button(root, text="view plots", command=view_plots).grid(row=row_number, column=0)
    row_number += 1
    Label(root, text="", bg="white").grid(row=row_number)


    root.mainloop()



main()
