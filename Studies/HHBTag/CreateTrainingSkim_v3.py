import ROOT
import numpy as np
import sys
import os
if __name__ == "__main__":
    sys.path.append(os.environ['ANALYSIS_PATH'])
import Common.Utilities as Utilities
import Common.ReportTools as ReportTools
import yaml
import Common.BaselineSelection as Baseline
import AnaProd.HH_bbtautau.baseline as HHBaseline


def createSkim(inFile, outFile, run, period, sample, X_mass, node_index, mpv, snapshotOptions):
    jetVar_list = [ "pt", "eta", "phi", "mass", "HHBtagScore_v3", "btagDeepFlavB", "btagPNetB", "btagRobustParTAK4B", "genMatched", "hadronFlavour"] # "HHBtagScore" excluded for now until I can test the new version for Run3
    def JetSavingCondition(df):
        df = df.Define('Jet_selIdx', 'ReorderObjects(Jet_btagRobustParTAK4B, Jet_idx[Jet_bCand_CCLUB])')
        for var in jetVar_list:
            df = df.Define(f"RecoJet_{var}", f"Take(Jet_{var}, Jet_selIdx)")
        return df
    
    genjetVar_list = ["pt","eta","phi","mass","hadronFlavour"]
    def GenJetSavingCondition(df):
        for genvar in genjetVar_list:
            df = df.Define(f"genjet_{genvar}",f"Take(GenJet_{genvar}, GenJet_idx)")
        return df

    Baseline.Initialize(True, True)

    df = ROOT.RDataFrame("Events", inFile)
    # df = df.Range(100)
    df = Baseline.CreateRecoP4(df)
    df = Baseline.SelectRecoP4(df)
    df = Baseline.DefineGenObjects(df, isHH=True, Hbb_AK4mass_mpv=mpv)

    # print("count at the beginning", df.Count().GetValue())
    df = df.Define("n_GenJet", "GenJet_idx.size()")
    df = HHBaseline.PassGenAcceptance(df)
    df = HHBaseline.GenJetSelection(df)
    df = HHBaseline.GenJetHttOverlapRemoval(df)

    df = HHBaseline.RecoJetSelection_CCLUB(df)

    df = HHBaseline.GenRecoJetMatching_CCLUB(df)
    df = df.Define("sample", f"static_cast<int>(SampleType::{sample})")
    df = df.Define("period", f"static_cast<int>(Period::Run{run}_{period})")
    df = df.Define("X_mass", f"static_cast<int>({X_mass})")
    df = df.Define("node_index", f"static_cast<int>({node_index})")

    df = df.Define(f"Jet_HHBtagScore_v3", "GetHHBtagScore_v3(Jet_bCand_CCLUB, Jet_idx, Jet_p4, Jet_btagPNetB, MET_pt,  MET_phi, dau1_p4, dau1_pt, dau2_p4, dau2_pt, period, event, pairType)")

    df = df.Define("HttCandidate_leg0_pt", "dau1_pt")
    df = df.Define("HttCandidate_leg0_eta", "dau1_eta")
    df = df.Define("HttCandidate_leg0_phi", "dau1_phi")
    df = df.Define("HttCandidate_leg0_mass", "dau1_mass")
    df = df.Define("HttCandidate_leg1_pt", "dau2_pt")
    df = df.Define("HttCandidate_leg1_eta", "dau2_eta")
    df = df.Define("HttCandidate_leg1_phi", "dau2_phi")
    df = df.Define("HttCandidate_leg1_mass", "dau2_mass")
    df = df.Define("channel", "pairType")

    n_MoreThanTwoMatches = df.Filter("Jet_idx[Jet_genMatched].size()>2").Count()
    df = JetSavingCondition(df)
    df = GenJetSavingCondition(df)

    report = df.Report()
    histReport=ReportTools.SaveReport(report.GetValue())
    if(n_MoreThanTwoMatches.GetValue()!=0) :
        raise RuntimeError('There are more than two jets matched! ')

    colToSave = ["event","luminosityBlock",
                "HttCandidate_leg0_pt", "HttCandidate_leg0_eta", "HttCandidate_leg0_phi", "HttCandidate_leg0_mass", "HttCandidate_leg1_pt", "HttCandidate_leg1_eta", "HttCandidate_leg1_phi","HttCandidate_leg1_mass",
                "channel","sample", "period", "X_mass", "node_index", "MET_pt", "MET_phi", "PuppiMET_pt", "PuppiMET_phi"]

    colToSave+=[f"RecoJet_{var}" for var in jetVar_list]
    colToSave+=[f"genjet_{genvar}" for genvar in genjetVar_list]
    colToSave+=["GenJet_b_PF", "GenJetAK8_b_PF", "GenJet_Hbb" , "GenJetAK8_Hbb", "GenJet_idx"]
    colToSave+=["genHbbIdx", "GenPart_pdgId", "GenPart_genPartIdxMother", "GenPart_statusFlags", "GenJet_partonFlavour", "GenPart_phi"]

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
    parser.add_argument('--inFile', type=str)
    parser.add_argument('--outFile', type=str)
    parser.add_argument('--X_mass', type=int, default=-1)
    parser.add_argument('--node_index', type=int, default=-1)
    parser.add_argument('--mpv', type=float, default=125)
    parser.add_argument('--sample', type=str)
    parser.add_argument('--compressionLevel', type=int, default=9)
    parser.add_argument('--compressionAlgo', type=str, default="LZMA")
    parser.add_argument('--particleFile', type=str,
                        default=f"{os.environ['ANALYSIS_PATH']}/config/pdg_name_type_charge.txt")
    args = parser.parse_args()

    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.ProcessLine(".include "+ os.environ['ANALYSIS_PATH'])
    ROOT.gROOT.ProcessLine('#include "include/GenTools.h"')
    ROOT.gInterpreter.ProcessLine(f"ParticleDB::Initialize(\"{args.particleFile}\");")
    snapshotOptions = ROOT.RDF.RSnapshotOptions()
    snapshotOptions.fOverwriteIfExists=True
    snapshotOptions.fCompressionAlgorithm = getattr(ROOT.ROOT, 'k' + args.compressionAlgo)
    snapshotOptions.fCompressionLevel = args.compressionLevel
    createSkim(args.inFile, args.outFile, args.run, args.period, args.sample, args.X_mass, args.node_index, args.mpv, snapshotOptions)
