uts#!/bin/bash

# VBF HH->bbtautau Training Skims Generator
# Complete script to generate training skims for all VBF nodes and Run3 periods
# Author: E. Martin
# Date: September 2025

set -e  # Exit on error


echo "Loading environment..."

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load the environment
echo "Sourcing env.sh from: ${SCRIPT_DIR}"
source "${SCRIPT_DIR}/env.sh"

# Set up cmsEnv (it's an alias, so we need to define it explicitly)
CMSENV_CMD='env -i HOME=/afs/cern.ch/user/e/emartinv ANALYSIS_PATH=/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw ANALYSIS_DATA_PATH=/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/data X509_USER_PROXY=/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/data/voms.proxy CENTRAL_STORAGE= ANALYSIS_BIG_DATA_PATH= DEFAULT_CMSSW_BASE=/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/soft/CMSSW_14_0_8 DEFAULT_CMSSW_ARCH=el9_amd64_gcc12 /afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/RunKit/cmsEnv.sh'

# Verify that the cmsEnv script exists
if [ ! -f "/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/RunKit/cmsEnv.sh" ]; then
    echo "ERROR: cmsEnv.sh script not found at expected location"
    echo "Expected: /afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/RunKit/cmsEnv.sh"
    exit 1
fi

# Set output directory based on VBF cuts mode
OUTPUT_BASE="/eos/user/e/emartinv/HHBtag_Training/training_skims_Run3_2024_2110"
OUTPUT_SUFFIX=""


echo "Environment loaded successfully!"
echo "cmsEnv script found at: /afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/RunKit/cmsEnv.sh"
echo "Python found at: $(which python3)"
echo "Current conda environment: ${CONDA_DEFAULT_ENV:-'none'}"
echo "Output directory: ${OUTPUT_BASE}/"

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_BASE}/"

