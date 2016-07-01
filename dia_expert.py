__author__ = 'Tiannan Guo, ETH Zurich 2015'

# this software reads in chromatographic text files, and openSWATH identification results,
# and refine fragments, perform quantification of fragments and peptides.

import os
import sys
import time
import dia_quant
import io_dia
import peak_groups
import r_code
import chrom
import parameters as param
from whichcraft import which

def print_help():
    print
    print "python %s accepts the following command line arguments:" % sys.argv[0]
    print
    print "   <chromatogram_file>:  path to chromatogram_file to process (mandatory)"
    print "   <path_to_rcmd_exe> :  path to Rcmd.exe or RScript on your computer (optional)"
    print

# if len(sys.argv) < 2:
#     print_help()
#     sys.exit(1)

# chrom_file = sys.argv[1]  # eg, com_chrom_1.txt.gz
# id_mapping_file = sys.argv[2]  #eg, 'goldenSets90.txt'
# tic_normalization_file = sys.argv[3]  #eg, 'gold90.tic'

chrom_file = 'com_chrom_32test2.txt.gz'
id_mapping_file = "nci60_sample_information.txt"
tic_normalization_file = "nci60.tic"
out_R_file = "com_chrom_32test2.R"


def remove_all_file_extensions(path):
    path = os.path.splitext(path)[0]
    while True:
        path, ext = os.path.splitext(path)
        if ext == "":
            return path

name_stem = remove_all_file_extensions(chrom_file)

out_chrom_file = name_stem + '.chrom.txt'
out_file_poor_tg = name_stem + '.poor.txt'
quant_file_fragments = name_stem + '.quant.fragments.txt'
quant_file_peptides = name_stem + '.quant.peptides.txt'
quant_file_proteins = name_stem + '.quant.proteins.txt'

def main():

    # read input file of sample information
    sample_id, raw_to_sample_id, sample_id_to_name = io_dia.read_id_file(id_mapping_file)

    # read TIC to compute normalization factor
    normalization_factors = io_dia.read_tic_normalization_file(tic_normalization_file)

    # read input chrom file,
    # build chrom_data, find peaks when the class is initialized
    ref_sample_data, chrom_data, peptide_data = io_dia.read_com_chrom_file(
        chrom_file, sample_id, normalization_factors)

    # based on peaks of fragments, keep peak groups with at least MIN_FRAGMENT
    # fragment, find out peak boundary of each fragment
    peak_group_candidates = peak_groups.find_peak_group_candidates(chrom_data, sample_id)

    # based on peak groups found in the reference sample, find out fragments
    # that form good peaks, remove the rest fragments
    ref_sample_data, chrom_data, peptide_data, peak_group_candidates = \
        peak_groups.refine_peak_forming_fragments_based_on_reference_sample(
            ref_sample_data, chrom_data, peptide_data, peak_group_candidates)

    # compute the peak boundary for the reference sample, write to display_pg
    display_data, peak_group_candidates, chrom_data = \
        chrom.compute_reference_sample_peak_boundary(ref_sample_data, chrom_data,
                                                     peptide_data, peak_group_candidates)

    # based on the display_data for reference sample, get the best matched peak groups from all other samples
    # and then write to display_data
    display_data = peak_groups.find_best_peak_group_based_on_reference_sample(
        display_data, ref_sample_data, chrom_data, peptide_data, peak_group_candidates, sample_id)

    # compute peak area for display_pg
    display_data = chrom.compute_peak_area_for_all(display_data)

    # compute peak area for only the peak-forming fragments
    display_data = dia_quant.compute_peak_area_for_refined_fragment(
        display_data, sample_id, ref_sample_data, quant_file_fragments)

    # compute peptide area
    dia_quant.compute_peptide_intensity_based_on_median_ratio_of_fragments(
        quant_file_peptides, quant_file_fragments, sample_id, ref_sample_data, display_data)

    # write r code into a file
    r_code.write_r_code_for_all_samples(display_data, sample_id, out_R_file, ref_sample_data)

start_time = time.time()
print "--- start conversion ---"
main()
print "--- %s seconds ---" % (time.time() - start_time)
