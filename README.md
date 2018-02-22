Input files:

1. SWATH/DIA mappingfile: eg, pppa1005.txt 
2. SWATH/DIA mzXML file: pppa696.mzXML.gz: the format of the file is sampleN.mzXML.gz，sampleN refers to the second column of the mapping file;
3. SWATH/DIA window file: 100swaths-variable.txt
4. Library file 1: 422dda_sp_sv_tr_addDecoy.TraML，for the -tr of the command OpenSwathWorkflow;
5. Library file 2: iRT_library.TraML，for the -tr_irt of the command OpenSwathWorkflo;
6. Library file 3”: cons_irt_sp.sptxt, the spectrast file of the library containing all fragments. 


Commands:

1.	OpenSwathWorkflow -min_upper_edge_dist 1 -mz_extraction_window 0.05 -rt_extraction_window 600 -extra_rt_extraction_window 100 -min_rsq 0.8 -min_coverage 0.7 -use_ms1_traces -Scoring:stop_report_after_feature 5 -tr_irt /data/swathcode/iRT_library.TraML -tr /data/swathcode/422dda_sp_sv_tr_addDecoy.TraML -threads 4 -readOptions cache -tempDirectory /data/tmp/swath -in /data/swathcode/pppa696.mzXML.gz -out_tsv /data/swathcode/pppa696_allFrag.tsv
INPUT: 422dda_sp_sv_tr_addDecoy.TraML, iRT_library.TraML,  pppa696.mzXML.gz
OUTPUT: pppa696_allFrag.tsv
2.	mProphetScoreSelector.sh /data/swathcode/pppa696_allFrag.tsv xx_swath_prelim_score library_corr yseries_score xcorr_coelution_weighted massdev_score norm_rt_score library_rmsd bseries_score intensity_score xcorr_coelution log_sn_score isotope_overlap_score massdev_score_weighted xcorr_shape_weighted isotope_correlation_score xcorr_shape
INPUT: pppa696_allFrag.tsv
OUTPUT: pppa696_allFrag.tsv
3.	pyprophet --ignore.invalid_score_columns --target.dir=/data/swathcode/pyprophet.results  --xeval.num_iter=10 --d_score.cutoff=0.01 /data/swathcode/pppa696_allFrag.tsv
INPUT: pppa696_allFrag.tsv
OUTPUT: pppa696_allFrag_with_dscore_filtered.csv in --target.dir
4.	spectrast2tsv.py -l 400,2000 -s a,b,y -x 1,2,3 -o 6 -n 100 -p 0.05 -e -w /data/100swaths-variable.txt -k openswath -a spectrast2tsv_output.tsv /data/swathcode/cons_irt_sp.sptxt
INPUT: 100swaths-variable.txt, cons_irt_sp.sptxt
OUTPUT: spectrast2tsv_output.tsv
5.	generate_ref_sample.py -csv_dir pyprophet.results/ --out test_ref_2.tsv --m_score_th 0.01
INPUT: pyprophet.results （a folder containing all *_with_dscore_filtered.csv files from pyprophet）
OUTPUT: test_ref_2.tsv
Note: Perform this step only after all the pyprophet analyses are completed. 
6.	select_library.pl test_ref_2.tsv spectrast2tsv_output.tsv library_selected.tsv
INPUT: test_ref_2.tsv, spectrast2tsv_output.tsv
Output: library_selected.tsv
7.	OpenSwathWorkflow -min_upper_edge_dist 1 -mz_extraction_window 0.05 -rt_extraction_window 600 -extra_rt_extraction_window 100 -min_rsq 0.8 -min_coverage 0.7 -use_ms1_traces -Scoring:stop_report_after_feature 5 -tr_irt /data/swathcode/iRT_library.TraML -tr /data/swathcode/library_selected.tsv -threads 8 -readOptions cache -tempDirectory /data/tmp/swath -in /data/swathcode/pppa696.mzXML.gz -out_tsv /data/swathcode/pppa696_allFrag_2.tsv -out_chrom /data/swathcode/pppa696_allFrag_2.chrom.mzML
INPUT: library_selected.tsv,  iRT_library.TraML
OUTPUT: pppa696_allFrag_2.tsv,  pppa696_allFrag_2.chrom.mzML
8.	gzip pppa696_allFrag_2.chrom.mzML  
INPUT: pppa696_allFrag_2.chrom.mzML
OUTPUT: pppa696_allFrag_2.chrom.mzML.gz
9.	parse_chrom_mzML.py test_ref_2.tsv pppa696_allFrag_2.chrom.mzML.gz library_selected.tsv pppa696_allFrag_2.chrom.txt.gz ../pppa1005.txt
INPUT: test_ref_2.tsv , pppa696_allFrag_2.chrom.mzML.gz,  library_selected.tsv, pppa1005.txt
OUTPUT: pppa696_allFrag_2.chrom.txt
10.	split_chrom_txt.pl pppa696_allFrag.chrom.txt.gz test_ref_2.tsv 10
INPUT: pppa696_allFrag.chrom.txt.gz  test_ref_2.tsv
OUTPUT: pppa696_allFrag_part\[1-10].chrom.txt.gz 10 files part1~part10
11.	combine_chrom_txt_perl_new.pl pppa1005.txt pppa1_allFrag_part${i}.chrom.txt.gz
INPUT: pppa1005.txt and  1005 part${i} files
OUTPUT: a part${i} file 
12.	generate_tic.py --map_file pppa1005.txt --file_dir path_to_mzXML_gz_directory --out output_file_path
INPUT: 
1. The directory containing all .mzXML.gz files;
13.	Mapping file
OUTPUT: tic file
14.	dia_expert.py
INPUT: TIC file