# Function to validate ROOT file integrity
validate_root_file() {
    local file="$1"
    
    echo "    -> Validating: $(basename $file)"
    
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "    -> File does not exist"
        return 1
    fi
    
    # Check if file has non-zero size
    local size=$(stat -c%s "$file" 2>/dev/null || echo 0)
    echo "    -> File size: $size bytes"
    if [ "$size" -eq 0 ]; then
        echo "    -> File is empty"
        return 1
    fi
    
    # Check ROOT file integrity using the same environment as processing
    local validation_result
    validation_result=$($CMSENV_CMD python3 -c "
import ROOT
import sys
try:
    f = ROOT.TFile.Open('$file', 'READ')
    if not f:
        print('ERROR: Cannot open file')
        sys.exit(1)
    if f.IsZombie():
        print('ERROR: File is in zombie state')
        f.Close()
        sys.exit(1)
    
    # Check if file has expected tree structure
    tree = f.Get('Event')
    if not tree:
        print('ERROR: No Event tree found')
        f.Close()
        sys.exit(1)
    
    entries = tree.GetEntries()
    f.Close()
    
    if entries <= 0:
        print('ERROR: Event tree is empty')
        sys.exit(1)
    
    print(f'Valid ROOT file: {entries} entries')
    sys.exit(0)
except Exception as e:
    print(f'ERROR: {str(e)}')
    sys.exit(1)
" 2>&1)
    
    local exit_code=$?
    echo "    -> Validation result: $validation_result"
    
    return $exit_code
}

# Function to process a sample with robust validation
process_sample() {
    local input_path="$1"
    local output_file="$2" 
    local sample="$3"
    local period="$4"
    local node_index="$5"
    local description="$6"

    echo "Processing $description..."
    echo "  -> Input: $input_path"
    echo "  -> Output: $output_file"
    
    # Check if valid output already exists
    echo "  -> Checking if valid output exists..."
    if validate_root_file "$output_file"; then
        echo "  -> ✓ Valid output file already exists, skipping: $(basename $output_file)"
        return 0
    elif [ -f "$output_file" ]; then
        echo "  -> ⚠ File exists but validation failed, removing: $(basename $output_file)"
        rm -f "$output_file"
    else
        echo "  -> File does not exist, proceeding with processing"
    fi
    
    CMD="$CMSENV_CMD python3 $SCRIPT --input $input_path --outFile $output_file --sample $sample --period $period --node_index $node_index"

    
    echo ""
    echo "  -> Executing command:"
    echo "     $CMD"
    echo ""
    
    $CMD
    
    if [ $? -eq 0 ]; then
        # Validate the output file after processing
        if validate_root_file "$output_file"; then
            echo "  -> Completed successfully: $(basename $output_file)"
            return 0
        else
            echo "  -> ERROR: Output file is corrupted or empty: $(basename $output_file)"
            rm -f "$output_file"
            return 1
        fi
    else
        echo "  -> ERROR during processing: $(basename $output_file)"
        # Clean up potentially corrupted output
        [ -f "$output_file" ] && rm -f "$output_file"
        return 1
    fi
}

# Define base paths
# PREPROCESS_BASE="/eos/cms/store/group/phys_higgs/HHbbtautau/PreprocessRDF"
PREPROCESS_BASE="/eos/user/e/emartinv/cmt/PreprocessRDF"
SCRIPT="Studies/HHBTag/CreateTrainingSkim_CCLUB.py"

# Define nodos para qqHH
declare -A QQHH_NODES
QQHH_NODES["0"]="qqHH_CV_1_C2V_1_kl_1_hbbhtt"
QQHH_NODES["1"]="qqHH_CV_1_C2V_0_kl_1_hbbhtt"
QQHH_NODES["2"]="qqHH_CV_1p74_C2V_1p37_kl_14p4_hbbhtt"
QQHH_NODES["3"]="qqHH_CV_m0p012_C2V_0p030_kl_10p2_hbbhtt"
QQHH_NODES["4"]="qqHH_CV_m0p758_C2V_1p44_kl_m19p3_hbbhtt"
QQHH_NODES["5"]="qqHH_CV_m0p962_C2V_0p959_kl_m1p43_hbbhtt"
QQHH_NODES["6"]="qqHH_CV_m1p21_C2V_1p94_kl_m0p94_hbbhtt"
QQHH_NODES["7"]="qqHH_CV_m1p60_C2V_2p72_kl_m1p36_hbbhtt"
QQHH_NODES["8"]="qqHH_CV_m1p83_C2V_3p57_kl_m3p39_hbbhtt"
QQHH_NODES["9"]="qqHH_CV_2p12_C2V_3p87_kl_m5p96_hbbhtt"

# Define nodos para ggHH
declare -A GGHH_NODES
GGHH_NODES["0"]="ggHH_kl_1_kt_1_c2_0_hbbhtt"
GGHH_NODES["13"]="ggHH_kl_0_kt_1_c2_0_hbbhtt"
GGHH_NODES["14"]="ggHH_kl_0_kt_1_c2_1_hbbhtt"
GGHH_NODES["15"]="ggHH_kl_1_kt_1_c2_0p10_hbbhtt"
GGHH_NODES["16"]="ggHH_kl_1_kt_1_c2_0p35_hbbhtt"
GGHH_NODES["17"]="ggHH_kl_1_kt_1_c2_3_hbbhtt"
GGHH_NODES["18"]="ggHH_kl_1_kt_1_c2_m2_hbbhtt"
GGHH_NODES["6"]="ggHH_kl_2p45_kt_1_c2_0_hbbhtt"
GGHH_NODES["7"]="ggHH_kl_5_kt_1_c2_0_hbbhtt"

# Define all Run3 periods
PERIODS=("2024:run3_2024_fullYear")

echo ""
echo "================================================================="
echo "Processing all 2024 signal samples"
echo "================================================================="

# Process all combinations of nodes and periods
for node_idx in "${!QQHH_NODES[@]}"; do
    node_dir="${QQHH_NODES[$node_idx]}"
    SAMPLE="VBFnonRes"
    OUTPUT_TAG="VBFHHto2B2Tau"

    for period_info in "${PERIODS[@]}"; do
        IFS=':' read -r period_name dir_name <<< "$period_info"
        output_suffix=$node_idx
        input_path="${PREPROCESS_BASE}/${dir_name}/${node_dir}/cat_base/signals_forHHBTag/"
        output_file="${OUTPUT_BASE}/${period_name}_${OUTPUT_TAG}_${output_suffix}.root"

        process_sample \
            "$input_path" \
            "$output_file" \
            "$SAMPLE" \
            "$period_name" \
            "$node_idx" \
            "qqHH Node $node_idx - Run3 $period_name"
    done
done

# Procesar nodos ggHH
for node_idx in "${!GGHH_NODES[@]}"; do
    node_dir="${GGHH_NODES[$node_idx]}"
    SAMPLE="HHnonRes"
    OUTPUT_TAG="ggHHto2B2Tau"

    for period_info in "${PERIODS[@]}"; do
        IFS=':' read -r period_name dir_name <<< "$period_info"
        output_suffix=$node_idx
        input_path="${PREPROCESS_BASE}/${dir_name}/${node_dir}/cat_base/signals_forHHBTag/"
        output_file="${OUTPUT_BASE}/${period_name}_${OUTPUT_TAG}_${output_suffix}.root"

        process_sample \
            "$input_path" \
            "$output_file" \
            "$SAMPLE" \
            "$period_name" \
            "$node_idx" \
            "ggHH Node $node_idx - Run3 $period_name"
    done
done

echo ""
echo "================================================================="
echo "Output files located in: ${OUTPUT_BASE}/"
TOTAL_FILES=$(ls ${OUTPUT_BASE}/*.root 2>/dev/null | wc -l)
EXPECTED_FILES=40  # 10 nodes × 4 periods = 40 files (node 0 is SM, nodes 1-9 are BSM)
echo "Total files found: ${TOTAL_FILES}/${EXPECTED_FILES}"

if [ "$TOTAL_FILES" -eq "$EXPECTED_FILES" ]; then
    echo "✓ All expected files are present!"
else
    echo "⚠ Some files may be missing. Check the output above for any errors."
fi

echo ""
echo "File list:"
ls -lh ${OUTPUT_BASE}/*.root 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'