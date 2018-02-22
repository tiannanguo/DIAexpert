__author__ = 'Tiannan Guo, ETH Zurich 2015'

# this software reads in chromatographic text files, and openSWATH identification results,
# and refine fragments, perform quantification of fragments and peptides.

import os
import sys
import time
import swath_quant
import io_swath
import peak_groups
import r_code
import chrom
import parameters as param
from whichcraft import which
import data_holder

def print_help():
    print
    print "python %s accepts the following command line arguments:" % sys.argv[0]
    print
    print "   <chromatogram_file>:  path to chromatogram_file to process (mandatory)"
    print "   <path_to_rcmd_exe> :  path to Rcmd.exe or RScript on your computer (optional)"
    print

if len(sys.argv) < 2:
    print_help()
    sys.exit(1)

# chrom_file = "com_chrom.txt.gz"
# # chrom_file = "com_chrom_9_9.txt.gz"
# id_mapping_file = "goldenSets90.txt"
# tic_normalization_file = "gold90.tic"

chrom_file = sys.argv[1]  # eg, com_chrom_1.txt.gz
id_mapping_file = sys.argv[2]  #eg, 'goldenSets90.txt'
tic_normalization_file = sys.argv[3]  #eg, 'gold90.tic'

def remove_all_file_extensions(path):
    path = os.path.splitext(path)[0]
    while True:
        path, ext = os.path.splitext(path)
        if ext == "":
            return path

name_stem = remove_all_file_extensions(chrom_file)

out_R_file = name_stem + '.R'
out_file_poor_tg = name_stem + '.poor.txt'
quant_file_fragments = name_stem + '.quant.fragments.txt'
quant_file_peptides = name_stem + '.quant.peptides.txt'
quant_file_proteins = name_stem + '.quant.proteins.txt'
quant_file_peptides_ms1 = name_stem + '.quant.peptides_ms1.txt'


if sys.platform == "win32":
    batch_file = name_stem + ".bat"
else:
    batch_file = name_stem + ".sh"


def check_r():
    if len(sys.argv) == 3:
        r_path = sys.argv[2]
    elif sys.platform == 'win32':
        r_path = r'C:\R\R-2.15.1\bin\x64\Rcmd.exe'
    elif sys.platform in ('linux', 'darwin'):
        r_path = which('RScript')  # might return None
    else:
        raise Exception("platform %r not supported (yet)" % sys.platform)

    if r_path is None or not os.path.exists(r_path):
        print
        print "could not find R interpreter at %r" % r_path
        print_help()
        sys.exit(1)
    return r_path


def write_bat_file(out_R_file, batch_file):
    with open(batch_file, 'w') as o:
        if param.platform == 'linux':
            cmd = 'R CMD BATCH ' % (out_R_file)
        elif param.platform == 'tiannan_windows':
            cmd = 'C:\R\R-2.15.1\bin\x64\Rcmd.exe %s\n' % out_R_file
        o.write(cmd)
        o.write('\n')

def main():

    # read input file of sample information
    sample_id, id_mapping = io_swath.read_id_file(id_mapping_file)

    normalization_factors = io_swath.read_tic_normalization_file(tic_normalization_file)

    # build chrom_data, find peaks when the class is initialized
    ref_sample_data, chrom_data, peptide_data = io_swath.read_com_chrom_file(
        chrom_file, sample_id, normalization_factors)

    display_data = peak_groups.find_best_fit_peak_groups(
            chrom_data, ref_sample_data, peptide_data, sample_id)

    # compute peak area for display_pg
    display_data = chrom.compute_peak_area_for_all(display_data)

    # compute peak area for only the peak-forming fragments
    display_data,fragment_area_data = swath_quant.compute_peak_area_for_refined_fragment(
        display_data, sample_id, ref_sample_data, quant_file_fragments)
    # computer peak area for ms1 peptide
    display_data = swath_quant.compute_peak_area_for_refined_peptides_ms1(
        display_data, sample_id, ref_sample_data, quant_file_peptides_ms1)

    # compute peptide area
    swath_quant.compute_peptide_intensity_based_on_median_ratio_of_fragments_v1(
        quant_file_peptides, fragment_area_data, sample_id, ref_sample_data, display_data)

    # write r code into a file
    r_code.write_r_code_for_all_samples(display_data, sample_id, out_R_file, ref_sample_data)


#2018.1,this progrom style is more python
if __name__ == '__main__':
    start_time = time.time()
    print "--- start processing at %s---"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    main()
    print "--- end processing after %s seconds ---" % (time.time() - start_time)




