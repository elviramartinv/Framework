import ROOT
import json
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.stats.proportion import proportion_confint

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

def save_root(df, filename, columns_to_save):
  df.Snapshot("Events", filename, columns_to_save)

  columns_to_save = ["HHBtagScore_FirstTwoJetsMatched","btagDeepFlavB_FirstTwoJetsMatched", "particleNetAK4_B_FirstTwoJetsMatched",
  "idx_jets_btagDeepFlavB", "idx_jets_particleNetAK4_B", "idx_jets_HHBtagScore", 
  "GenJet_b_PF", "RecoJet_btagDeepFlavB", "RecoJet_particleNetAK4_B", "RecoJet_HHBtagScore"]



p = "/afs/cern.ch/user/e/emartinv/public/cms-hh-bbtautau/Framework/newHH/"
HH_nonres_SM = "GluGluToHHTo2B2Tau_node_SM_2018.root"
HH_res_250 = "GluGluToRadionToHHTo2B2Tau_M-250_2018.root"
HH_res_500 = "GluGluToRadionToHHTo2B2Tau_M-500.root"
HH_res_1000 =  "GluGluToRadionToHHTo2B2Tau_M-1000.root"
HH_res_1500 = "GluGluToRadionToHHTo2B2Tau_M-1500.root"
HH_res_3000 = "GluGluToRadionToHHTo2B2Tau_M-3000.root"
TT = "TTToSemiLeptonic_nano_0.root"
DY = "DYJetsToLL_M-50_nano_0.root"

samples = [HH_nonres_SM, HH_res_250,HH_res_500, HH_res_1000, HH_res_1500, HH_res_3000, TT, DY]
samples_names = ["HH nonres SM", "HH res 250","HH res 500", "HH res 1000", "HH res 1500", "HH res 3000", "TT dileptonic", "DY"]
efficiencies = {}
missID_rate = {}
for sample in samples:
  file = p + sample
  df = ROOT.RDataFrame("Event", file)
  # df = df.Range(30)
  df = df.Filter("RecoJet_pt.size() >= 2")
  num_evt = df.Count()
  df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
  taggers = ["btagDeepFlavB", "particleNetAK4_B", "HHBtagScore"]

  efficiencies[sample] = {}
  missID_rate[sample] = {}

  for tagger in taggers:
      df = df.Define(f'idx_jets_{tagger}', f'ReorderObjects(RecoJet_{tagger}, RecoJet_idx)') 
      df = df.Define(f"{tagger}_FirstTwoJetsMatched", f"RecoJet_idx.size() >= 2 && GenJet_b_PF[idx_jets_{tagger}[0]] == 1 && GenJet_b_PF[idx_jets_{tagger}[1]] == 1")
      df = df.Define(f"{tagger}_FirstTwoJetsNotMatched", f"RecoJet_idx.size() >= 2 && (GenJet_b_PF[idx_jets_{tagger}[0]] != 1 || GenJet_b_PF[idx_jets_{tagger}[1]] != 1)")
      
      success_count = df.Filter(f"{tagger}_FirstTwoJetsMatched").Count()
      # print(f"Success count for {tagger}: {success_count.GetValue()}")
      missID_count = df.Filter(f"{tagger}_FirstTwoJetsNotMatched").Count()
      # print(f"MissID count for {tagger}: {missID_count.GetValue()}")

      efficiency = float(success_count.GetValue()) / df.Count().GetValue()
      # print(f"Efficiency for {tagger}: {efficiency}")
      missID = float(missID_count.GetValue()) / df.Count().GetValue()
      # print(f"MissID for {tagger}: {missID}")
  
      lower, upper = proportion_confint(success_count.GetValue(), df.Count().GetValue(), alpha = 0.68, method='beta')
      error_lower = efficiency - lower
      error_upper = upper - efficiency
      # print(f"Lower: {error_lower}, Upper: {error_upper}")
      efficiencies[sample][tagger] = {"efficiency": efficiency, "err_low": error_lower, "err_up": error_upper}

      lower_miss, upper_miss = proportion_confint(missID_count.GetValue(), df.Count().GetValue(), alpha = 0.68, method='beta')
      error_lower_miss = missID - lower_miss
      error_upper_miss = upper_miss - missID
      # print(f"Lower: {error_lower_miss}, Upper: {error_upper_miss}")
      missID_rate[sample][tagger] = {"missID": missID, "err_low": error_lower_miss, "err_up": error_upper_miss}
  # save_to_root(df,f"{sample}.root", columns_to_save)

with open("output/effi.json", "w") as f:
    json.dump(efficiencies, f)
with open("output/missID.json", "w") as f:
    json.dump(missID_rate, f)

# df.Snapshot("Events", "TTToHadronic.root", columns_to_save)

def create_table(efficiencies, sample_names):
  # for sample in efficiencies:
  #     for tagger in efficiencies[sample]:
  #         efficiencies[sample][tagger]['efficiency'] = round(efficiencies[sample][tagger]['efficiency'] * 100, 2)
  efficiencies_only = {sample_names[i]: {tagger: "{:.2f}%".format(efficiencies[sample][tagger]['efficiency'] * 100) for tagger in efficiencies[sample]} for i, sample in enumerate(efficiencies)}  
  df = pd.DataFrame(efficiencies_only).T
  fig, ax = plt.subplots(figsize=(10,6))
  ax.axis('off')
  table = plt.table(cellText=df.values, 
  colLabels=df.columns, rowLabels=df.index, cellLoc = 'center', loc='center')

  table.auto_set_font_size(False)
  table.set_fontsize(10)
  table.scale(0.9, 1.5)

  cells = table.get_celld()
  for i in range(len(df.columns)):
      cells[0, i].set_facecolor('#7f74b5')
      cells[0, i].set_text_props(weight='bold', color='w')

  plt.savefig('output/efficiencies_table.png', dpi=300)

create_table(efficiencies, samples_names)

