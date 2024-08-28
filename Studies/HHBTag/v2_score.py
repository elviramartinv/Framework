import ROOT
import sys
import os
if __name__ == "__main__":
    sys.path.append(os.environ['ANALYSIS_PATH'])


def create_v2_score(inFile, outFile):
    df = ROOT.RDataFrame("Event", inFile)

    df = df.Define("RecoJet_HHBtagScore_v2", "RecoJet_HHBtagScore")

    df.Snapshot("Event", outFile)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--inFile', type=str)
    parser.add_argument('--outFile', type=str)
    args = parser.parse_args()

    ROOT.gROOT.SetBatch(True)
    create_v2_score(args.inFile, args.outFile)


