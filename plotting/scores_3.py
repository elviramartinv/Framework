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

VBF_2022 = "2022_VBFtoHHto2B2Tau_SM.root"
VBF_2022_v2 = "2022_VBFtoHHto2B2Tau_SM_v2.root"
GGF_2022 = "2022_GluGlutoHHto2B2Tau_SM.root"
GGF_2022_v2 = "2022_GluGlutoHHto2B2Tau_SM_v2.root"

samples_colors = ['#900C3F']
# samples_colors = ['#900C3F', '#EAA850', '#EA5750']
# samples = [VBF_2022, VBF_2022_v2]
samples = [GGF_2022, GGF_2022_v2]
# sample_name = "VBF_2022"
sample_name = "GGF_2022"
# label = ['HH nonres SM', 'TT dl', 'DY']
signal_colors = ['#900C3F', '#50EAA8', '#50B4EA', '#5083EA', '#8F50EA', '#EA5096']


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
        df1 = df1.Filter("RecoJet_pt.size() == 3")
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
plt.savefig(f"output/{sample_name}/scores_3jets/firstjet_scores.png", dpi=300)

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
        df = df.Filter("RecoJet_pt.size() == 3")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        hist = df.Histo1D(f"SecondJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df.Count().GetValue()
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=1, histtype='step', color=color)
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
plt.savefig(f"output/{sample_name}/scores_3jets/secondjet_scores.png", dpi=300)


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
        df = df.Filter("RecoJet_pt.size() == 3")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        hist = df.Histo1D(f"ThirdJet_{tag}")
        hist_np = np.array([hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)])
        x = np.array([hist.GetBinCenter(i) for i in range(1, hist.GetNbinsX()+1)])
        num_events = df.Count().GetValue()
        hist_np = hist_np / num_events
        color = tagger_colors[tag]
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=0.2, histtype='stepfilled', color=color, label=f"{tag}")
        plt.hist(x, weights=hist_np, bins=bin_edges, alpha=1, histtype='step', color=color)
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))
plt.xlabel("Score")
plt.ylabel("Normalized Events") 
plt.title("Third Jet scores")
plt.yscale('log')
plt.xlim(-0.2,2.2)
plt.legend(handles=legend_elements, loc='upper right')
plt.savefig(f"output/{sample_name}/scores_3jets/thirdjet_scores.png", dpi=300)
