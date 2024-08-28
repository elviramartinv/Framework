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

p = "/afs/cern.ch/user/e/emartinv/public/hhbtag_skims_fw/new_HHbtag/"
# nonres = "GluGluToHHTo2B2Tau_node_SM_2018.root"
# res_250 = "GluGluToRadionToHHTo2B2Tau_M-250_2018.root"
# res_500 = "GluGluToRadionToHHTo2B2Tau_M-500.root"
# res_1000 =  "GluGluToRadionToHHTo2B2Tau_M-1000.root"
# res_1500 = "GluGluToRadionToHHTo2B2Tau_M-1500.root"
# res_3000 = "GluGluToRadionToHHTo2B2Tau_M-3000.root"
# TT = "TTToSemiLeptonic_nano_0.root"
# DY = "DYJetsToLL_M-50_nano_0.root"
# DY_2J = "DYJetsToLL_2J_nano_0.root"
VBF_2022 = "2022_VBFtoHHto2B2Tau_SM.root"
VBF_2022_v2 = "2022_VBFtoHHto2B2Tau_SM_v2.root"
GGF_2022 = "2022_GluGlutoHHto2B2Tau_SM.root"
GGF_2022_v2 = "2022_GluGlutoHHto2B2Tau_SM_v2.root"

samples_colors = ['#900C3F']
# samples_colors = ['#900C3F', '#EAA850', '#EA5750']
samples = [VBF_2022, VBF_2022_v2]
# samples = [GGF_2022, GGF_2022_v2]
sample_name = "VBF_2022"
# sample_name = "GGF_2022"
# label = ['HH nonres SM', 'TT dl', 'DY']
signal_colors = ['#900C3F', '#50EAA8', '#50B4EA', '#5083EA', '#8F50EA', '#EA5096']
# signal_samples = [nonres, res_250, res_500, res_1000, res_1500, res_3000]
# signal_label = ['nonres', 'res_250', 'res_500', 'res_1000', 'res_1500', 'res_3000']

taggers = ["HHBtagScore", "btagPNetB", "btagDeepFlavB", "btagRobustParTAK4B"]
taggers_v2 = ["HHBtagScore_v2"]
tagger_colors = {
    "HHBtagScore": "#900C3F",
    "btagPNetB": "#EAA850",
    "btagDeepFlavB": "#50EAA8",
    "btagRobustParTAK4B": "#50B4EA",
    "HHBtagScore_v2": "#FF5733"
}

legend_elements = []
num_bins = 40
bin_edges = np.linspace(0, 2, num_bins+1)

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        # print(f)
        df = ROOT.RDataFrame("Event", f)
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_pt.size() >= 1 ? RecoJet_{tag}[idx_jets_{tag}[0]] : -1")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_pt.size() >= 2 ? RecoJet_{tag}[idx_jets_{tag}[1]] : -1")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_pt.size() >= 3 ? RecoJet_{tag}[idx_jets_{tag}[2]] : -1")
        df = df.Define(f"FourthJet_{tag}", f"RecoJet_pt.size() >= 4 ? RecoJet_{tag}[idx_jets_{tag}[3]] : -1")
        df = df.Define(f"Sum_{tag}", f"FirstJet_{tag} + SecondJet_{tag}")
        df = df.Define("SumGreaterThan2", f"Sum_{tag} > 2.000001 ? 1 : 0")
    # count = df.Filter("SumGreaterThan2 == 1").Count()
    # print("Number of events where Sum_{tag} > 2: ", count.GetValue(), "event", )
    # df = df.Filter("SumGreaterThan2 == 1")
        columns_to_save = ["event", f"RecoJet_{tag}", f"FirstJet_{tag}", f"SecondJet_{tag}", f"ThirdJet_{tag}", f"FourthJet_{tag}"]
        # df.Snapshot("output", f"output_{sample}.root", columns_to_save)
        df = None
# raise RuntimeError("Stop here")


#F#################### first jet
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df1 = ROOT.RDataFrame("Event", f)
        df1 = df1.Filter("RecoJet_pt.size() >= 1")
        df1 = df1.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df1 = df1.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df1 = df1.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        hist = df1.Histo1D(f"FirstJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df1.Count().GetValue()
        # print("num_events", num_events)
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=1, histtype='step', color=color)
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

# legend_elements = [Patch(facecolor=tagger_colors[tag], edgecolor=tagger_colors[tag], alpha=1, linewidth=2, label=tag) for tag in taggers + taggers_v2] 
plt.xlabel("Score")
plt.ylabel("Normalized Events") 
plt.title("First Jet scores")
plt.yscale('log')
plt.xlim(-0.2,2.2)
# plt.legend(loc='upper right')
plt.legend(handles=legend_elements, loc='upper right')
plt.savefig(f"output/{sample_name}/scores/firstjet_scores.png", dpi=300)

# raise RuntimeError("Stop here")

################# second jet
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() >= 2")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        hist = df.Histo1D(f"SecondJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df.Count().GetValue()
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=20, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=20, alpha=1, histtype='step', color=color)
        # legend_elements = [Patch(facecolor=tagger_colors[tag], edgecolor=tagger_colors[tag], alpha=1, linewidth=2, label=tag) for tag in taggers]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))
plt.xlabel("Score")
plt.ylabel("Normalized Events") 
plt.title("Second Jet scores")
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(handles=legend_elements, loc='upper right')
plt.savefig(f"output/{sample_name}/scores/secondjet_scores.png", dpi=300)

