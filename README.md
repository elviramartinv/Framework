# HH -> bbtautau Framework

FLAF - Flexible LAW-based Analysis Framework.
Task workflow managed is done via [LAW](https://github.com/riga/law) (Luigi Analysis Framework).

Documentation is available on [GitHub Pages](https://cms-flaf.github.io/Framework/).


## Run3_prod branch notes:

### example command:

cmsEnv python3 Studies/HHBTag/CreateTrainingSkim.py --inFile /eos/user/j/jmotta/HHbbtautau_Run3/PreprocessRDF/run3_2022_postEE/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p00/cat_base/miniProd_24_06/data_222.root --outFile testFile --mass 125 --sample GluGluToRadion --period 2022EE --config config/global_config.yaml

### pNtuples:
• 2022preEE : /eos/cms/store/group/phys_higgs/HHbbtautau
• 2022postEE : /eos/user/j/jmotta/HHbbtautau_Run3/PreprocessRDF/
• 2023preBPix : /eos/cms/store/group/phys_higgs/HHbbtautau
• 2023postBPix : /eos/home-l/leamaria/miniProdJune2024/
