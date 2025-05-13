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


variables = ["pt", "eta", "phi", "mass"]

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
        df = df.Filter("RecoJet_pt.size() >= 2")

        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f"FirstJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[0]]")
        df = df.Define(f"SecondJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[1]]")
        df = df.Define(f"ThirdJet_{tag}", f"RecoJet_{tag}[idx_jets_{tag}[2]]")

        for v in variables:
            df = df.Define(f"recojet1_{v}_{tag}", f"RecoJet_{v}[idx_jets_{tag}[0]]")
            df = df.Define(f"recojet2_{v}_{tag}", f"RecoJet_{v}[idx_jets_{tag}[1]]")
            df = df.Define(f"genjet1_{v}_{tag}", f"genjet_{v}[idx_jets_{tag}[0]]")
            df = df.Define(f"genjet2_{v}_{tag}", f"genjet_{v}[idx_jets_{tag}[1]]")
        
        df = df.Define(f"reco_inv_mass_{tag}", f"sqrt(2*recojet1_pt_{tag}*recojet2_pt_{tag}*(cosh(recojet1_eta_{tag}-recojet2_eta_{tag})-cos(recojet1_phi_{tag}-recojet2_phi_{tag})))")
        df = df.Define(f"gen_inv_mass_{tag}", f"sqrt(2*genjet1_pt_{tag}*genjet2_pt_{tag}*(cosh(genjet1_eta_{tag}-genjet2_eta_{tag})-cos(genjet1_phi_{tag}-genjet2_phi_{tag})))")
        
        reco_hist = df.Histo1D((f"reco_inv_mass_{tag}", f"Reco Inv Mass {tag}", 50, 0, 200), f"reco_inv_mass_{tag}")
        gen_hist = df.Histo1D((f"gen_inv_mass_{tag}", f"Gen Inv Mass {tag}", 50, 0, 200), f"gen_inv_mass_{tag}")

        # Convertir los histogramas en arrays para matplotlib
        reco_vals = np.array(reco_hist.GetBinContent())
        gen_vals = np.array(gen_hist.GetBinContent())

        # Superponer histogramas de masa invariante
        plt.hist(reco_vals, bins=bins, color=tagger_colors[tag], histtype='step', label=f'Reco {tag} {sample}', linewidth=2)
        plt.hist(gen_vals, bins=bins, color=tagger_colors[tag], histtype='step', label=f'Gen {tag} {sample}', linestyle='--', linewidth=2)

# Etiquetas y leyenda
plt.xlabel("Invariant Mass (GeV)")
plt.ylabel("Frequency")
plt.title("Invariant Mass: Reco vs Gen for Leading Jets")
plt.legend(loc='upper right')

# Guardar las figuras
plt.savefig("invariant_mass_comparison.png")
plt.show()


                

raise RuntimeError("Stop here")
        
        
 