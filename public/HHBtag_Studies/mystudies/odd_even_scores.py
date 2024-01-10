import ROOT
import numpy as np

def create_histograms(input_file, output_file):
    # Abre el archivo root
    df = ROOT.RDataFrame("Event", input_file)

    # Filtra los eventos pares e impares
    df_even = df.Filter("event % 2 == 0")
    df_odd = df.Filter("event % 2 != 0")

    df_even = df_even.Define("RecoJet_HHBtagScore_first", "RecoJet_HHBtagScore[0]")
    df_odd = df_odd.Define("RecoJet_HHBtagScore_first", "RecoJet_HHBtagScore[0]")


    # Crea histogramas para los eventos pares e impares
    h_even = df_even.Histo1D(("hhbtag_score_even", "HHBtag Score - Events Pares", 100, 0.5, 1.5), "RecoJet_HHBtagScore_first")
    h_odd = df_odd.Histo1D(("hhbtag_score_odd", "HHBtag Score - Events Impares", 100, 0.5, 1.5), "RecoJet_HHBtagScore_first")

    # Pinta los histogramas
    c = ROOT.TCanvas("c", "HHBtag Score", 800, 600)
    h_even.SetLineColor(ROOT.kBlue)
    h_odd.SetLineColor(ROOT.kRed)

    h_even.Draw()
    h_odd.Draw("SAME")

    # Muestra la leyenda
    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)
    legend.AddEntry(h_even.GetPtr(), "Even par", "l")
    legend.AddEntry(h_odd.GetPtr(), "Odd par", "l")
    legend.Draw()

    c.Draw()

    c.SaveAs(output_file)
    print(f"Plot guardado en: {output_file_path}")

if __name__ == "__main__":
    # Especifica la ruta del archivo nano.root
    input_file_path = "/afs/cern.ch/user/e/emartinv/public/Ntuple_prod/newHH_ntuples/GluGluToRadionToHHTo2B2Tau_M-250.root"
    output_file_path = f"/afs/cern.ch/user/e/emartinv/public/Ntuple_prod/mystudies/output/GluGluToRadionToHHTo2B2Tau_M-250.pdf"
    # Llama a la función para crear histogramas y pintar distribuciones
    create_histograms(input_file_path, output_file_path)


