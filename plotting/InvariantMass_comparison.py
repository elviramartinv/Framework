import ROOT

# Declaración del código C++ en ROOT
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

samples = ["2022_GluGlutoHHto2B2Tau_SM.root", "2022_GluGlutoHHto2B2Tau_SM_v2.root"]
taggers = ["HHBtagScore_v3"]
taggers_v2 = ["HHBtagScore_v2"]


variables = ["pt", "eta", "phi", "mass"]

combined_canvas = ROOT.TCanvas("combined_canvas", "Combined Invariant Mass", 800, 600)

# Loop sobre muestras y taggers
for sample_idx, sample in enumerate(samples):
    if "_v2" in sample:
        taggers_loop = taggers_v2
    else:
        taggers_loop = taggers
    
    for tag in taggers_loop:
        f = p + sample
        df = ROOT.RDataFrame("Event", f)
        df = df.Filter("RecoJet_pt.size() >= 2")  

        # Definir índices de los jets
        df = df.Define('RecoJet_idx', 'CreateIndexes(RecoJet_pt.size())')
        # df = df.Define('GenJet_idx', 'CreateIndexes(GenJet_pt.size())')
        df = df.Define(f'idx_jets_{tag}', f'ReorderObjects(RecoJet_{tag}, RecoJet_idx)')
        df = df.Define(f'idx_jets_Hbb', f'ReorderObjects(GenJet_Hbb, GenJet_idx)')
        
        # Definir variables de los jets ordenados
        for v in variables:
            df = df.Define(f"recojet1_{v}_{tag}", f"RecoJet_{v}[idx_jets_{tag}[0]]")
            df = df.Define(f"recojet2_{v}_{tag}", f"RecoJet_{v}[idx_jets_{tag}[1]]")
            df = df.Define(f"genjet1_{v}_{tag}", f"genjet_{v}[idx_jets_{tag}[0]]")
            df = df.Define(f"genjet2_{v}_{tag}", f"genjet_{v}[idx_jets_{tag}[1]]")
            df = df.Define(f"goodgenjet1_{v}", f"genjet_{v}[idx_jets_Hbb[0]]")
            df = df.Define(f"goodgenjet2_{v}", f"genjet_{v}[idx_jets_Hbb[1]]")
            df = df.Define(f"matchedgenjet1_{v}_{tag}", f"(idx_jets_{tag}[0] == idx_jets_Hbb[0] || idx_jets_{tag}[0] == idx_jets_Hbb[1]) ? genjet_{v}[idx_jets_{tag}[0]] : -999")
            df = df.Define(f"matchedgenjet2_{v}_{tag}", f"(idx_jets_{tag}[1] == idx_jets_Hbb[0] || idx_jets_{tag}[1] == idx_jets_Hbb[1]) ? genjet_{v}[idx_jets_{tag}[1]] : -999")

        # Calcular la masa invariante reconstruida y generada
        df = df.Define(f"reco_inv_mass_{tag}", f"sqrt(2*recojet1_pt_{tag}*recojet2_pt_{tag}*(cosh(recojet1_eta_{tag}-recojet2_eta_{tag}) - cos(recojet1_phi_{tag}-recojet2_phi_{tag})))")
        df = df.Define(f"gen_inv_mass_{tag}", f"sqrt(2*genjet1_pt_{tag}*genjet2_pt_{tag}*(cosh(genjet1_eta_{tag}-genjet2_eta_{tag}) - cos(genjet1_phi_{tag}-genjet2_phi_{tag})))")
        df = df.Define(f"goodgen_inv_mass", f"sqrt(2*goodgenjet1_pt*goodgenjet2_pt*(cosh(goodgenjet1_eta-goodgenjet2_eta) - cos(goodgenjet1_phi-goodgenjet2_phi)))")
        df = df.Define(f"matchedgen_inv_mass_{tag}", f"(matchedgenjet1_pt_{tag} != -999 && matchedgenjet2_pt_{tag} != -999) ? sqrt(2*matchedgenjet1_pt_{tag}*matchedgenjet2_pt_{tag}*(cosh(matchedgenjet1_eta_{tag}-matchedgenjet2_eta_{tag}) - cos(matchedgenjet1_phi_{tag}-matchedgenjet2_phi_{tag}))) : -999")
        gen_count = df.Filter(f"gen_inv_mass_{tag} > 0").Count().GetValue()
        goodgen_count = df.Filter("goodgen_inv_mass > 0").Count().GetValue()
        matched_gen_count = df.Filter(f"matchedgen_inv_mass_{tag} > 0").Count().GetValue()

        canvas = ROOT.TCanvas(f"canvas_{tag}", f"Invariant Mass {tag}", 800, 600)

        h_gen_mass = df.Histo1D((f"gen_mass_{tag}", f"Gen Invariant Mass {tag}", 100, 0, 600), f"gen_inv_mass_{tag}")
        h_goodgen_mass = df.Histo1D(("goodgen_mass", "Good Gen Invariant Mass", 100, 0, 600), "goodgen_inv_mass")
        h_matchedgen_mass = df.Histo1D((f"matchedgen_mass_{tag}", f"Matched Gen Invariant Mass {tag}", 100, 0, 600), f"matchedgen_inv_mass_{tag}")

        # Asignar colores
        h_gen_mass.SetLineColor(ROOT.kBlue-4)
        h_goodgen_mass.SetLineColor(ROOT.kMagenta+2)
        h_matchedgen_mass.SetLineColor(ROOT.kMagenta-4)

        h_gen_mass.SetStats(False)
        h_goodgen_mass.SetStats(False)
        h_matchedgen_mass.SetStats(False)

        # Dibujar histogramas en el mismo canvas
        h_gen_mass.Draw()
        h_goodgen_mass.Draw("same")
        h_matchedgen_mass.Draw("same")

        max_y = max(h_gen_mass.GetMaximum(), h_goodgen_mass.GetMaximum(), h_matchedgen_mass.GetMaximum())

        # Ajustar el rango del eje Y de todos los histogramas al valor máximo encontrado
        h_gen_mass.SetMaximum(max_y * 1.1)  # Añadir un 10% de margen superior
        h_goodgen_mass.SetMaximum(max_y * 1.1)
        h_matchedgen_mass.SetMaximum(max_y * 1.1)

        # Añadir leyenda
        legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
        legend.SetTextSize(0.03)
        legend.AddEntry(h_gen_mass.GetValue(), f"Gen Mass ({gen_count})", "l")
        legend.AddEntry(h_goodgen_mass.GetValue(), f"Good Gen Mass ({goodgen_count})", "l")
        legend.AddEntry(h_matchedgen_mass.GetValue(), f"Matched Gen Mass ({matched_gen_count})", "l")
        legend.Draw()

        # Guardar el canvas
        canvas.SaveAs(f"InvariantMass_{tag}.png")


        # combined_canvas.cd()

        # # Dibujar histograma reconstruido
        # reco_hists[tag].SetLineColor(tagger_colors[tag])
        # reco_hists[tag].Draw("HIST SAME")
        
        # # Dibujar histograma generado
        # gen_hists[tag].SetLineColor(tagger_colors[tag])
        # gen_hists[tag].SetLineStyle(2)
        # gen_hists[tag].Draw("HIST SAME")

        # # Agregar leyenda al gráfico combinado
        # combined_legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
        # combined_legend.AddEntry(reco_hists["HHBtagScore_v3"].GetValue(), "Reco Inv Mass HHBtagScore_v3", "l")
        # combined_legend.AddEntry(gen_hists["HHBtagScore_v3"].GetValue(), "Gen Inv Mass HHBtagScore_v3", "l")
        # combined_legend.AddEntry(reco_hists["HHBtagScore_v2"].GetValue(), "Reco Inv Mass HHBtagScore_v2", "l")
        # combined_legend.AddEntry(gen_hists["HHBtagScore_v2"].GetValue(), "Gen Inv Mass HHBtagScore_v2", "l")
        # combined_legend.Draw()

        # # Guardar el gráfico combinado
        # combined_canvas.SaveAs("combined_invariant_mass_comparison.png")