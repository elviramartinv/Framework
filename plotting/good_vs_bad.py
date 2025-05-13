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


taggers = ["HHBtagScore_v3"]
# taggers = ["HHBtagScore", "btagPNetB", "btagDeepFlavB", "btagRobustParTAK4B"]
taggers_v2 = ["HHBtagScore_v2"]
tagger_colors = {
    "HHBtagScore_v3": "#900C3F",
    "HHBtagScore_v2": "#FF5733"
}
tagger_colors_3 = {
    "HHBtagScore_v3": "#375cd9",
    "HHBtagScore_v2": "#37d9c0"
}

tagger_legend_names = {
    "HHBtagScore_v3": "HHBtagScore_v3",
    "HHBtagScore_v2": "HHBtagScore_v2"
}


# plt.figure()
legend_elements = []

bins = np.linspace(0, 2, 41)

plt.figure(figsize=(10, 6))

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        print("eventos con 3 jets", df.Count().GetValue(), "para el tagger", tag)

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        print("good events", df_good.Count().GetValue())

        scores = df_bad.AsNumpy([f"FirstJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"FirstJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"FirstJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('First Jet Scores (misslabeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/FirstJet_bad.png", dpi=300)


plt.figure(figsize=(10, 6))

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df_good.AsNumpy([f"FirstJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"FirstJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"FirstJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('First Jet Scores (well-labeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/FirstJet_good.png", dpi=300)
plt.figure(figsize=(10, 6))

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df_bad.AsNumpy([f"SecondJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Second Jet Scores (misslabeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/SecondJet_bad.png", dpi=300)

plt.figure(figsize=(10, 6))
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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df_good.AsNumpy([f"SecondJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Second Jet Scores (well-labeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/SecondJet_good.png", dpi=300)

plt.figure(figsize=(10, 6))

plt.figure(figsize=(10, 6))
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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df.AsNumpy([f"SecondJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"SecondJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Second Jet Scores (well-labeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/SecondJet.png", dpi=300)

plt.figure(figsize=(10, 6))

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df_bad.AsNumpy([f"ThirdJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"ThirdJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"ThirdJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Third Jet Scores (misslabeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/ThirdJet_bad.png", dpi=300)
plt.figure(figsize=(10, 6))
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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores = df_good.AsNumpy([f"ThirdJet_{tag}"])
        color = tagger_colors[tag]
        # Pintar la distribución de los scores
        plt.hist(scores[f"ThirdJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color, label=f'{tag}')
        plt.hist(scores[f"ThirdJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color, label=f'{tag}')
        legend_label = tagger_legend_names[tag]
        legend_label = "HHBtagScore_v3" if tag == "HHBtagScore" else tag
        if legend_label not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color, edgecolor=color, alpha=1, linewidth=2, label=legend_label))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Third Jet Scores (well-labeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/ThirdJet_good.png", dpi=300)

plt.figure(figsize=(10, 6))
legend_elements = []

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores_second = df_good.AsNumpy([f"SecondJet_{tag}"])
        scores_third = df_good.AsNumpy([f"ThirdJet_{tag}"])
        color_second = tagger_colors[tag]
        color_third = tagger_colors_3[tag]
        

        # Pintar la distribución de los scores
        plt.hist(scores_second[f"SecondJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color_second, label=f'{tag} SecondJet')
        plt.hist(scores_second[f"SecondJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color_second, label=f'{tag} SecondJet')
        plt.hist(scores_third[f"ThirdJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color_third, linestyle='dashed', label=f'{tag} ThirdJet')
        plt.hist(scores_third[f"ThirdJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color_third, linestyle='dashed', label=f'{tag} ThirdJet')
        
        legend_label_second = tagger_legend_names[tag] + " SecondJet"
        legend_label_third = tagger_legend_names[tag] + " ThirdJet"
        
        if legend_label_second not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color_second, edgecolor=color_second, alpha=1, linewidth=2, label=legend_label_second))
        if legend_label_third not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color_third, edgecolor=color_third, alpha=1, linewidth=2, label=legend_label_third))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Third Jet Scores (well-labeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/SecondvsThirdJet_good.png", dpi=300)


plt.figure(figsize=(10, 6))
legend_elements = []

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
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")
        # print("eventos con 3 jets", df.Count().GetValue())

        df_bad = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 1")
        # print("bad events", df_bad.Count().GetValue())
        df_good = df.Filter(f"RecoJet_genMatched[idx_jets_{tag}[2]] == 0 && RecoJet_genMatched[idx_jets_{tag}[0]] == 1 && RecoJet_genMatched[idx_jets_{tag}[1]] == 1")
        # print("good events", df_good.Count().GetValue())

        scores_second = df_bad.AsNumpy([f"SecondJet_{tag}"])
        scores_third = df_bad.AsNumpy([f"ThirdJet_{tag}"])
        color_second = tagger_colors[tag]
        color_third = tagger_colors_3[tag]
        

        # Pintar la distribución de los scores
        plt.hist(scores_second[f"SecondJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color_second, label=f'{tag} SecondJet')
        plt.hist(scores_second[f"SecondJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color_second, label=f'{tag} SecondJet')
        plt.hist(scores_third[f"ThirdJet_{tag}"], bins=bins, alpha=0.2, histtype='stepfilled', color=color_third, linestyle='dashed', label=f'{tag} ThirdJet')
        plt.hist(scores_third[f"ThirdJet_{tag}"], bins=bins, alpha=1, histtype='step', color=color_third, linestyle='dashed', label=f'{tag} ThirdJet')
        
        legend_label_second = tagger_legend_names[tag] + " SecondJet"
        legend_label_third = tagger_legend_names[tag] + " ThirdJet"
        
        if legend_label_second not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color_second, edgecolor=color_second, alpha=1, linewidth=2, label=legend_label_second))
        if legend_label_third not in [elem.get_label() for elem in legend_elements]:
            legend_elements.append(Patch(facecolor=color_third, edgecolor=color_third, alpha=1, linewidth=2, label=legend_label_third))

    plt.xlabel('Score', fontsize=14)
    plt.xlim(0, 2)
    plt.ylabel('Events', fontsize=14)
    plt.yscale('log')
    plt.title('Third Jet Scores (misslabeled event)', fontsize=14)
    plt.legend(handles=legend_elements, loc='upper right', fontsize=14)
    plt.savefig(f"output/{sample_name}/scores_good_bad/SecondvsThirdJet_bad.png", dpi=300)
raise RuntimeError("Stop here")
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