# raise RuntimeError("Stop")
### third jet
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() >= 2")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        hist = df.Histo1D(f"ThirdJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df.Count().GetValue()
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=20, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=20, alpha=1, histtype='step', color=color)
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))
plt.xlabel("Score")
plt.ylabel("Normalized Events") 
plt.title("Third Jet scores")
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(handles=legend_elements, loc='upper right')
plt.savefig(f"output/{sample_name}/scores/thirdjet_scores.png", dpi=300)


#####   fourth jet
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() >= 2")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"FourthJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[3]]")
        hist = df.Histo1D(f"FourthJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df.Count().GetValue()
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=20, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=20, alpha=1, histtype='step', color=color)
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))
plt.xlabel("Score")
plt.ylabel("Normalized Events") 
plt.title("Fourth Jet scores")
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(handles=legend_elements, loc='upper right')
plt.savefig(f"output/{sample_name}/scores/fourthjet_scores.png", dpi=300)

################# 2D plot

plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        bin_size = 0.05
        x_min, x_max = 0, 2 + bin_size
        y_min, y_max = 0, 2 + bin_size
        bins_x = int((x_max - x_min) / bin_size)
        bins_y = int((y_max - y_min) / bin_size)

        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        # df = df.Filter("RecoJet_pt.size() >= 2")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_pt.size() >= 2 ? RecoJet_{tag}[idx_jets_{tag}[0]] : -1")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_pt.size() >= 2 ? RecoJet_{tag}[idx_jets_{tag}[1]] : -1")
        hist2D = df.Histo2D(("hist2D", f"2D plot of FirstJet_{tag} vs SecondJet_{tag}", bins_x, x_min, x_max, bins_y, y_min, y_max), f"FirstJet_{tag}", f"SecondJet_{tag}")
        
        hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

        plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
        plt.colorbar(label="Events")
        plt.xlabel(f"Leading Jet {tag}")
        plt.ylabel(f"Second Jet {tag}")
        plt.title(f"Lead Jet vs Second Jet")
        plt.savefig(f"output/{sample_name}/scores/2Dplot_{sample}_{tag}.png", dpi=300)
        plt.clf()


################# 2D plot when 2 jets reconstructed

# plt.figure()

# for sample in samples:

#     bin_size = 0.05
#     x_min, x_max = 0, 2 + bin_size
#     y_min, y_max = 0, 2 + bin_size
#     bins_x = int((x_max - x_min) / bin_size)
#     bins_y = int((y_max - y_min) / bin_size)

#     f = p + sample
#     df = ROOT.RDataFrame("Event", f)
#     df = df.Filter("RecoJet_pt.size() >= 2")
#     df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
#     df = df.Define('idx_jets_HHBtag', 'ReorderObjects(RecoJet_HHBtagScore, RecoJet_idx)')
#     df = df.Define("FirstJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[0]]")
#     df = df.Define("SecondJet_HHBtagScore", "RecoJet_HHBtagScore[idx_jets_HHBtag[1]]")
#     hist2D = df.Histo2D(("hist2D", "2D plot of FirstJet_HHBtagScore vs SecondJet_HHBtagScore", bins_x, x_min, x_max, bins_y, y_min, y_max), "FirstJet_HHBtagScore", "SecondJet_HHBtagScore")
    
#     hist2D_np = np.array([[hist2D.GetBinContent(i, j) if hist2D.GetBinContent(i, j) != 0 else np.nan for j in range(1, hist2D.GetNbinsY()+1)] for i in range(1, hist2D.GetNbinsX()+1)])

#     plt.imshow(hist2D_np, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='viridis', norm=LogNorm())
#     plt.colorbar(label="Events")
#     plt.xlabel("Leading Jet HHBtag")
#     plt.ylabel("Second Jet HHBtag")
#     plt.title(f"Lead Jet vs Second Jet for {label[samples.index(sample)]}")
#     plt.savefig(f"output/scores_HHBtagordered/2Dplot_{sample}_2RecoJets.png", dpi=300)
#     plt.clf()

raise RuntimeError("Stop here")

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
# plt.figure()
# for sample in samples:
#     f = p + sample
#     df = ROOT.RDataFrame("Event", f)
#     df = df.Filter("RecoJet_pt.size() > 2")
#     hist = df.Histo1D("RecoJet_HHBtagScore")
#     hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
#     x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
#     num_events = df.Count().GetValue()
#     hist_np = hist_np / num_events
#     plt.hist(x, weights=hist_np, bins=len(x), alpha=0.2, color=samples_colors[samples.index(sample)], histtype='stepfilled')
#     plt.hist(x, weights=hist_np, bins=len(x), alpha=1, color=samples_colors[samples.index(sample)], label=label[samples.index(sample)], histtype='step')
#     legend_elements = [Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=label[samples.index(sample)]) for sample, color in zip(samples, samples_colors)]
#     plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.85, 1))
# plt.xlabel("HHBtagScore")
# plt.ylabel("Normalized Events")
# plt.title("Scores")
# # plt.yscale('log')
# plt.xlim(-0.2,2.2)
# plt.savefig("output/scores_HHBtagordered/scores_signal_bck_2RecoJet.png", dpi=300)

# raise RuntimeError("Stop here")

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
