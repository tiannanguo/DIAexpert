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
    raw_to_sample_id = {}
    sample_id_to_name = {}

    with open(id_mapping_file) as i:
        reader = csv.DictReader(i, delimiter="\t")
        for row in reader:
            sample_id.append(row['sample_ID'])
            raw_to_sample_id[row['raw_file_name'].lower()] = row['sample_ID']
            sample_id_to_name[row['sample_ID'].lower()] = row['sample_name']

    return sample_id, raw_to_sample_id, sample_id_to_name


def read_com_chrom_file(chrom_file, sample_id, normalization_factors):

    ref_sample_data = {}
    chrom_data = data_holder.NestedDict()
    peptide_data = data_holder.NestedDict()

    # sometimes, in the golden standard data set, multiple "best_sample"s are found. The best in water may not be the best in human
    # in this case, check the input file and write to a new file
    # select the best sample with lowest m_score
    # sometimes, there are too many NA values. remove tg with >50% missing values.

    with gzip.open(chrom_file, 'rb') as i:

        r = csv.DictReader(i, delimiter="\t")

        # get the list of unique transition groups
        tg_list = get_tg_list(r)

        # re-iterate the chrom file
        i.seek(0)
        next(r)

        # get the best sample for each tg
        best_sample, best_score, best_rt = get_best_sample_for_each_tg(i, r, tg_list)

        # re-iterate the chrom file
        i.seek(0)
        next(r)

        # data process
        for row in r:
            tg = row['transition_group_id']
            fragment = row['transition_name']
            tg = row['transition_group_id']

            # correct the best sample if necessary
            peak_rt = float(best_rt[tg])
            ref_sample_name = best_sample[tg]
            ref_sample_score = float(best_score[tg])

            ref_sample_data[tg] = data_holder.ReferenceSample(
                ref_sample_name, ref_sample_score, peak_rt)

            peptide_data[tg]['ms1']['preMz'] = float(row['precursor_mz'])
            peptide_data[tg]['ms1']['protein'] = row['protein']
            peptide_data[tg]['ms1']['irt'] = float(row['irt'])

            peptide_data[tg]['ms2'][fragment] = float(row['transition_mz'])

            for k in sample_id:
                rt_list_three_values_csv = row[k + '_rt']
                i_list_csv = row[k + '_i']
                i_list_csv = apply_normalization_based_on_tic(i_list_csv, normalization_factors, k)

                ########### only for debugging purpose
                # if k == 'gold80' and fragment.startswith('1191_'):
                #     pass

                chrom_data[tg][k][fragment] = data_holder.Chromatogram(
                    rt_list_three_values_csv, i_list_csv)

    ########### only for debugging purpose
    # print chrom_data

    return ref_sample_data, chrom_data, peptide_data


def get_tg_list(reader):
    tg_list = {}
    for row in reader:
        perc_nonNA = get_percentage_of_non_NA_values(row)
        # print perc_nonNA
        if perc_nonNA < 0.5:
            tg_list[row['transition_group_id']] = 1
    return tg_list.keys()



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


def get_percentage_of_non_NA_values(row):

    num_total = len(row)
    num_total *= 1.0
    num_others = 10.0
    num_NA = 0
    for key_string, value in row.iteritems():
        if value == 'NA':
            num_NA += 1
    num_NA *= 1.0
    perc = num_NA / (num_total - num_others)

    # print row['transition_group_id'], num_NA, num_total, num_others, perc
    return perc


def get_best_sample_for_each_tg(i, reader, tg_list):

    best_sample = {}
    best_score = {}
    best_rt = {}

    for tg in tg_list:
        best_sample[tg] = ''
        best_score[tg] = 1.0
        best_rt[tg] = -1.0

        for row in reader:
            tg2 = row['transition_group_id']
            if tg2 == tg and float(row['best_score']) < float(best_score[tg]):
                best_sample[tg] = row['best_sample']
                best_rt[tg] = row['best_rt']
                best_score[tg] = float(row['best_score'])
        i.seek(0)
        next(reader)

    return best_sample, best_score, best_rt

def read_tic_normalization_file(tic_normalization_file):

    norm_factor = {}

    with open(tic_normalization_file, 'rb') as i:
        r = csv.DictReader(i, delimiter="\t")
        for row in r:
            norm_factor[row['sample_ID']] = row['tic']

    return norm_factor
