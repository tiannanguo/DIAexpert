Input files:
test data could be download at http://www.guomics.org/dia-expert/data/wlym_test_data.7z

1. SWATH/DIA mappingfile: eg, wlym113.txt 
2. SWATH/DIA mzXML file: wlym5.mzXML.gz: the format of the file is sampleN.mzXML.gz，sampleN refers to the second column of the mapping file;
3. SWATH/DIA window file: 100swaths-variable.txt
4. Library file 1: 422dda_sp_sv_tr_addDecoy.TraML，for the -tr of the command OpenSwathWorkflow;
5. Library file 2: iRT_library.TraML，for the -tr_irt of the command OpenSwathWorkflo;
6. Library file 3”: cons_irt_sp.sptxt, the spectrast file of the library containing all fragments. 


Commands:

1.	OpenSwathWorkflow -min_upper_edge_dist 1 -mz_extraction_window 0.05 -rt_extraction_window 600 -extra_rt_extraction_window 100 -min_rsq 0.8 -min_coverage 0.7 -use_ms1_traces -Scoring:stop_report_after_feature 5 -tr_irt ../iRT_library.TraML -tr ../phl004_canonical_s64_osw_decoys.TraML -threads 10 -readOptions cache -tempDirectory ../temp/ -in ../wlym5.mzXML.gz -out_tsv ../wlym5_allFrag.tsv
2.	mProphetScoreSelector.sh wlym5_allFrag.tsv xx_swath_prelim_score library_corr yseries_score xcorr_coelution_weighted massdev_score norm_rt_score library_rmsd bseries_score intensity_score xcorr_coelution log_sn_score isotope_overlap_score massdev_score_weighted xcorr_shape_weighted isotope_correlation_score xcorr_shape
3.	pyprophet --ignore.invalid_score_columns --target.dir=2_pyprophet/  --xeval.num_iter=10 --d_score.cutoff=0.01 wlym5_allFrag.tsv
4.	spectrast2tsv.py -l 400,2000 -s a,b,y -x 1,2,3 -o 6 -n 100 -p 0.05 -e -w 100swaths-variable.txt -k openswath -a spectrast2tsv_output.tsv phl004_consensus.sptxt
5.	generate_ref_sample.py --csv_dir 2_pyprophet --out 5_ref_sample/wlym28_5.tsv --m_score_th 0.01
6.	select_library.pl 5_ref_sample/wlym28_5.tsv spectrast2tsv_output.tsv library_selected.tsv
7.	OpenSwathWorkflow -min_upper_edge_dist 1 -mz_extraction_window 0.05 -rt_extraction_window 600 -extra_rt_extraction_window 100 -min_rsq 0.8 -min_coverage 0.7 -use_ms1_traces -Scoring:stop_report_after_feature 5 -tr_irt iRT_library.TraML -tr library_selected.tsv  -threads 20 -readOptions cache -tempDirectory 7_openswath/temp/ -in wlym5.mzXML.gz -out_tsv wlym5_allFrag_2.tsv -out_chrom wlym5_allFrag_2.chrom.mzML
8.	gzip  wlym5_allFrag_2.chrom.mzML
9.	parse_chrom_mzML.py 5_ref_sample/wlym28_5.tsv wlym5_allFrag_2.chrom.mzML.gz library_selected.tsv wlym5_allFrag_2.chrom.txt.gz wlym113.txt
10.	split_chrom_txt.pl wlym5_allFrag_2.chrom.txt.gz  5_ref_sample/wlym28_5.tsv 10
11.	combine_chrom_txt_perl_new.pl wlym113.txt wlym5_allFrag_2_part1.chrom.txt
12.	generate_tic.py --map_file wlym113.txt --file_dir ./ --out 12_generate_tic/normalization3.tic
13.	dia_expert.py --chrom_file com_chrom_wlym5_part1.txt --map_file wlym113.txt --tic_file 12_generate_tic/normalization3.tic

#docker version (optional)
1. docker login  # login the account on http://cloud.docker.com
2. docker pull xihuswath/xihu_swath  # pull the image
3. mkdir swath_data
4. copy all data files into swath_data
5. cd swath_data
6. sudo docker run -v `pwd`:/swath/mnt -i -t --rm xihuswath/xihu_swath bash
   (now you are in the docker container)
7. edit config file (../program/script/swath_batch_run.config) if needed
8. swath_batch_run.sh  # specify input files using the arguments

e.g.
swath_batch_run.sh --config_file ./swath_batch_run.config --sample_name wlym --tr ./phl004_canonical_s64_osw_decoys.TraML --tr_irt ./iRT_library.TraML --win_file ./100swaths-variable.txt --splib ./phl004_consensus.sptxt --map_file ./wlym113.txt
note:  swath_batch_run.config is a configure file contains user specified parameters with OpenSwathWorkflow，pyprophet，spectrast2tsv and generate_ref_sample.py
