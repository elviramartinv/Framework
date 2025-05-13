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
# samples = [VBF_2022, VBF_2022_v2]
samples = [GGF_2022, GGF_2022_v2]
# sample_name = "VBF_2022"
sample_name = "GGF_2022"
# label = ['HH nonres SM', 'TT dl', 'DY']
signal_colors = ['#900C3F', '#50EAA8', '#50B4EA', '#5083EA', '#8F50EA', '#EA5096']
# signal_samples = [nonres, res_250, res_500, res_1000, res_1500, res_3000]
# signal_label = ['nonres', 'res_250', 'res_500', 'res_1000', 'res_1500', 'res_3000']

taggers = ["HHBtagScore_v3", "btagPNetB", "btagDeepFlavB", "btagRobustParTAK4B"]
taggers_v2 = ["HHBtagScore_v2"]
tagger_colors = {
    "HHBtagScore_v3": "#900C3F",
    "btagPNetB": "#EAA850",
    "btagDeepFlavB": "#50EAA8",
    "btagRobustParTAK4B": "#50B4EA",
    "HHBtagScore_v2": "#FF5733"
}

tagger_legend_names = {
    "HHBtagScore_v3": "HHBtagScore_v3",
    "btagPNetB": "btagPNetB",
    "btagDeepFlavB": "btagDeepFlavB",
    "btagRobustParTAK4B": "btagRobustParTAK4B",
    "HHBtagScore_v2": "HHBtagScore_v2"
}

jet_positions_3 = ["FirstJet", "SecondJet", "ThirdJet"]
jet_positions_4 = ["FirstJet", "SecondJet", "ThirdJet", "FourthJet"]
jet_positions_5 = ["FirstJet", "SecondJet", "ThirdJet", "FourthJet", "FifthJet"]
jet_positions_6 = ["FirstJet", "SecondJet", "ThirdJet", "FourthJet", "FifthJet", "SixthJet"]
jet_counts_3 = {tagger: {pos: 0 for pos in jet_positions_3} for tagger in taggers + taggers_v2}
jet_counts_4 = {tagger: {pos: 0 for pos in jet_positions_4} for tagger in taggers + taggers_v2}
jet_counts_5 = {tagger: {pos: 0 for pos in jet_positions_5} for tagger in taggers + taggers_v2}
jet_counts_6 = {tagger: {pos: 0 for pos in jet_positions_6} for tagger in taggers + taggers_v2}
njets = range(1,11)
njet_counts = {n: 0 for n in njets}

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
        df = df.Define('njets', 'RecoJet_pt.size()')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_pt.size() >= 1 ? RecoJet_{tag}[idx_jets_{tag}[0]] : -1")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_pt.size() >= 2 ? RecoJet_{tag}[idx_jets_{tag}[1]] : -1")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_pt.size() >= 3 ? RecoJet_{tag}[idx_jets_{tag}[2]] : -1")
        df = df.Define(f"FourthJet_{tag}", f"RecoJet_pt.size() >= 4 ? RecoJet_{tag}[idx_jets_{tag}[3]] : -1")
        df = df.Define(f"Sum_{tag}", f"FirstJet_{tag} + SecondJet_{tag}")
        df = df.Define("SumGreaterThan2", f"Sum_{tag} > 2.000001 ? 1 : 0")
        df = df.Filter("RecoJet_pt.size()==3")



        columns_to_save = ["event", f"RecoJet_{tag}", f"JetMatched_{tag}", f"FirstJet_{tag}", f"SecondJet_{tag}", f"ThirdJet_{tag}", f"FourthJet_{tag}", "RecoJet_genMatched"]
        # df.Snapshot("output", f"output_{tag}_{sample}", columns_to_save)
# raise RuntimeError("Stop here")
##################### jets multiplicity
plt.figure()


for sample in samples:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        for n in njets:
            count = df.Filter(f"RecoJet_pt.size() == {n}").Count().GetValue()
            njet_counts[n] += count
            # print(count)

fig, ax = plt.subplots()
x = np.arange(len(njets))
counts = [njet_counts[n] for n in njets]

ax.bar(x, counts, color='#50B4EA')

ax.set_xlabel('Number of Jets')
ax.set_ylabel('Number of Events')
ax.set_title('Jet Multiplicity')
ax.set_xticks(x)
ax.set_xticklabels(njets)
plt.savefig(f"output/{sample_name}/jets_matched/jet_multiplicity.png", dpi=300)


# raise RuntimeError("Stop here")

##################### with 3 jets
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

        
        print("eventos con 3 jets", df.Count().GetValue())

        # count_2 = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[0]] == 1").Count().GetValue()
        # print("First jet matched", count_2)
        # count_3 = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[1]] == 1").Count().GetValue()
        # print("Second jet matched", count_3)
        # count_4 = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1").Count().GetValue()
        # print("Third jet matched", count_4)

        for pos in jet_positions_3:
            count = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[{jet_positions_3.index(pos)}]] == 1").Count().GetValue()
            jet_counts_3[tag][pos] += count
            # print(f"tagger {tag} jet {pos} count {count}")

