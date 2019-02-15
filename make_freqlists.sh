#PROCESS COCA FILES
python3 read_lemmas_by_pos_dir.py ../data/COCA/Word_lemma_PoS/ cocatopnfreqs/ 12000
python3 read_lemmas_by_pos_dir.py ../data/COCA/Word_lemma_PoS/ cocatopnfreqs/ 1042
python3 read_lemmas_by_pos_dir.py ../data/COCA/Word_lemma_PoS/ cocatopnfreqs/ 500
python3 read_lemmas_by_pos_dir.py ../data/COCA/Word_lemma_PoS/ cocatopnfreqs/ 100

#PROCESS CHILDES FILES
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brown/ cocatopnfreqs/wlp_cds_brown_top12000.txt --pos v part aux --rankcutoff 12000
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brown/ cocatopnfreqs/wlp_cds_brown_top1042.txt --pos v part aux --rankcutoff 1042
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brown/ cocatopnfreqs/wlp_cds_brown_top500.txt --pos v part aux --rankcutoff 500
##python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brown/ cocatopnfreqs/wlp_cds_brown_top350.txt --pos v part aux --rankcutoff 350
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brown/ cocatopnfreqs/wlp_cds_brown_top100.txt --pos v part aux --rankcutoff 100
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top12000.txt --pos v part aux --rankcutoff 12000
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top1042.txt --pos v part aux --rankcutoff 1042
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top500.txt --pos v part aux --rankcutoff 500
##python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top350.txt --pos v part aux --rankcutoff 350
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top100.txt --pos v part aux --rankcutoff 100
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/MacWhinney/ cocatopnfreqs/wlp_cds_macwhinney_top12000.txt --pos v part aux --rankcutoff 12000
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/MacWhinney/ cocatopnfreqs/wlp_cds_macwhinney_top1042.txt --pos v part aux --rankcutoff 1042
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/Brent/ cocatopnfreqs/wlp_cds_brent_top500.txt --pos v part aux --rankcutoff 500
##python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/MacWhinney/ cocatopnfreqs/wlp_cds_macwhinney_top350.txt --pos v part aux --rankcutoff 350
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/MacWhinney/ cocatopnfreqs/wlp_cds_macwhinney_top100.txt --pos v part aux --rankcutoff 100

#SAMPLE CHILDES AND COCA
python3 read_lemmas_sample.py ../data/COCA/Word_lemma_PoS/ cocasamples/ 1000 100 250 500 750 1000 sample_adult
#python3 read_lemmas_CHILDES_by_dir.py ../data/CHILDES/English/ outputs/wlp_cds_all_top12000.txt --pos v part aux --rankcutoff 12000
#python3 sample_CHILDES.py outputs/wlp_cds_all_top12000.txt cocasamples/ 1000 100 250 500 750 1000 sample_cds
#./make_ing.sh

python3 compare_lexicons.py cocatopnfreqs/ outputs/similarities.txt acad fic mag news spok cds 100,500,1042,12000

echo "STRONG VERBS"
python3 compare_features.py cocatopnfreqs/ outputs/strongverbs.txt propertylists/strongverbs.txt acad fic mag news spok cds 100,500,1042,12000

echo ""
echo "LATINATE"
python3 compare_features.py cocatopnfreqs/ outputs/latinate.txt propertylists/latinate.txt acad fic mag news spok cds 100,500,1042,12000

echo ""
echo "DOUBLE OBJECT"
python3 compare_features.py cocatopnfreqs/ outputs/doubleobj.txt propertylists/doubleobj.txt acad fic mag news spok cds 100,500,1042,12000

echo ""
echo "IRREGULAR VERBS"
python3 compare_features.py cocatopnfreqs/ outputs/irregularverbs.txt propertylists/irregularverbs.txt acad fic mag news spok cds 100,500,1042,12000

echo ""
echo "IRREGULAR VERBS - SAMPLED LEXICONS"
python3 compare_features.py cocasamples/ outputs/irregularverbs_sampled.txt propertylists/irregularverbs.txt cds adult 100,250,500,750,1000

echo ""
echo "SINGSANG"
python3 compare_features.py singsang/ outputs/singsang_sampled.txt propertylists/notsingsang.txt cds adult 100,250,500,750,1000
