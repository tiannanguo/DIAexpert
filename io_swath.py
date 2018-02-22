__author__ = 'guot'

import csv
import gzip
import data_holder

def read_sample_replicate_info(sample_replicates_info_file):

    unqiue_sample = {}

    with open(sample_replicates_info_file, 'r') as f:
        line_num = 1
        for line in f:
            unqiue_sample[line_num] = line.split("\t")
            line_num += 1

    return unqiue_sample


def read_id_file(id_mapping_file):
    sample_id = []
    id_mapping = {}
    with open(id_mapping_file) as i:
        reader = csv.reader(i, delimiter="\t")
        for row in reader:
            sample_id.append(row[1])
            id_mapping[row[0].lower()] = row[1]
    return sample_id, id_mapping

#at 2018.1,optimize the io process
#reduce i/o operation by finding the best_sample information in memory insteand of in replicated file

def read_com_chrom_file(chrom_file, sample_id, normalization_factors):
    tg_list = {}
    best_sample = {}
    best_rt = {}
    best_score = {}

    ref_sample_data = {}
    chrom_data = data_holder.NestedDict()
    peptide_data = data_holder.NestedDict()
    # count = 0
    with gzip.open(chrom_file, 'rb') as i:
        r = csv.DictReader(i, delimiter='\t')
        for row in r:
            #just for debuging
            # count = count + 1
            # print("%d row(s) have been read" % count)

            # find all  tgs and their numbers
            tg = row['transition_group_id']
            fragment = row['transition_name']

            # peptide_data
            peptide_data[tg]['ms1']['preMz'] = float(row['precursor_mz'])
            peptide_data[tg]['ms1']['protein'] = row['protein']
            peptide_data[tg]['ms1']['irt'] = float(row['irt'])
            peptide_data[tg]['ms2'][fragment] = float(row['transition_mz'])

            for k in sample_id:
                rt_list_three_values_csv = row[k + '_rt']
                i_list_csv = row[k + '_i']

                if rt_list_three_values_csv == "NA" or rt_list_three_values_csv == "0,0,0" or i_list_csv == "NA" or i_list_csv == 0:
                    i_list_csv = "NA"
                    chrom_data[tg][k][fragment] = "NA"
                else:
                    i_list_csv = apply_normalization_based_on_tic(i_list_csv, normalization_factors, k)
                    chrom_data[tg][k][fragment] = data_holder.Chromatogram(
                        rt_list_three_values_csv, i_list_csv)

            #to find the best_sample information
            if tg not in tg_list:
                tg_list[tg] = 1
            else:
                tg_list[tg] = tg_list[tg] + 1

            #this is a bug
            if tg_list[tg] == 1:
                best_sample[tg] = row['best_sample']
                best_score[tg] = float(row['best_score'])
                best_rt[tg] = float(row['best_rt'])
            else:   #occered more than one times
                if float(row['best_score']) < float(best_score[tg]):
                    best_sample[tg] = row['best_sample']
                    best_rt[tg] = float(row['best_rt'])
                    best_score[tg] = float(row['best_score'])

        # ref_sample_data
        for tg in tg_list:
            ref_sample_data[tg] = data_holder.ReferenceSample(best_sample[tg], best_score[tg], float(best_rt[tg]))

    return ref_sample_data, chrom_data, peptide_data



def apply_normalization_based_on_tic(i_list_csv, normalization_factors, k):

    if i_list_csv != 'NA':
        i_list = map(float, i_list_csv.split(','))
        norm_factor = compute_norm_factor(k, normalization_factors)

        if len(i_list) > 1:
            i_list2 = [round(x * norm_factor, 1) for x in i_list]
            i_list2_str = map(str, i_list2)
            i_list_csv2 = ','.join(i_list2_str)
            return i_list_csv2
        else:
            return i_list_csv
    else:
        return i_list_csv


def compute_norm_factor(k, normalization_factors):
    max_i = max(normalization_factors.values())
    if normalization_factors[k] <= 0:
        print 'error: sample %s has wrong tic value' % k
    norm_factor = float(max_i) / float(normalization_factors[k])
    return norm_factor


def get_tg_list(chrom_file):
    tg_list = {}
    with gzip.open(chrom_file, 'rb') as i:
        r = csv.DictReader(i, delimiter="\t")
        for row in r:
            tg_list[row['transition_group_id']] = 1
    return tg_list.keys()


def get_best_sample_for_each_tg(chrom_file, tg_list):

    best_sample = {}
    best_score = {}
    best_rt = {}

    for tg in tg_list:
        best_sample[tg] = ''
        best_score[tg] = 1.0
        best_rt[tg] = -1.0

        with gzip.open(chrom_file, 'rb') as i:

            r = csv.DictReader(i, delimiter="\t")

            for row in r:
                tg2 = row['transition_group_id']
                if tg2 == tg and float(row['best_score']) < float(best_score[tg]):
                    best_sample[tg] = row['best_sample']
                    best_rt[tg] = row['best_rt']
                    best_score[tg] = float(row['best_score'])

    return best_sample, best_score, best_rt


def read_tic_normalization_file(tic_normalization_file):

    norm_factor = {}

    with open(tic_normalization_file, 'rb') as i:
        r = csv.DictReader(i, delimiter="\t")
        for row in r:
            norm_factor[row['sample']] = row['tic']

    return norm_factor
