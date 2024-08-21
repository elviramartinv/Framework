import ROOT
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import LogNorm


ROOT.gInterpreter.Declare("""
using RVecS = ROOT::VecOps::RVec<size_t>;
using RVecI = ROOT::VecOps::RVec<int>;

RVecS CreateIndexes(size_t vecSize){
  RVecS i(vecSize);
  std::iota(i.begin(), i.end(), 0);
  return i;
}

template<typename V>
RVecI ReorderObjects(const V& varToOrder, const RVecI& indices, size_t nMax=std::numeric_limits<size_t>::max())
{
  RVecI ordered_indices = indices;
  std::sort(ordered_indices.begin(), ordered_indices.end(), [&](int a, int b) {
    return varToOrder.at(a) > varToOrder.at(b);
  });
  const size_t n = std::min(ordered_indices.size(), nMax);
  ordered_indices.resize(n);
  return ordered_indices;
}
""")

p = "/afs/cern.ch/user/e/emartinv/public/cms-hh-bbtautau/Framework/newHH/"
nonres = "GluGluToHHTo2B2Tau_node_SM_2018.root"
res_250 = "GluGluToRadionToHHTo2B2Tau_M-250_2018.root"
res_500 = "GluGluToRadionToHHTo2B2Tau_M-500.root"
res_1000 =  "GluGluToRadionToHHTo2B2Tau_M-1000.root"
res_1500 = "GluGluToRadionToHHTo2B2Tau_M-1500.root"
res_3000 = "GluGluToRadionToHHTo2B2Tau_M-3000.root"
TT = "TTToSemiLeptonic_nano_0.root"
DY = "DYJetsToLL_M-50_nano_0.root"
# DY_2J = "DYJetsToLL_2J_nano_0.root"

samples_colors = ['#900C3F', '#EAA850', '#EA5750']
samples = [nonres, TT, DY]
label = ['HH nonres SM', 'TT dl', 'DY']
signal_colors = ['#900C3F', '#50EAA8', '#50B4EA', '#5083EA', '#8F50EA', '#EA5096']
signal_samples = [nonres, res_250, res_500, res_1000, res_1500, res_3000]
signal_label = ['nonres', 'res_250', 'res_500', 'res_1000', 'res_1500', 'res_3000']


for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_pt.size() >= 1 ? RecoJet_HHBtagScore[idx_jets_HHBtag[0]] : -1")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_pt.size() >= 2 ? RecoJet_HHBtagScore[idx_jets_HHBtag[1]] : -1")
    df = df.Define("Sum_HHBtagScore", "FirstJet_HHBtagScore + SecondJet_HHBtagScore")
    df = df.Define("SumGreaterThan2", "Sum_HHBtagScore > 2.000001 ? 1 : 0")
    # count = df.Filter("SumGreaterThan2 == 1").Count()
    # print("Number of events where Sum_HHBtagScore > 2: ", count.GetValue(), "event", )
    # df = df.Filter("SumGreaterThan2 == 1")
    columns_to_save = ["event", "RecoJet_HHBtagScore", "FirstJet_HHBtagScore", "SecondJet_HHBtagScore"]
    df.Snapshot("output", f"output_{sample}.root", columns_to_save)

raise RuntimeError("Stop here")


#F#################### first jet
plt.figure()

