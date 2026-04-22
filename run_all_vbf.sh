uts#!/bin/bash

# VBF HH->bbtautau Training Skims Generator
# Complete script to generate training skims for all VBF nodes and Run3 periods
# Author: E. Martin
# Date: September 2025

set -e  # Exit on error

# Parse command line arguments
VBF_CUTS=false
TEST_MODE=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --vbf_cuts)
            VBF_CUTS=true
            shift
            ;;
        --test)
            TEST_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--vbf_cuts] [--test]"
            echo "  --vbf_cuts    Apply VBF topological cuts for high-purity sample"
            echo "                (saves to training_skims_highpurity_2909/)"
            echo "  --test        Process only first file for testing"
            echo "  Without --vbf_cuts: saves to training_skims_2909/"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo "Starting VBF training skim generation..."
if [ "$VBF_CUTS" = true ]; then
    echo "Mode: High-purity skims (with VBF topological cuts)"
else
    echo "Mode: Standard skims (without VBF cuts)"
fi
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
if [ "$VBF_CUTS" = true ]; then
    OUTPUT_BASE="/eos/user/e/emartinv/vbfjets_Training/training_skims_highpurity_1310_all_v4"
    OUTPUT_SUFFIX="_highpurity"
else
    OUTPUT_BASE="/eos/user/e/emartinv/vbfjets_Training/training_skims_1310_all_v7_0311"
    OUTPUT_SUFFIX=""
fi

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
    local config="$5"
    local node_index="$6"
    local description="$7"
    
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
    
    # Build command with optional VBF cuts argument
    CMD="$CMSENV_CMD python3 $SCRIPT --input $input_path --outFile $output_file --sample $sample --period $period --config $config --node_index $node_index"
    if [ "$VBF_CUTS" = true ]; then
        CMD="$CMD --vbf_cuts"
    fi
    
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
# OUTPUT_BASE is set above based on VBF_CUTS mode
CONFIG="config/global_config.yaml"
SAMPLE="VBFnonRes"
SCRIPT="Studies/HHVBFjTag/CreateTrainingSkim_CCLUB_VBFvar.py"

# Define all the VBF nodes and their corresponding directory names
declare -A VBF_NODES
VBF_NODES["0"]="qqHH_CV_1_C2V_1_kl_1_hbbhtt"                    # SM Point
VBF_NODES["1"]="qqHH_CV_1_C2V_0_kl_1_hbbhtt"                    # CV=1, C2V=0, kl=1
VBF_NODES["2"]="qqHH_CV_1p74_C2V_1p37_kl_14p4_hbbhtt"           # CV=1.74, C2V=1.37, kl=14.4
VBF_NODES["3"]="qqHH_CV_m0p012_C2V_0p030_kl_10p2_hbbhtt"          # CV=2.12, C2V=3.87, kl=-5.96
VBF_NODES["4"]="qqHH_CV_m0p758_C2V_1p44_kl_m19p3_hbbhtt"        # CV=-0.758, C2V=1.44, kl=-19.3
VBF_NODES["5"]="qqHH_CV_m0p962_C2V_0p959_kl_m1p43_hbbhtt"       # CV=-0.962, C2V=0.959, kl=-1.43
VBF_NODES["6"]="qqHH_CV_m1p21_C2V_1p94_kl_m0p94_hbbhtt"         # CV=-1.21, C2V=1.94, kl=-0.94
VBF_NODES["7"]="qqHH_CV_m1p60_C2V_2p72_kl_m1p36_hbbhtt"         # CV=-1.60, C2V=2.72, kl=-1.36
VBF_NODES["8"]="qqHH_CV_m1p83_C2V_3p57_kl_m3p39_hbbhtt"         # CV=-1.83, C2V=3.57, kl=-3.39

# Define all Run3 periods
PERIODS=("2022:run3_2022_preEE" "2022EE:run3_2022_postEE" "2023:run3_2023_preBPix" "2023BPix:run3_2023_postBPix")

echo ""
echo "================================================================="
echo "Processing all VBF nodes across all Run3 periods"
echo "================================================================="

# Process all combinations of nodes and periods
processed_count=0
for node_idx in "${!VBF_NODES[@]}"; do
    node_dir="${VBF_NODES[$node_idx]}"
    
    echo ""
    echo "================================================================="
    echo "NODE $node_idx"
    echo "================================================================="
    
    for period_info in "${PERIODS[@]}"; do
        # Split period info: period_name:directory_name
        IFS=':' read -r period_name dir_name <<< "$period_info"
        
        # Handle special case for SM point (node 0) - use suffix "SM" instead of number
        if [ "$node_idx" == "0" ]; then
            output_suffix="SM"
        else
            output_suffix="$node_idx"
        fi
        
        # Define input and output paths
        # input_path="${PREPROCESS_BASE}/${dir_name}/${node_dir}/cat_base/Prod_25_09_signalsForVbfjtagTraining/" 
        input_path="${PREPROCESS_BASE}/${dir_name}/${node_dir}/cat_base/VBFjTag_bypass_0310/" 
        output_file="${OUTPUT_BASE}/${period_name}_VBFHHto2B2Tau_${output_suffix}.root"
        
        # Process the sample
        process_sample \
            "$input_path" \
            "$output_file" \
            "$SAMPLE" \
            "$period_name" \
            "$CONFIG" \
            "$node_idx" \
            "Node $node_idx - Run3 $period_name"
        
        processed_count=$((processed_count + 1))
        
        # If in test mode, only process first file
        if [ "$TEST_MODE" = true ]; then
            echo ""
            echo "TEST MODE: Stopping after first file"
            break 2
        fi
    done
done

echo ""
echo "================================================================="
if [ "$VBF_CUTS" = true ]; then
    echo "VBF High-Purity Training Skim Generation Completed Successfully!"
else
    echo "VBF Training Skim Generation Completed Successfully!"
fi
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