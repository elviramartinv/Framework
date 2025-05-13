import ROOT
import glob

# Define la ruta de la carpeta que contiene los archivos .root
folder_path = "/eos/user/e/emartinv/HHBtag_Training/training_skims_Run3_PNet/"
file_paths = glob.glob(f"{folder_path}/*.root")  # Lista de todos los archivos .root en la carpeta

# Declara el código C++ en ROOT
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

variables = ["pt", "eta", "phi", "mass"]

# Define el RDataFrame usando todos los archivos .root
df = ROOT.RDataFrame("Event", file_paths)

# Define índices de los jets
# df = df.Define('GenJet_idx', 'CreateIndexes(GenJet_pt.size())')
df = df.Define(f'idx_genjets_Hbb', f'ReorderObjects(GenJet_Hbb, GenJet_idx)')
df = df.Define(f'idx_genjets_Hbb_PF', f'ReorderObjects(GenJet_Hbb_PF, GenJet_idx)')
df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
df = df.Define(f'idx_recojets_Hbb', f'ReorderObjects(RecoJet_genMatched, RecoJet_idx)')

# Define variables de los jets ordenados
for v in variables:
    df = df.Define(f"genjet1_hbb_{v}", f"genjet_{v}[idx_genjets_Hbb[0]]")
    df = df.Define(f"genjet2_hbb_{v}", f"genjet_{v}[idx_genjets_Hbb[1]]")
    df = df.Define(f"genjet1_hbb_pf_{v}", f"genjet_{v}[idx_genjets_Hbb_PF[0]]")
    df = df.Define(f"genjet2_hbb_pf_{v}", f"genjet_{v}[idx_genjets_Hbb_PF[1]]")
    df = df.Define(f"recojet1_hbb_{v}", f"RecoJet_{v}[idx_recojets_Hbb[0]]")
    df = df.Define(f"recojet2_hbb_{v}", f"RecoJet_{v}[idx_recojets_Hbb[1]]")

# Calcula la masa invariante reconstruida y generada
df = df.Define("gen_inv_mass_hbb", "sqrt(2*genjet1_hbb_pt*genjet2_hbb_pt*(cosh(genjet1_hbb_eta-genjet2_hbb_eta) - cos(genjet1_hbb_phi-genjet2_hbb_phi)))")
df = df.Define("gen_inv_mass_hbb_pf", "sqrt(2*genjet1_hbb_pf_pt*genjet2_hbb_pf_pt*(cosh(genjet1_hbb_pf_eta-genjet2_hbb_pf_eta) - cos(genjet1_hbb_pf_phi-genjet2_hbb_pf_phi)))")
df = df.Define("reco_inv_mass_hbb", "sqrt(2*recojet1_hbb_pt*recojet2_hbb_pt*(cosh(recojet1_hbb_eta-recojet2_hbb_eta) - cos(recojet1_hbb_phi-recojet2_hbb_phi)))")

# Filtrar y contar eventos
hbb_count = df.Filter("gen_inv_mass_hbb > 0").Count().GetValue()
print("gen count", hbb_count)
hbb_pf_count = df.Filter("gen_inv_mass_hbb_pf > 0").Count().GetValue()
print("gen PF count", hbb_pf_count)
hbb_reco_count = df.Filter("reco_inv_mass_hbb > 0").Count().GetValue()
print("reco count", hbb_reco_count)

# Crear canvas y dibujar los histogramas
canvas = ROOT.TCanvas(f"canvas", f"Invariant Mass", 800, 600)

# Crear histogramas
h_gen_mass = df.Histo1D(("gen_mass_hbb", "Gen Invariant Mass Hbb", 50, 0, 300), "gen_inv_mass_hbb")
h_gen_mass_pf = df.Histo1D(("gen_mass_hbb_pf", "Gen Invariant Mass Hbb PF", 50, 0, 300), "gen_inv_mass_hbb_pf")
h_reco_mass = df.Histo1D(("reco_inv_mass_hbb", "Reco Invariant Mass Hbb", 50, 0, 300), "reco_inv_mass_hbb")

# h_gen_mass.SetTitle("Invariant Mass Hbb")
h_gen_mass.GetXaxis().SetTitle("Invariant Mass [GeV]")
h_gen_mass.GetYaxis().SetTitle("Events")

# Configurar el estilo de los histogramas
h_gen_mass.SetLineColor(ROOT.kBlue-4)
h_gen_mass_pf.SetLineColor(ROOT.kMagenta)
h_gen_mass_pf.SetLineStyle(10)
h_reco_mass.SetLineColor(ROOT.kOrange+7)
h_reco_mass.SetLineStyle(2)

# Ocultar estadísticas
h_gen_mass.SetStats(False)
h_gen_mass_pf.SetStats(False)
h_reco_mass.SetStats(False)

# Dibujar histogramas en el mismo canvas
h_gen_mass.Draw()
h_gen_mass_pf.Draw("same")
# h_reco_mass.Draw("same")

# Ajustar el rango máximo del eje Y
max_y = max(h_gen_mass.GetMaximum(), h_gen_mass_pf.GetMaximum(), h_reco_mass.GetMaximum())
h_gen_mass.SetMaximum(max_y * 1.1)

# Añadir leyenda
legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
legend.SetTextSize(0.03)
legend.AddEntry(h_gen_mass.GetValue(), f"Gen Mass Hbb", "l")
legend.AddEntry(h_gen_mass_pf.GetValue(), f"Gen Mass Hbb PF", "l")
# legend.AddEntry(h_reco_mass.GetValue(), f"Reco Mass Hbb", "l")
legend.Draw()

# Guardar el canvas
canvas.SaveAs(f"InvariantMass.png")
