#!/usr/bin/python

import sys

if __name__ == "__main__":
    origin_library = sys.argv[1]
    fixed_library = sys.argv[2]

    fin = open(origin_library, 'r')
    fout = open(fixed_library, 'w')

    line = fin.readline()
    fout.write(line)

    fields = line.strip().split('\t')

    peptide_group_label_pos = 0
    transition_group_id_pos = 0
    Charge_pos = 0
    aggr_Fragment_Annotation_pos = 0

    for i in range(len(fields)):
        f = fields[i]
        if f == "peptide_group_label":
            peptide_group_label_pos = i
        elif f == "transition_group_id":
            transition_group_id_pos = i
        elif f == "Charge":
            Charge_pos = i
        elif f == "aggr_Fragment_Annotation":
            aggr_Fragment_Annotation_pos = i

    for line in fin:
        values = line.strip().split('\t')
        append = "_" + values[Charge_pos]
        values[peptide_group_label_pos] = values[peptide_group_label_pos] + append
        values[transition_group_id_pos] = values[transition_group_id_pos] + append

        aa = values[aggr_Fragment_Annotation_pos].split(';')
        values[aggr_Fragment_Annotation_pos] = ';'.join([a + append for a in aa])

        fout.write('\t'.join(values) + '\n')

    fin.close()
    fout.close()
