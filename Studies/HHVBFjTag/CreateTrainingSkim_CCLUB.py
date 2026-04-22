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


def createSkim(inFile, outFile, run, period, sample, X_mass, node_index, mpv, version, config, snapshotOptions, apply_vbf_cuts=False, jet_selection="all"):
    # Include necessary headers for ROOT operations
    ROOT.gInterpreter.Declare("""
    #include <ROOT/RVec.hxx>
    #include <ROOT/RDF/RInterface.hxx>
    using namespace ROOT::VecOps;
    """)
    
    # Variables that exist in the original DataFrame
    jetVar_list_original = ["pt", "eta", "phi", "mass", "btagDeepFlavB", "btagPNetB", "btagPNetQvG", "HHbtag"] # "HHBtagScore" excluded for now until I can test the new version for Run3
    
    # Variables that are defined during selection process
    jetVar_list_defined = ["vbfgenMatched", "isCCLUBbjet", "isCCLUBvbfjet"]
       
    jetVar_list = jetVar_list_original + jetVar_list_defined
    
    def JetSavingCondition(df, jet_selection_mode):
        # Define jet selection strategies
        if jet_selection_mode == "all":
            # Both b-candidate and VBF candidate jets
            df = df.Define('Jet_selIdx', '''ReorderObjects(abs(Jet_eta), 
                Jet_idx[(Jet_bCand_CCLUB || Jet_vbfCand_CCLUB)])''')
        elif jet_selection_mode == "vbf_only":
            # Only VBF candidate jets
            df = df.Define('Jet_selIdx', 'ReorderObjects(abs(Jet_eta), Jet_idx[Jet_vbfCand_CCLUB])')
        else:
            raise ValueError(f"Unknown jet_selection mode: {jet_selection_mode}. Use 'all' or 'vbf_only'")
        
        # Apply the selection to all jet variables
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

    df = ROOT.RDataFrame("Events", inFile)
    events_initial = df.Count().GetValue()
    print(f"Initial events in file: {events_initial}")
    print(f"Jet selection mode: {jet_selection}")
    
    # Print jet selection info
    jet_selection_descriptions = {
        "all": "Both b-candidate and VBF candidate jets with pT > 20",
        "vbf_only": "Only VBF candidate jets"
    }
    print(f"  -> {jet_selection_descriptions.get(jet_selection, 'Unknown selection')}")
    # df = df.Range(100)
    df = Baseline.CreateRecoP4(df)
    df = Baseline.SelectRecoP4(df)
    df = Baseline.DefineGenObjects(df, isHH=True, isVBF=True, Hbb_AK4mass_mpv=mpv)

    # df = HHBaseline.RecoJetInvMass(df)

    df = df.Define("n_GenJet", "GenJet_idx.size()")
    
    # print("Eventos inicial", df.Count().GetValue())
    df = HHBaseline.PassGenAcceptance(df) # candidate Htt pT > 20 and eta < 2.3
    # print("Eventos despues de PassGenAcceptance", df.Count().GetValue()) 
    df = HHBaseline.GenJetSelection(df) # Jets selected from Hbb pt > 20 and eta < 2.5 & b-parton matching from Higgs
    # print("Eventos despues de GenJetSelection", df.Count().GetValue())
    df = HHBaseline.GenVBFJetSelection(df) # Jets from VBF quarks pt > 20 & eta < 4.7 & VBF quark matching from LHE particles (applied before overlap removal)
    # print("Eventos despues de GenVBFJetSelection", df.Count().GetValue())
    df = HHBaseline.GenAllOverlapRemoval(df) # Overlap removal between GenJets, GenTaus and GenVBFJets
    # print("Eventos despues de GenJetVBFOverlapRemoval", df.Count().GetValue())
    df = HHBaseline.RequestOnlyResolvedGenJets(df) # Only resolved jets
    # print("Eventos despues de RequestOnlyResolvedGenJets", df.Count().GetValue())


    # df_initial = ROOT.RDataFrame("Events", inFile)
    # df_initial.Snapshot("InitialEvents", "initial.root", ["event"])

    # # Aplicamos los filtros y guardamos los eventos eliminados en cada paso
    # def save_rejected_events(df, previous_df, filter_function, filter_name):
    #     df_after_filter = filter_function(previous_df)  # Aplicar el filtro
    #     df_rejected = previous_df.Filter(f"!( {filter_name} )")  # Filtrar los eliminados
    #     df_rejected.Snapshot(f"RejectedEvents_{filter_name}", f"rejected_{filter_name}.root", ["event"])
    #     print(f"Eventos eliminados en {filter_name}: {df_rejected.Count().GetValue()}")
    #     return df_after_filter

    # df = df.Define("n_GenJet", "GenJet_idx.size()")
    # df = save_rejected_events(df, df_initial, HHBaseline.PassGenAcceptance, "PassGenAcceptance")

    # df = save_rejected_events(df, df, HHBaseline.GenJetSelection, "GenJetSelection")
    # df = save_rejected_events(df, df, HHBaseline.GenJetHttOverlapRemoval, "GenJetHttOverlapRemoval")
    # df = save_rejected_events(df, df, HHBaseline.RequestOnlyResolvedGenJets, "RequestOnlyResolvedGenJets")
    # df = save_rejected_events(df, df, HHBaseline.GenVBFJetSelection, "GenVBFJetSelection")

    # print("Archivos .root creados con eventos eliminados en cada filtro.")

    df = df.Define("sample", f"static_cast<int>(SampleType::{sample})")
    df = df.Define("period", f"static_cast<int>(Period::Run{run}_{period})")
    df = df.Define("X_mass", f"static_cast<int>({X_mass})")
    df = df.Define("node_index", f"static_cast<int>({node_index})")

    df = HHBaseline.GenRecoTauMatching(df)
    df = HHBaseline.GenJetMatchingForBjets(df)

    if apply_vbf_cuts:
        pT_threshold = 30.0
    else:
        pT_threshold = 20.0

    df = HHBaseline.RecoVBFJetSelection_CCLUB(df, pT_threshold)
    df = HHBaseline.GenRecoVBFJetMatching_CCLUB(df)

    df = HHBaseline.DefineVBFCand_CCLUB(df)

    df = HHBaseline.DefineisCCLUBjet(df)
    df = HHBaseline.DefineisCCLUBvbfjet(df)

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
 
    df = HHBaseline.VBFTopologicalVariables_CCLUB(df, centralJet_ptThreshold)

    # Apply VBF topological cuts if requested (for purer sample)
    if apply_vbf_cuts:
        print(f"Applying VBF topological cuts for purer sample...")
        df = HHBaseline.ApplyVBFTopologicalSelection_CCLUB(df, centralJet_ptThreshold)

    # Show final statistics (total efficiency from initial to final)
    events_final = df.Count().GetValue()
    final_efficiency = 100 * events_final / events_initial
    
    if apply_vbf_cuts:
        print(f"Final statistics (baseline + VBF cuts): {events_final}/{events_initial} events ({final_efficiency:.1f}% total efficiency)")
    else:
        print(f"Final statistics (baseline only): {events_final}/{events_initial} events ({final_efficiency:.1f}% total efficiency)")

    df = df.Define("channel", "pairType")

    df = JetSavingCondition(df, jet_selection)
    df = GenJetSavingCondition(df)
    # df = LHEPartSavingCondition(df)

    report = df.Report()
    histReport=ReportTools.SaveReport(report.GetValue())

    colToSave = ["event","luminosityBlock",
                "HttCandidate_leg0_pt", "HttCandidate_leg0_eta", "HttCandidate_leg0_phi", "HttCandidate_leg0_mass", "HttCandidate_leg1_pt", "HttCandidate_leg1_eta", "HttCandidate_leg1_phi","HttCandidate_leg1_mass",
                "HbbCandidate_leg0_pt", "HbbCandidate_leg0_eta", "HbbCandidate_leg0_phi", "HbbCandidate_leg0_mass", "HbbCandidate_leg1_pt", "HbbCandidate_leg1_eta", "HbbCandidate_leg1_phi","HbbCandidate_leg1_mass",
                "VBFCand_leg0_pt", "VBFCand_leg0_eta", "VBFCand_leg0_phi", "VBFCand_leg0_mass", "VBFCand_leg1_pt", "VBFCand_leg1_eta", "VBFCand_leg1_phi","VBFCand_leg1_mass",
                "VBF_mjj", "VBF_deltaEta", "VBF_deltaPhi", "VBF_centrality_htt", "VBF_centrality_hbb", "nJets_central",
                "channel","sample", "period", "X_mass", "node_index", "PuppiMET_pt", "PuppiMET_phi"]

    colToSave+=[f"RecoJet_{var}" for var in jetVar_list]
    colToSave+=[f"genjet_{genvar}" for genvar in genjetVar_list]
    colToSave+=[f"LHEPart_{lhevar}" for lhevar in lheVar_list]
    colToSave+=["GenJet_b_PF", "GenJet_Hbb" , "GenJet_idx", "GenJet_eta", "GenJet_B3"]
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
    parser.add_argument('--jet_selection', type=str, default="vbf_only",
                        choices=['all', 'vbf_only'],
                        help='Jet selection strategy: all (b+VBF jets with pT>20), vbf_only (only VBF jets)')
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

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine(".include "+ os.environ['ANALYSIS_PATH'])
    ROOT.gROOT.ProcessLine('#include "include/GenTools.h"')
    ROOT.gInterpreter.ProcessLine(f"ParticleDB::Initialize(\"{args.particleFile}\");")
    snapshotOptions = ROOT.RDF.RSnapshotOptions()
    snapshotOptions.fOverwriteIfExists=True
    snapshotOptions.fCompressionAlgorithm = getattr(ROOT.ROOT, 'k' + args.compressionAlgo)
    snapshotOptions.fCompressionLevel = args.compressionLevel
    createSkim(inFile, args.outFile, args.run, args.period, args.sample, args.X_mass, args.node_index, args.mpv, args.version, config, snapshotOptions, args.vbf_cuts, args.jet_selection)
