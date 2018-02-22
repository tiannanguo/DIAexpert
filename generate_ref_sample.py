#!/usr/bin/python

import os
import sys
import argparse

def generate_ref_from_filtered_files(files, out_file, m_score_th):
    """
    the input files must be .tsv formated, since each line of the files
    is going to be splitted by '\t'.
    """
    col_separator = '\t'

    tg_data = {}    # {'tg_name': {'filename': ..., 'm_score': ..., 'area': ..., 'rt': ...}}

    for filepath in files:
        fp = open(filepath, 'r')

        # read in the first line to look up columns position
        line = fp.readline()
        titles = line.strip().split(col_separator)
        titles_pos = {}
        for i in range(len(titles)):
            titles_pos[titles[i]] = i

        filename_pos = titles_pos['filename']
        peptide_group_label_pos = titles_pos['peptide_group_label']
        aggr_Peak_Area_pos = titles_pos['aggr_Peak_Area']
        m_score_pos = titles_pos['m_score']
        RT_pos = titles_pos['RT']

        # process remaining lines
        for line in fp:
            data = line.strip().split(col_separator)
            filename = data[filename_pos]
            tg = data[peptide_group_label_pos]
            m_score = float(data[m_score_pos])
            rt = float(data[RT_pos])
            aggr_peak_area = data[aggr_Peak_Area_pos].split(';')
            area = sum([float(a.strip()) for a in aggr_peak_area])

            if m_score > m_score_th:
                continue

            if tg.upper().startswith("DECOY_"):
                continue

            if not tg_data.has_key(tg):
                tg_data[tg] = {}

            tg_data_d = tg_data[tg]

            # try to set tg data dict if m_score is less than existing value
            if not tg_data_d.has_key('m_score') or tg_data_d['m_score'] > m_score:
                tg_data_d['m_score'] = m_score
                tg_data_d['filename'] = filename
                tg_data_d['area'] = area
                tg_data_d['rt'] = rt

    fout = open(out_file, 'w')
    fout.write('%s\t%s\t%s\t%s\n' %
        ('transition_name', 'reference_sample', 'reference_score', 'reference_rt'))

    for zz in tg_data.iteritems():
        tg_name = zz[0]
        data = zz[1]
        filename = os.path.basename(data['filename'])
        m_score = data['m_score']
        rt = data['rt']
        sample = filename[:filename.index('.mzXML')]
        fout.write('%s\t%s\t%s\t%s\n' % (tg_name, sample, m_score, rt))

    fout.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="generate reference_samples_file.tsv")

    parser.add_argument("--m_score_th", type=float, default=0.01,
        help="threshold for m_score, samples with m_score greater than this value will be discarded.")

    parser.add_argument("--csv_dir", required=True,
        help="all dscore_filtered_csv files under the directory will be processed.")

    parser.add_argument("--out", required=True,
        help="output file path. the format is tsv")

    args = parser.parse_args()

    csv_dir = args.csv_dir
    output_file = args.out
    m_score_th = args.m_score_th

    csv_files = []
    for f in os.listdir(csv_dir):
        if f.endswith('with_dscore_filtered.csv'):
            fpath = os.path.realpath(os.path.join(csv_dir, f))
            csv_files.append(fpath)

    generate_ref_from_filtered_files(csv_files, output_file, m_score_th)