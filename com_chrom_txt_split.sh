bsub -R "rusage[mem=2000]" "python split_big_com_chrom_files.py com_chrom_ncir20b_part1.txt.gz"
bsub -R "rusage[mem=2000]" "python split_big_com_chrom_files.py com_chrom_ncir20b_part2.txt.gz"
bsub -R "rusage[mem=2000]" "python split_big_com_chrom_files.py com_chrom_ncir20b_part3.txt.gz"
bsub -R "rusage[mem=2000]" "python split_big_com_chrom_files.py com_chrom_ncir20b_part4.txt.gz"
bsub -R "rusage[mem=2000]" "python split_big_com_chrom_files.py com_chrom_ncir20b_part5.txt.gz"

#for i in {1..5}; do python split_big_com_chrom_files.py com_chrom_ncir20b_part${i}.txt.gz; done