# Plotting
fig, ax = plt.subplots()
x = np.arange(len(jet_positions_3))
width = 0.12

for i, (tag, color) in enumerate(tagger_colors.items()):
    counts = [jet_counts_3[tag][pos] for pos in jet_positions_3]
    legend_name = tagger_legend_names.get(tag, tag) 
    bars = ax.bar(x + i * width, counts, width, label=legend_name, color=color)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,  
            f'{int(height)}',
            ha='center',  
            va='bottom', 
            rotation=90,
            fontsize=7    
        )

ax.set_xlabel('Jet Position')
ax.set_ylabel('Number of Matches')
ax.set_title('3 RecoJets')
ax.set_xticks(x + width * (len(tagger_colors) - 1) / 2)
ax.set_xticklabels(jet_positions_3)
ax.legend()

plt.savefig(f"output/{sample_name}/jets_matched/3jet_matching_histograms.png", dpi=300)


##################### with 4 jets
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() == 4")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"JetMatched_{tag}", f"RecoJet_genMatched[idx_jets_{tag}]")
        print("eventos con 4 jets", df.Count().GetValue())

        for pos in jet_positions_4:
            count = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[{jet_positions_4.index(pos)}]] == 1").Count().GetValue()
            jet_counts_4[tag][pos] += count
            # print(f"tagger {tag} jet {pos} count {count}")

# Plotting
fig, ax = plt.subplots()
x = np.arange(len(jet_positions_4))
width = 0.12

for i, (tag, color) in enumerate(tagger_colors.items()):
    counts = [jet_counts_4[tag][pos] for pos in jet_positions_4]
    legend_name = tagger_legend_names.get(tag, tag) 
    bars = ax.bar(x + i * width, counts, width, label=legend_name, color=color)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,  
            f'{int(height)}',
            ha='center',  
            va='bottom', 
            rotation=90,
            fontsize=7    
        )

ax.set_xlabel('Jet Position')
ax.set_ylabel('Number of Matches')
ax.set_title('4 RecoJets')
ax.set_xticks(x + width * (len(tagger_colors) - 1) / 2)
ax.set_xticklabels(jet_positions_4)
ax.legend()

plt.savefig(f"output/{sample_name}/jets_matched/4jet_matching_histograms.png", dpi=300)

##################### with 5 jets
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() == 5")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"JetMatched_{tag}", f"RecoJet_genMatched[idx_jets_{tag}]")
        print("eventos con 5 jets", df.Count().GetValue())
        
        for pos in jet_positions_5:
            count = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[{jet_positions_5.index(pos)}]] == 1").Count().GetValue()
            jet_counts_5[tag][pos] += count
            # print(f"tagger {tag} jet {pos} count {count}")

# Plotting
fig, ax = plt.subplots()
x = np.arange(len(jet_positions_5))
width = 0.12

for i, (tag, color) in enumerate(tagger_colors.items()):
    counts = [jet_counts_5[tag][pos] for pos in jet_positions_5]
    legend_name = tagger_legend_names.get(tag, tag) 
    bars = ax.bar(x + i * width, counts, width, label=legend_name, color=color)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,  
            f'{int(height)}',
            ha='center',  
            va='bottom', 
            rotation=90,
            fontsize=7    
        )

ax.set_xlabel('Jet Position')
ax.set_ylabel('Number of Matches')
ax.set_title('5 RecoJets')
ax.set_xticks(x + width * (len(tagger_colors) - 1) / 2)
ax.set_xticklabels(jet_positions_5)
ax.legend()

plt.savefig(f"output/{sample_name}/jets_matched/5jet_matching_histograms.png", dpi=300)


##################### with 6 jets
plt.figure()

for sample in samples:
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() == 6")
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"JetMatched_{tag}", f"RecoJet_genMatched[idx_jets_{tag}]")
        print("eventos con 6 jets", df.Count().GetValue())
        for pos in jet_positions_6:
            count = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[{jet_positions_6.index(pos)}]] == 1").Count().GetValue()
            jet_counts_6[tag][pos] += count
            # print(f"tagger {tag} jet {pos} count {count}")

# Plotting
fig, ax = plt.subplots()
x = np.arange(len(jet_positions_6))
width = 0.12

for i, (tag, color) in enumerate(tagger_colors.items()):
    counts = [jet_counts_6[tag][pos] for pos in jet_positions_6]
    legend_name = tagger_legend_names.get(tag, tag) 
    bars = ax.bar(x + i * width, counts, width, label=legend_name, color=color)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,  
            f'{int(height)}',
            ha='center',  
            va='bottom', 
            rotation=90,
            fontsize=7    
        )

ax.set_xlabel('Jet Position')
ax.set_ylabel('Number of Matches')
ax.set_title('6 RecoJets')
ax.set_xticks(x + width * (len(tagger_colors) - 1) / 2)
ax.set_xticklabels(jet_positions_6)
ax.legend()

plt.savefig(f"output/{sample_name}/jets_matched/6jet_matching_histograms.png", dpi=300)


 