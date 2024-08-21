import ROOT
import matplotlib.pyplot as plt
import numpy as np

# Lista de archivos
path = "/afs/cern.ch/user/e/emartinv/public/cms-hh-bbtautau/Framework/newHH/GluGluToHHTo2B2Tau_node_SM_"

colors = ['purple', 'red', 'blue', 'green']
years = ["2016HIPM", "2016", "2017", "2018"]

#FirstJet_HHBtagScore
plt.figure()

for year in years:
    f = path + str(year) + ".root"
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[0]")
    hist = df.Histo1D("FirstJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, histtype='step', color=colors[years.index(year)], label='First Jet ' + year)
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events") 
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(loc='upper right')
plt.savefig("output/firstjet_scores_years.png", dpi=300)

#SecondJet_HHBtagScore
plt.figure()

for year in years:
    f = path + str(year) + ".root"
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_HHBtagScore[1]")
    hist = df.Histo1D("SecondJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, histtype='step', color=colors[years.index(year)], label='Second Jet ' + year)
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events") 
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(loc='upper right')
plt.savefig("output/secondjet_scores_years.png", dpi=300)