for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 1")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[0]]")
    hist = df.Histo1D("FirstJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    # print("num_events", num_events)
    hist_np = hist_np / num_events
    # plt.hist(x, weights=hist_np, bins=len(x), alpha=1, histtype = 'step', color=samples_colors[samples.index(sample)], label=label[samples.index(sample)])
    plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events") 
plt.title("First Jet scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
# plt.legend(loc='upper right')
plt.savefig("output/scores_HHBtagordered/firstjet_scores_signal_bck.png", dpi=300)

###########     first jet when 2 jets reconstructed
plt.figure()

for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[0]]")
    hist = df.Histo1D("FirstJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    # print("num_events", num_events)
    hist_np = hist_np / num_events
    # plt.hist(x, weights=hist_np, bins=len(x), alpha=1, histtype = 'step', color=samples_colors[samples.index(sample)], label=label[samples.index(sample)])
    plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events") 
plt.title("First Jet scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
# plt.legend(loc='upper right')
plt.savefig("output/scores_HHBtagordered/firstjet_scores_signal_bck_2RecoJet.png", dpi=300)


################# second jet
plt.figure()

for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[1]]")
    hist = df.Histo1D("SecondJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], label=label[samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events") 
plt.title("Second Jet scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.savefig("output/scores_HHBtagordered/secondjet_scores_signal_bck.png", dpi=300)

################# 2D plot

plt.figure()

for sample in samples:

    bin_size = 0.05
    x_min, x_max = 0, 2 + bin_size
    y_min, y_max = 0, 2 + bin_size
    bins_x = int((x_max - x_min) / bin_size)
    bins_y = int((y_max - y_min) / bin_size)

    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    # df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_pt.size() >= 1 ? RecoJet_HHBtagScore[idx_jets_HHBtag[0]] : -1")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_pt.size() >= 2 ? RecoJet_HHBtagScore[idx_jets_HHBtag[1]] : -1")
    hist2D = df.Histo2D(("hist2D", "2D plot of FirstJet_HHBtagScore vs SecondJet_HHBtagScore", bins_x, x_min, x_max, bins_y, y_min, y_max), "FirstJet_HHBtagScore", "SecondJet_HHBtagScore")
    
    hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

    plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
    plt.colorbar(label="Events")
    plt.xlabel("Leading Jet HHBtag")
    plt.ylabel("Second Jet HHBtag")
    plt.title(f"Lead Jet vs Second Jet for {label[samples.index(sample)]}")
    plt.savefig(f"output/scores_HHBtagordered/2Dplot_{sample}.png", dpi=300)
    plt.clf()


################# 2D plot when 2 jets reconstructed

plt.figure()

for sample in samples:

    bin_size = 0.05
    x_min, x_max = 0, 2 + bin_size
    y_min, y_max = 0, 2 + bin_size
    bins_x = int((x_max - x_min) / bin_size)
    bins_y = int((y_max - y_min) / bin_size)

    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[0]]")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[1]]")
    hist2D = df.Histo2D(("hist2D", "2D plot of FirstJet_HHBtagScore vs SecondJet_HHBtagScore", bins_x, x_min, x_max, bins_y, y_min, y_max), "FirstJet_HHBtagScore", "SecondJet_HHBtagScore")
    
    hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

    plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
    plt.colorbar(label="Events")
    plt.xlabel("Leading Jet HHBtag")
    plt.ylabel("Second Jet HHBtag")
    plt.title(f"Lead Jet vs Second Jet for {label[samples.index(sample)]}")
    plt.savefig(f"output/scores_HHBtagordered/2Dplot_{sample}_2RecoJets.png", dpi=300)
    plt.clf()


#Scores
plt.figure()
for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() > 0")
    hist = df.Histo1D("RecoJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], label=label[samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events")
plt.title("Scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.savefig("output/scores_HHBtagordered/scores_signal_bck.png", dpi=300)

#Scores
plt.figure()
for sample in samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() > 2")
    hist = df.Histo1D("RecoJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], label=label[samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events")
plt.title("Scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.savefig("output/scores_HHBtagordered/scores_signal_bck_2RecoJet.png", dpi=300)

#signal scores
plt.figure()
for sample in signal_samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() > 0")
    hist = df.Histo1D("RecoJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    # print("signal", np.sum(hist_np))
    # plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=signal_colors[signal_samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=signal_colors[signal_samples.index(sample)], label=signal_label[signal_samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=signal_label[signal_samples.index(sample)]) for sample, color in zip(signal_samples, signal_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events")
plt.title("Scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.savefig("output/scores_HHBtagordered/scores_signal.png", dpi=300)

#signal scores
plt.figure()
for sample in signal_samples:
    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() > 2")
    hist = df.Histo1D("RecoJet_HHBtagScore")
    hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
    x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
    num_events = df.Count().GetValue()
    hist_np = hist_np / num_events
    # print("signal", np.sum(hist_np))
    # plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=signal_colors[signal_samples.index(sample)], histtype='stepfilled')
    plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=signal_colors[signal_samples.index(sample)], label=signal_label[signal_samples.index(sample)], histtype='step')
    legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=signal_label[signal_samples.index(sample)]) for sample, color in zip(signal_samples, signal_colors)]
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
plt.xlabel("HHBtagScore")
plt.ylabel("Normalized Events")
plt.title("Scores")
# plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.savefig("output/scores_HHBtagordered/scores_signal_2RecoJet.png", dpi=300)


plt.figure()
for sample in signal_samples:
    bin_size = 0.05
    x_min, x_max = 0, 2 + bin_size
    y_min, y_max = 0, 2 + bin_size
    bins_x = int((x_max - x_min) / bin_size)
    bins_y = int((y_max - y_min) / bin_size)

    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_pt.size() >= 1 ? RecoJet_HHBtagScore[idx_jets_HHBtag[0]] : std::numeric_limits<float>::quiet_NaN()")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_pt.size() >= 2 ? RecoJet_HHBtagScore[idx_jets_HHBtag[1]] : std::numeric_limits<float>::quiet_NaN()")
    hist2D = df.Histo2D(("hist2D", "2D plot of FirstJet_HHBtagScore vs SecondJet_HHBtagScore", bins_x, x_min, x_max, bins_y, y_min, y_max), "FirstJet_HHBtagScore", "SecondJet_HHBtagScore")
    
    hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

    plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
    plt.colorbar(label="Events")
    plt.xlabel("Leading Jet HHBtag")
    plt.ylabel("Second Jet HHBtag")
    plt.title(f"Lead Jet vs Second Jet for {signal_label[signal_samples.index(sample)]}")
    plt.savefig(f"output/scores_HHBtagordered/2Dplot_{sample}.png", dpi=300)
    plt.clf()

plt.figure()
for sample in signal_samples:
    bin_size = 0.05
    x_min, x_max = 0, 2 + bin_size
    y_min, y_max = 0, 2 + bin_size
    bins_x = int((x_max - x_min) / bin_size)
    bins_y = int((y_max - y_min) / bin_size)

    f = p + sample
    df = ROOT.RDataFrame("Event", f)
    df = df.Filter("RecoJet_pt.size() >= 2")
    df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
    df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
    df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[0]]")
    df = df.Define("SecondJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[1]]")
    hist2D = df.Histo2D(("hist2D", "2D plot of FirstJet_HHBtagScore vs SecondJet_HHBtagScore", bins_x, x_min, x_max, bins_y, y_min, y_max), "FirstJet_HHBtagScore", "SecondJet_HHBtagScore")
    
    hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

    plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
    plt.colorbar(label="Events")
    plt.xlabel("Leading Jet HHBtag")
    plt.ylabel("Second Jet HHBtag")
    plt.title(f"Lead Jet vs Second Jet for {signal_label[signal_samples.index(sample)]}")
    plt.savefig(f"output/scores_HHBtagordered/2Dplot_{sample}_2RecoJet.png", dpi=300)
    plt.clf()
