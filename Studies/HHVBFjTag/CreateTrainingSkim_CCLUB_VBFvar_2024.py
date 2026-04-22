import ROOT
import numpy as np
import sys
import os
if __name__ == "__main__":
    # Get ANALYSIS_PATH from environment, with fallback to current directory structure
    analysis_path = os.environ.get('ANALYSIS_PATH', '/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw')
    if analysis_path not in sys.path:
        sys.path.append(analysis_path)
import Common.Utilities as Utilities
import Common.ReportTools as ReportTools
import yaml
import glob
import Common.BaselineSelection as Baseline
import AnaProd.HH_bbtautau.baseline as HHBaseline


def createSkim(inFile, outFile, run, period, sample, X_mass, node_index, mpv, version, config, snapshotOptions, apply_vbf_cuts=False):
    # Include necessary headers for ROOT operations
    ROOT.gInterpreter.Declare("""
    #include <ROOT/RVec.hxx>
    #include <ROOT/RDF/RInterface.hxx>
    #include <algorithm>
    #include <numeric>
    #include <vector>
    #include <cmath>
    using namespace ROOT::VecOps;
    
    // Helper function to calculate VBF-specific topological variables for a jet
    struct JetVBFVars {
        float best_vbf_mjj;           // mjj of the best VBF-like pair formed by this jet
        float best_vbf_deltaEta;      // deltaEta of the best VBF-like pair
        float best_vbf_deltaPhi;      // deltaPhi of the best VBF-like pair
        int best_vbf_nCentral;        // nCentralJets of the best VBF-like pair
        int n_vbf_like_pairs;         // Total number of VBF-like pairs this jet can form
        float second_best_mjj;        // mjj of the second best VBF-like pair
        float avg_mjj_all_pairs;      // Average mjj with all other jets
    };
    
    // Implementation of VBF variable calculation function
    JetVBFVars CalculateJetVBFVariables(int target_jet_idx, 
                                       const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& all_jet_p4,
                                       const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& vbf_jet_p4,
                                       const ROOT::VecOps::RVec<int>& vbf_jet_idx) {
        JetVBFVars result;
        result.best_vbf_mjj = -1;
        result.best_vbf_deltaEta = -1;
        result.best_vbf_deltaPhi = -999;
        result.best_vbf_nCentral = -1;
        result.n_vbf_like_pairs = 0;
        result.second_best_mjj = -1;
        result.avg_mjj_all_pairs = -1;
        
        std::vector<float> mjj_values;
        std::vector<float> deltaEta_values;
        std::vector<float> deltaPhi_values;
        std::vector<int> nCentral_values;
        
        // Find target jet in all jets to get its 4-momentum
        ROOT::Math::PtEtaPhiMVector target_jet_p4;
        bool found_target = false;
        for (size_t k = 0; k < all_jet_p4.size(); ++k) {
            if (k == target_jet_idx) {
                target_jet_p4 = all_jet_p4[k];
                found_target = true;
                break;
            }
        }
        
        if (!found_target) return result;
        
        // Loop through VBF candidate jets to form pairs
        for (size_t j = 0; j < vbf_jet_idx.size(); ++j) {
            int other_jet_idx = vbf_jet_idx[j];
            if (other_jet_idx == target_jet_idx) {
                continue;  // Skip same jet
            }
            
            ROOT::Math::PtEtaPhiMVector other_jet_p4 = vbf_jet_p4[j];
            
            // Calculate invariant mass
            float mjj = (target_jet_p4 + other_jet_p4).M();
            mjj_values.push_back(mjj);
            
            // Calculate delta eta and delta phi
            float deltaEta = std::abs(target_jet_p4.Eta() - other_jet_p4.Eta());
            float deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(target_jet_p4, other_jet_p4);
            deltaEta_values.push_back(deltaEta);
            deltaPhi_values.push_back(deltaPhi);
            
            // Count central jets (simplified - count VBF jets between the two in eta)
            int nCentral = 0;
            float eta_min = std::min(target_jet_p4.Eta(), other_jet_p4.Eta());
            float eta_max = std::max(target_jet_p4.Eta(), other_jet_p4.Eta());
            
            for (size_t k = 0; k < vbf_jet_idx.size(); ++k) {
                if (vbf_jet_idx[k] != target_jet_idx && vbf_jet_idx[k] != other_jet_idx) {
                    float jet_eta = vbf_jet_p4[k].Eta();
                    if (jet_eta > eta_min && jet_eta < eta_max && vbf_jet_p4[k].Pt() > 20) {
                        nCentral++;
                    }
                }
            }
            nCentral_values.push_back(nCentral);
            
            // Count VBF-like pairs (mjj > 500 && deltaEta > 2.5)
            if (mjj > 500.0 && deltaEta > 2.5) {
                result.n_vbf_like_pairs++;
            }
        }
        
        if (mjj_values.size() > 0) {
            // Find best pair (highest mjj)
            auto max_it = std::max_element(mjj_values.begin(), mjj_values.end());
            size_t best_idx = std::distance(mjj_values.begin(), max_it);
            
            result.best_vbf_mjj = mjj_values[best_idx];
            result.best_vbf_deltaEta = deltaEta_values[best_idx];
            result.best_vbf_deltaPhi = deltaPhi_values[best_idx];
            result.best_vbf_nCentral = nCentral_values[best_idx];
            
            // Calculate average mjj
            float sum_mjj = std::accumulate(mjj_values.begin(), mjj_values.end(), 0.0f);
            result.avg_mjj_all_pairs = sum_mjj / mjj_values.size();
            
            // Find second best mjj
            if (mjj_values.size() > 1) {
                std::sort(mjj_values.begin(), mjj_values.end(), std::greater<float>());
                result.second_best_mjj = mjj_values[1];
            }
        }
        
        return result;
    }
    
    // Wrapper functions for RDataFrame to extract VBF-specific variables
    ROOT::VecOps::RVec<float> GetJetBestVBFMjj(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                               const ROOT::VecOps::RVec<int>& Jet_idx,
                                               const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                               const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> best_vbf_mjj(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            best_vbf_mjj[i] = vars.best_vbf_mjj;
        }
        return best_vbf_mjj;
    }
    
    ROOT::VecOps::RVec<float> GetJetBestVBFDeltaEta(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                    const ROOT::VecOps::RVec<int>& Jet_idx,
                                                    const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                    const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> best_vbf_deltaEta(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            best_vbf_deltaEta[i] = vars.best_vbf_deltaEta;
        }
        return best_vbf_deltaEta;
    }
    
    ROOT::VecOps::RVec<float> GetJetBestVBFDeltaPhi(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                    const ROOT::VecOps::RVec<int>& Jet_idx,
                                                    const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                    const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> best_vbf_deltaPhi(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            best_vbf_deltaPhi[i] = vars.best_vbf_deltaPhi;
        }
        return best_vbf_deltaPhi;
    }
    
    ROOT::VecOps::RVec<int> GetJetBestVBFNCentral(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                  const ROOT::VecOps::RVec<int>& Jet_idx,
                                                  const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                  const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<int> best_vbf_nCentral(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            best_vbf_nCentral[i] = vars.best_vbf_nCentral;
        }
        return best_vbf_nCentral;
    }
    
    ROOT::VecOps::RVec<int> GetJetNVBFLikePairs(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                               const ROOT::VecOps::RVec<int>& Jet_idx,
                                               const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                               const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<int> n_vbf_like_pairs(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            n_vbf_like_pairs[i] = vars.n_vbf_like_pairs;
        }
        return n_vbf_like_pairs;
    }
    
    ROOT::VecOps::RVec<float> GetJetSecondBestMjj(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                  const ROOT::VecOps::RVec<int>& Jet_idx,
                                                  const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                  const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> second_best_mjj(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            second_best_mjj[i] = vars.second_best_mjj;
        }
        return second_best_mjj;
    }
    
    ROOT::VecOps::RVec<float> GetJetAvgMjj(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                          const ROOT::VecOps::RVec<int>& Jet_idx,
                                          const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                          const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> avg_mjj_all_pairs(Jet_idx.size());
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            auto vars = CalculateJetVBFVariables(i, Jet_p4, VBF_p4, VBF_idx);
            avg_mjj_all_pairs[i] = vars.avg_mjj_all_pairs;
        }
        return avg_mjj_all_pairs;
    }
    
    // Simple, fast-to-calculate variables for real-time inference
    ROOT::VecOps::RVec<float> GetJetDistanceToNearestJet(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                         const ROOT::VecOps::RVec<int>& Jet_idx,
                                                         const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                         const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> distance_to_nearest(Jet_idx.size());
        
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            float min_distance = 999.0;
            ROOT::Math::PtEtaPhiMVector target_jet = Jet_p4[i];
            
            // Find minimum distance to any VBF candidate jet (excluding itself)
            for (size_t j = 0; j < VBF_idx.size(); ++j) {
                if (VBF_idx[j] != i) {  // Don't compare jet to itself
                    float deltaR = ROOT::Math::VectorUtil::DeltaR(target_jet, VBF_p4[j]);
                    if (deltaR < min_distance) {
                        min_distance = deltaR;
                    }
                }
            }
            
            distance_to_nearest[i] = min_distance;
        }
        
        return distance_to_nearest;
    }
    
    ROOT::VecOps::RVec<float> GetJetEtaCentrality(const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& Jet_p4,
                                                  const ROOT::VecOps::RVec<int>& Jet_idx,
                                                  const ROOT::VecOps::RVec<ROOT::Math::PtEtaPhiMVector>& VBF_p4,
                                                  const ROOT::VecOps::RVec<int>& VBF_idx) {
        ROOT::VecOps::RVec<float> eta_centrality(Jet_idx.size());
        
        // Find the eta range of VBF jets
        float min_eta = 999.0;
        float max_eta = -999.0;
        
        for (size_t j = 0; j < VBF_p4.size(); ++j) {
            float eta = VBF_p4[j].Eta();
            if (eta < min_eta) min_eta = eta;
            if (eta > max_eta) max_eta = eta;
        }
        
        // Calculate centrality for each jet
        for (size_t i = 0; i < Jet_idx.size(); ++i) {
            float jet_eta = Jet_p4[i].Eta();
            
            if (max_eta > min_eta) {
                // Centrality = how close to the center of the eta range (0 = at edge, 1 = at center)
                float eta_center = (max_eta + min_eta) / 2.0;
                float eta_range = max_eta - min_eta;
                float distance_from_center = std::abs(jet_eta - eta_center);
                
                // Normalize: 0 = at edge of range, 1 = at center, >1 = outside range
                eta_centrality[i] = 1.0 - (2.0 * distance_from_center / eta_range);
            } else {
                // If all VBF jets have same eta, centrality is based on distance
                eta_centrality[i] = 1.0 / (1.0 + std::abs(jet_eta - min_eta));
            }
        }
        
        return eta_centrality;
    }
    """)
    
    # Variables that exist in the original DataFrame
    jetVar_list_original = ["pt", "eta", "phi", "mass", "btagDeepFlavB", "btagPNetB", "btagPNetQvG", "btagUParTAK4B", "HHbtag"] # "HHBtagScore" excluded for now until I can test the new version for Run3
    
    # Variables that are defined during selection process
    jetVar_list_defined = ["vbfgenMatched", "isCCLUBbjet", "isCCLUBvbfjet"]
    
    # New VBF-specific topological variables for each jet
    # jetVar_list_topological = ["bestVBFMjj", "bestVBFDeltaEta", "bestVBFDeltaPhi", "bestVBFNCentral", "nVBFLikePairs", "secondBestMjj", "avgMjj"]
    
    # Simple variables that are fast to calculate in real-time
    jetVar_list_simple = ["distanceToNearestJet", "etaCentrality"]
       
    # jetVar_list = jetVar_list_original + jetVar_list_defined + jetVar_list_topological + jetVar_list_simple
    jetVar_list = jetVar_list_original + jetVar_list_defined + jetVar_list_simple
    
    def JetSavingCondition(df):
        df = df.Define('Jet_selIdx', 'ReorderObjects(abs(Jet_eta), Jet_idx[Jet_vbfCand_CCLUB])')
        for var in jetVar_list:
            df = df.Define(f"RecoJet_{var}", f"Take(Jet_{var}, Jet_selIdx)")
        return df
    
    genjetVar_list = ["pt","eta","phi","mass"]

    def GenJetSavingCondition(df):
        for genvar in genjetVar_list:
            df = df.Define(f"genjet_{genvar}",f"Take(GenJet_{genvar}, GenJet_idx)")
        return df
    
    lheVar_list = ["status", "pdgId", "pt", "eta", "phi", "mass"]

    Baseline.Initialize(False, False)

    if isinstance(inFile, str):
        inFile = [inFile]

    ROOT.EnableImplicitMT()
    df = ROOT.RDataFrame("Events", Utilities.ListToVector(inFile))
    events_initial = df.Count().GetValue()
    print(f"Initial events: {events_initial}")

    # Initialize baseline framework (same as original script)
    df = Baseline.CreateRecoP4(df)
    df = Baseline.SelectRecoP4(df)
    df = Baseline.DefineGenObjects(df, isHH=True, isVBF=True, Hbb_AK4mass_mpv=mpv)

    # Apply baseline selection (exact copy from original script)
    df = df.Define("sample", f"static_cast<int>(SampleType::{sample})")
    df = df.Define("period", f"static_cast<int>(Period::Run{run}_{period})")
    df = df.Define("X_mass", f"static_cast<int>({X_mass})")
    df = df.Define("node_index", f"static_cast<int>({node_index})")
    df = df.Define("n_GenJet", "GenJet_idx.size()")

    # Apply selection functions
    df = HHBaseline.PassGenAcceptance(df)
    df = HHBaseline.GenJetSelection(df)
    df = HHBaseline.GenVBFJetSelection(df)
    df = HHBaseline.GenJetHttOverlapRemoval(df)
    df = HHBaseline.GenAllOverlapRemoval(df)
    df = HHBaseline.RequestOnlyResolvedGenJets(df)
    # df = HHBaseline.GenRecoTauMatching(df)
    # df = HHBaseline.GenJetMatchingForBjets(df)
    df = HHBaseline.RecoJetSelection_CCLUB(df)
    df = HHBaseline.GenRecoJetMatching_CCLUB(df)
    # Define VBF jet selection threshold
    pT_threshold = 20.0  # Use standard threshold since we're not applying VBF cuts
    df = HHBaseline.RecoVBFJetSelection_CCLUB(df, pT_threshold)
    df = HHBaseline.RecoJetHornsRemoval(df)
    df = HHBaseline.GenRecoVBFJetMatching_CCLUB(df)
    df = HHBaseline.DefineVBFCand_CCLUB(df)
    
    # Define isCCLUBjet
    df = HHBaseline.DefineisCCLUBjet(df)
    df = HHBaseline.DefineisCCLUBvbfjet(df)

    # Define candidate variables (for compatibility)
    df = df.Define("HttCandidate_leg0_pt", "dau1_pt")
    df = df.Define("HttCandidate_leg0_eta", "dau1_eta")
    df = df.Define("HttCandidate_leg0_phi", "dau1_phi")
    df = df.Define("HttCandidate_leg0_mass", "dau1_mass")
    df = df.Define("HttCandidate_leg1_pt", "dau2_pt")
    df = df.Define("HttCandidate_leg1_eta", "dau2_eta")
    df = df.Define("HttCandidate_leg1_phi", "dau2_phi")
    df = df.Define("HttCandidate_leg1_mass", "dau2_mass")

    df = df.Define("HbbCandidate_leg0_pt", "bjet1_pt_nom")
    df = df.Define("HbbCandidate_leg0_eta", "bjet1_eta")
    df = df.Define("HbbCandidate_leg0_phi", "bjet1_phi")
    df = df.Define("HbbCandidate_leg0_mass", "bjet1_mass_nom")
    df = df.Define("HbbCandidate_leg1_pt", "bjet2_pt_nom")
    df = df.Define("HbbCandidate_leg1_eta", "bjet2_eta")
    df = df.Define("HbbCandidate_leg1_phi", "bjet2_phi")
    df = df.Define("HbbCandidate_leg1_mass", "bjet2_mass_nom")

    df = df.Define("VBFCand_leg0_pt", "VBFCand->leg_p4[0].Pt()")
    df = df.Define("VBFCand_leg0_eta", "VBFCand->leg_p4[0].Eta()")
    df = df.Define("VBFCand_leg0_phi", "VBFCand->leg_p4[0].Phi()")
    df = df.Define("VBFCand_leg0_mass", "VBFCand->leg_p4[0].M()")
    df = df.Define("VBFCand_leg1_pt", "VBFCand->leg_p4[1].Pt()")
    df = df.Define("VBFCand_leg1_eta", "VBFCand->leg_p4[1].Eta()") 
    df = df.Define("VBFCand_leg1_phi", "VBFCand->leg_p4[1].Phi()")
    df = df.Define("VBFCand_leg1_mass", "VBFCand->leg_p4[1].M()")

    # Set pT threshold for central jets based on VBF cuts mode
    centralJet_ptThreshold = 30.0 if apply_vbf_cuts else 20.0
 
    # Apply VBF topological variables (original ones, for reference)
    df = HHBaseline.VBFTopologicalVariables_CCLUB(df, centralJet_ptThreshold)

    # Apply VBF topological cuts if requested (for purer sample)
    if apply_vbf_cuts:
        print(f"Applying VBF topological cuts for purer sample...")
        df = HHBaseline.ApplyVBFTopologicalSelection_CCLUB(df, centralJet_ptThreshold)

    # Show statistics after baseline selection
    events_baseline = df.Count().GetValue()
    baseline_efficiency = 100 * events_baseline / events_initial
    
    if apply_vbf_cuts:
        print(f"Baseline selection + VBF cuts: {events_baseline}/{events_initial} events ({baseline_efficiency:.1f}% total efficiency)")
    else:
        print(f"Baseline selection: {events_baseline}/{events_initial} events ({baseline_efficiency:.1f}% efficiency)")

    # NEW: Calculate jet-level VBF-specific topological variables
    print("Calculating jet-level VBF-specific topological variables...")
    
    # Define VBF-specific topological variables for each jet using VBF candidate jets
    # Get VBF candidate jet collections (with pT>20, |eta|<4.7, jetId>=6)
    df = df.Define("Jet_vbfCand_p4", "Take(Jet_p4, Jet_idx[Jet_vbfCand_CCLUB])")
    df = df.Define("Jet_vbfCand_idx", "Jet_idx[Jet_vbfCand_CCLUB]")
    
    # df = df.Define("Jet_bestVBFMjj", "GetJetBestVBFMjj(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_bestVBFDeltaEta", "GetJetBestVBFDeltaEta(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_bestVBFDeltaPhi", "GetJetBestVBFDeltaPhi(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_bestVBFNCentral", "GetJetBestVBFNCentral(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_nVBFLikePairs", "GetJetNVBFLikePairs(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_secondBestMjj", "GetJetSecondBestMjj(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    # df = df.Define("Jet_avgMjj", "GetJetAvgMjj(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    
    # Simple variables for real-time inference (O(N) complexity)
    df = df.Define("Jet_distanceToNearestJet", "GetJetDistanceToNearestJet(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")
    df = df.Define("Jet_etaCentrality", "GetJetEtaCentrality(Jet_p4, Jet_idx, Jet_vbfCand_p4, Jet_vbfCand_idx)")

    # Show final statistics
    events_final = df.Count().GetValue()
    final_efficiency = 100 * events_final / events_initial
    
    if apply_vbf_cuts:
        print(f"Final statistics (baseline + VBF cuts): {events_final}/{events_initial} events ({final_efficiency:.1f}% total efficiency)")
    else:
        print(f"Final statistics: {events_final}/{events_initial} events ({final_efficiency:.1f}% total efficiency)")

    df = df.Define("channel", "pairType")

    df = JetSavingCondition(df)
    df = GenJetSavingCondition(df)

    report = df.Report()
    histReport=ReportTools.SaveReport(report.GetValue())


    colToSave = ["event","luminosityBlock","hasVBFAK4",
                "HttCandidate_leg0_pt", "HttCandidate_leg0_eta", "HttCandidate_leg0_phi", "HttCandidate_leg0_mass", "HttCandidate_leg1_pt", "HttCandidate_leg1_eta", "HttCandidate_leg1_phi","HttCandidate_leg1_mass",
                "HbbCandidate_leg0_pt", "HbbCandidate_leg0_eta", "HbbCandidate_leg0_phi", "HbbCandidate_leg0_mass", "HbbCandidate_leg1_pt", "HbbCandidate_leg1_eta", "HbbCandidate_leg1_phi","HbbCandidate_leg1_mass",
                "VBFCand_leg0_pt", "VBFCand_leg0_eta", "VBFCand_leg0_phi", "VBFCand_leg0_mass", "VBFCand_leg1_pt", "VBFCand_leg1_eta", "VBFCand_leg1_phi","VBFCand_leg1_mass",
                "VBF_mjj", "VBF_deltaEta", "VBF_deltaPhi", "VBF_centrality_htt", "VBF_centrality_hbb", "nJets_central",  # Original VBF variables (for reference)
                "channel","sample", "period", "X_mass", "node_index", "PuppiMET_pt", "PuppiMET_phi"]

    colToSave+=[f"RecoJet_{var}" for var in jetVar_list]
    colToSave+=[f"genjet_{genvar}" for genvar in genjetVar_list]
    colToSave+=[f"LHEPart_{lhevar}" for lhevar in lheVar_list]
    colToSave+=["GenJet_b_PF", "GenJet_Hbb" , "GenJet_idx", "GenJet_eta"]
    colToSave+=["Jet_selIdx", "Jet_idx"]
    colToSave+=["LHEPartVBFJetsIdx", "GenVBFJetsMatch"]

    varToSave = Utilities.ListToVector(colToSave)
    df.Snapshot("Event", outFile, varToSave, snapshotOptions)
    outputRootFile= ROOT.TFile(outFile, "UPDATE")
    outputRootFile.WriteTObject(histReport, "Report", "Overwrite")
    outputRootFile.Close()



