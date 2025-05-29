import ROOT
import numpy as np
import sys
import os
if __name__ == "__main__":
    sys.path.append(os.environ['ANALYSIS_PATH'])
import Common.Utilities as Utilities
import Common.ReportTools as ReportTools
import yaml
import glob
import Common.BaselineSelection as Baseline
import AnaProd.HH_bbtautau.baseline as HHBaseline


def createSkim(inFile, outFile, run, period, sample, X_mass, node_index, mpv, version, config, snapshotOptions):
    jetVar_list = [ "pt", "eta", "phi", "mass", "invMass", f"HHBtagScore_v{version}", "btagDeepFlavB", "btagPNetB", "genMatched", "vbfgenMatched"] # "HHBtagScore" excluded for now until I can test the new version for Run3
    
    def JetSavingCondition(df):
        df = df.Define('Jet_selIdx', 'ReorderObjects(Jet_invMass, Jet_idx)')
        for var in jetVar_list:
            df = df.Define(f"RecoJet_{var}", f"Take(Jet_{var}, Jet_selIdx)")
        return df
    
    genjetVar_list = ["pt","eta","phi","mass"]
    def GenJetSavingCondition(df):
        for genvar in genjetVar_list:
            df = df.Define(f"genjet_{genvar}",f"Take(GenJet_{genvar}, GenJet_idx)")
        return df
    
    lheVar_list = ["status", "pdgId", "pt", "eta", "phi", "mass"]
    def LHEPartSavingCondition(df):
        for lhevar in lheVar_list:
            df = df.Define(f"LHEPart_{lhevar}", f"Take(LHEPart_{lhevar}, LHEPart_idx)")
        return df


    Baseline.Initialize(True, True)

    df = ROOT.RDataFrame("Events", inFile)
    # print("number of events before any selection: ", df.Count().GetValue())
    # df = df.Range(100)
    df = Baseline.CreateRecoP4(df)
    df = Baseline.SelectRecoP4(df)
    df = Baseline.DefineGenObjects(df, isHH=True, isVBF=True, Hbb_AK4mass_mpv=mpv)

    df = HHBaseline.RecoJetInvMass(df)

    df = df.Define("n_GenJet", "GenJet_idx.size()")
    df = HHBaseline.PassGenAcceptance(df)
    df = HHBaseline.GenJetSelection(df)
    df = HHBaseline.GenJetHttOverlapRemoval(df)
    df = HHBaseline.RequestOnlyResolvedGenJets(df)

    # df = HHBaseline.RecoLeptonsSelection(df)
    # df = Baseline.RecoJetAcceptance(df)

    df = HHBaseline.RecoHttCandidateSelection(df, config["GLOBAL"])
    # df = HHBaseline.RecoHttCandidateSelection(df)
    df = HHBaseline.RecoJetSelection(df)


    df = df.Define('genChannel', 'genHttCandidate->channel()')
    df = df.Define('recoChannel', 'HttCandidate.channel()')

    df = df.Filter("genChannel == recoChannel", "SameGenRecoChannels")
    df = df.Filter("GenRecoMatching(*genHttCandidate, HttCandidate, 0.2)", "SameGenRecoHTT")
    # df = Baseline.RequestOnlyResolvedRecoJets(df)

    df = HHBaseline.GenRecoJetMatching(df)
    df = df.Define("sample", f"static_cast<int>(SampleType::{sample})")
    df = df.Define("period", f"static_cast<int>(Period::Run{run}_{period})")
    df = df.Define("X_mass", f"static_cast<int>({X_mass})")
    df = df.Define("node_index", f"static_cast<int>({node_index})")

    # df = HHBaseline.DefineHbbCand(df) 
    df = df.Define(f"Jet_HHBtagScore_v{version}", "GetHHBtagScore(Jet_bCand, Jet_idx, Jet_p4, Jet_btagDeepFlavB, PFMET_pt,  PFMET_phi, HttCandidate, period, event)")
    df = df.Define("HbbCandidate", f"GetHbbCandidate(Jet_HHBtagScore_v{version}, Jet_bCand, Jet_p4, Jet_idx)")


    df = HHBaseline.RecoVBFJetSelection(df)
    # print("number of events after VBFJet selection: ", df.Count().GetValue())

    df = HHBaseline.GenRecoVBFJetMatching(df)
    # print("number of events after GenRecoVBFJetMatching: ", df.Count().GetValue())

    df = HHBaseline.DefineVBFCand(df)

    df = df.Define("HttCandidate_leg0_pt", "HttCandidate.leg_p4[0].Pt()")
    df = df.Define("HttCandidate_leg0_eta", "HttCandidate.leg_p4[0].Eta()")
    df = df.Define("HttCandidate_leg0_phi", "HttCandidate.leg_p4[0].Phi()")
    df = df.Define("HttCandidate_leg0_mass", "HttCandidate.leg_p4[0].M()")
    df = df.Define("HttCandidate_leg1_pt", "HttCandidate.leg_p4[1].Pt()")
    df = df.Define("HttCandidate_leg1_eta", "HttCandidate.leg_p4[1].Eta()")
    df = df.Define("HttCandidate_leg1_phi", "HttCandidate.leg_p4[1].Phi()")
    df = df.Define("HttCandidate_leg1_mass", "HttCandidate.leg_p4[1].M()")

    df = df.Define("HbbCandidate_leg0_pt", "HbbCandidate->leg_p4[0].Pt()")
    df = df.Define("HbbCandidate_leg0_eta", "HbbCandidate->leg_p4[0].Eta()")
    df = df.Define("HbbCandidate_leg0_phi", "HbbCandidate->leg_p4[0].Phi()")
    df = df.Define("HbbCandidate_leg0_mass", "HbbCandidate->leg_p4[0].M()")
    df = df.Define("HbbCandidate_leg1_pt", "HbbCandidate->leg_p4[1].Pt()")
    df = df.Define("HbbCandidate_leg1_eta", "HbbCandidate->leg_p4[1].Eta()")
    df = df.Define("HbbCandidate_leg1_phi", "HbbCandidate->leg_p4[1].Phi()")
    df = df.Define("HbbCandidate_leg1_mass", "HbbCandidate->leg_p4[1].M()")

    df = df.Define("VBFCand_leg0_pt", "VBFCand->leg_p4[0].Pt()")
    df = df.Define("VBFCand_leg0_eta", "VBFCand->leg_p4[0].Eta()")
    df = df.Define("VBFCand_leg0_phi", "VBFCand->leg_p4[0].Phi()")
    df = df.Define("VBFCand_leg0_mass", "VBFCand->leg_p4[0].M()")
    df = df.Define("VBFCand_leg1_pt", "VBFCand->leg_p4[1].Pt()")
    df = df.Define("VBFCand_leg1_eta", "VBFCand->leg_p4[1].Eta()")
    df = df.Define("VBFCand_leg1_phi", "VBFCand->leg_p4[1].Phi()")
    df = df.Define("VBFCand_leg1_mass", "VBFCand->leg_p4[1].M()")


    df = df.Define("channel", "static_cast<int>(genChannel)")

    n_MoreThanTwoMatches = df.Filter("Jet_idx[Jet_genMatched].size()>2").Count()
    df = JetSavingCondition(df)
    df = GenJetSavingCondition(df)
    # df = LHEPartSavingCondition(df)

    report = df.Report()
    histReport=ReportTools.SaveReport(report.GetValue())
    if(n_MoreThanTwoMatches.GetValue()!=0) :
        raise RuntimeError('There are more than two jets matched! ')

    colToSave = ["event","luminosityBlock",
                "HttCandidate_leg0_pt", "HttCandidate_leg0_eta", "HttCandidate_leg0_phi", "HttCandidate_leg0_mass", "HttCandidate_leg1_pt", "HttCandidate_leg1_eta", "HttCandidate_leg1_phi","HttCandidate_leg1_mass",
                "HbbCandidate_leg0_pt", "HbbCandidate_leg0_eta", "HbbCandidate_leg0_phi", "HbbCandidate_leg0_mass", "HbbCandidate_leg1_pt", "HbbCandidate_leg1_eta", "HbbCandidate_leg1_phi","HbbCandidate_leg1_mass",
                "VBFCand_leg0_pt", "VBFCand_leg0_eta", "VBFCand_leg0_phi", "VBFCand_leg0_mass", "VBFCand_leg1_pt", "VBFCand_leg1_eta", "VBFCand_leg1_phi","VBFCand_leg1_mass",
                "channel","sample", "period", "X_mass", "node_index", "PFMET_pt", "PFMET_phi", "PuppiMET_pt", "PuppiMET_phi"]

    colToSave+=[f"RecoJet_{var}" for var in jetVar_list]
    colToSave+=[f"genjet_{genvar}" for genvar in genjetVar_list]
    colToSave+=[f"LHEPart_{lhevar}" for lhevar in lheVar_list]
    colToSave+=["GenJet_b_PF", "GenJetAK8_b_PF", "GenJet_Hbb" , "GenJetAK8_Hbb", "GenJet_idx", "GenJet_eta", "GenJet_B2"]
    colToSave+=["Jet_selIdx", "Jet_idx", "Jet_bCand"]
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
    createSkim(inFile, args.outFile, args.run, args.period, args.sample, args.X_mass, args.node_index, args.mpv, args.version, config, snapshotOptions)