if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('--period', type=str)
    parser.add_argument('--run', type=str, default="3")
    parser.add_argument('--input', type=str)
    parser.add_argument('--outFile', type=str)
    parser.add_argument('--X_mass', type=int, default=-1)
    parser.add_argument('--node_index', type=int, default=-1)
    parser.add_argument('--config', required=True, type=str)
    parser.add_argument('--mpv', type=float, default=125)
    parser.add_argument('--version', type=int, default=2)
    parser.add_argument('--sample', type=str)
    parser.add_argument('--compressionLevel', type=int, default=9)
    parser.add_argument('--compressionAlgo', type=str, default="LZMA")
    parser.add_argument('--particleFile', type=str,
                        default=f"{os.environ['ANALYSIS_PATH']}/config/pdg_name_type_charge.txt")
    parser.add_argument('--vbf_cuts', action='store_true', 
                        help='Apply additional VBF topological cuts for purer sample')

    args = parser.parse_args()

    if os.path.isfile(args.input): 
        inFile = [args.input]
    elif os.path.isdir(args.input):  
        inFile = glob.glob(os.path.join(args.input, "*.root"))
    else:
        raise ValueError("Not input file or directory found")

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine(".include "+ os.environ['ANALYSIS_PATH'])
    ROOT.gROOT.ProcessLine('#include "include/GenTools.h"')
    ROOT.gInterpreter.ProcessLine(f"ParticleDB::Initialize(\"{args.particleFile}\");")
    snapshotOptions = ROOT.RDF.RSnapshotOptions()
    snapshotOptions.fOverwriteIfExists=True
    snapshotOptions.fCompressionAlgorithm = getattr(ROOT.ROOT, 'k' + args.compressionAlgo)
    snapshotOptions.fCompressionLevel = args.compressionLevel

    createSkim(inFile, args.outFile, args.run, args.period, args.sample, args.X_mass, args.node_index, args.mpv, args.version, config, snapshotOptions, args.vbf_cuts)