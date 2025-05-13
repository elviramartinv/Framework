void gen_studies() {

    // Abrir el archivo y cargar el árbol
    TFile *file = TFile::Open("/eos/user/e/emartinv/HHBtag_Training/training_skims_Run3_PNet/2022EE_GluGlutoHHto2B2Tau_SM.root");
    TTree *tree = (TTree*)file->Get("Event");

    // Crear un nuevo archivo para guardar los resultados
    TFile *outputFile = new TFile("/eos/user/e/emartinv/GenJet_Hbb_and_GenJet_Hbb_PF.root", "RECREATE");

    vector<int> *GenJet_Hbb = nullptr;
    vector<int> *GenJet_Hbb_PF = nullptr;

    // Crear las variables para leer las ramas del árbol
    tree->SetBranchAddress("GenJet_Hbb", &GenJet_Hbb);
    tree->SetBranchAddress("GenJet_Hbb_PF", &GenJet_Hbb_PF);

    Long64_t nEntries = tree->GetEntries();
    int match_info = 0;

    for (Long64_t i = 0; i < nEntries; ++i) {
        tree->GetEntry(i);

        bool isMatch = (GenJet_Hbb->size() == GenJet_Hbb_PF->size());
        if (isMatch) {
            for (size_t j = 0; j < GenJet_Hbb->size(); ++j) {
                if (GenJet_Hbb->at(j) != GenJet_Hbb_PF->at(j)) {
                    isMatch = false;
                    break;
                }
            }
        }

        if (isMatch) {
            ++match_info;
        }
    }

    // Imprimir por pantalla el numero de matches frente a numero de eventos
    cout << "Number of matches: " << match_info << " out of " << nEntries << " events" << endl;

    // Crear el primer lienzo
    TCanvas *c1 = new TCanvas("c1", "Canvas", 800, 600);

    // Dibujar la primera variable
    tree->Draw("GenJet_Hbb>>hist1", "", "HIST");
    TH1F *hist1 = (TH1F*)gPad->GetPrimitive("hist1");
    hist1->SetLineColor(kBlue); // Color de la primera variable
    hist1->SetTitle("");        // Quitar el título del gráfico
    hist1->GetXaxis()->SetTitle("match");  // Cambiar el título del eje x a "match"
    hist1->GetYaxis()->SetTitle("Events"); // Título del eje y
    hist1->SetStats(0);         // Quitar las estadísticas del histograma
    hist1->SetLineWidth(2);

    // Dibujar la segunda variable en el mismo canvas
    tree->Draw("GenJet_Hbb_PF>>hist2", "", "HIST SAME");
    TH1F *hist2 = (TH1F*)gPad->GetPrimitive("hist2");
    hist2->SetLineColor(kRed); // Color de la segunda variable
    hist2->SetStats(0);        // Quitar las estadísticas del histograma
    hist2->SetLineWidth(2);
    hist2->SetLineStyle(10);

    // Crear la leyenda
    auto legend = new TLegend(0.7, 0.8, 0.9, 0.9); // Posición de la leyenda
    legend->AddEntry(hist1, "GenJet_Hbb", "l");
    legend->AddEntry(hist2, "GenJet_Hbb_PF", "l");
    legend->Draw();

    // Añadir el conteo de cada bin en el histograma
    for (int i = 1; i <= hist1->GetNbinsX(); ++i) {
        int binContent1 = (int)hist1->GetBinContent(i);
        int binContent2 = (int)hist2->GetBinContent(i);

        double x = hist1->GetBinCenter(i);
        double y1 = binContent1 - 0.05 * binContent1;
        double y2 = binContent2 - 0.05 * binContent2;

        // Dibujar el texto con el número de entradas en cada bin
        TLatex latex;
        latex.SetTextAngle(90); // Rotar el texto 90 grados
        latex.SetTextSize(0.025);
        latex.SetTextColor(kBlue);
        latex.DrawLatex(x, y1, Form("%d", binContent1));
        latex.SetTextColor(kRed);
        latex.DrawLatex(x, y2, Form("%d", binContent2));
    }

    // Guardar el primer canvas en el archivo
    c1->Write();

    // Crear el segundo lienzo para la distribución de GenJet_Hbb cuando GenJet_Hbb_PF == 1
    TCanvas *c2 = new TCanvas("c2", "Canvas 2", 800, 600);
    
    // Filtrar los eventos donde GenJet_Hbb_PF == 1
    tree->Draw("GenJet_Hbb>>hist3", "GenJet_Hbb_PF == 1", "HIST");
    TH1F *hist3 = (TH1F*)gPad->GetPrimitive("hist3");
    hist3->SetLineColor(kGreen); // Color de la nueva variable
    hist3->SetTitle("GenJet_Hbb when GenJet_Hbb == 1");          // Quitar el título del gráfico
    hist3->GetXaxis()->SetTitle("Match"); // Título del eje x
    hist3->GetYaxis()->SetTitle("Events"); // Título del eje y
    hist3->SetStats(0);           // Quitar las estadísticas del histograma
    hist3->SetLineWidth(2);

        // Añadir el conteo de cada bin en el histograma de GenJet_Hbb cuando GenJet_Hbb_PF == 1
    for (int i = 1; i <= hist3->GetNbinsX(); ++i) {
        int binContent3 = (int)hist3->GetBinContent(i);
        double x = hist3->GetBinCenter(i);
        double y3 = binContent3 - 0.05 * binContent3; // Ajustar la posición del texto

        // Dibujar el texto con el número de entradas en cada bin, rotado 90 grados
        TLatex latex;
        latex.SetTextAngle(90); // Rotar el texto 90 grados
        latex.SetTextSize(0.025);
        latex.SetTextColor(kGreen);
        latex.DrawLatex(x, y3, Form("%d", binContent3)); // Texto del histograma
    }


    // Guardar el segundo canvas en el archivo
    c2->Write();

    TCanvas *c3 = new TCanvas("c3", "Canvas 3", 800, 600);

    // Filtrar los eventos donde GenJet_Hbb es igual a GenJet_Hbb_PF
    tree->Draw("GenJet_Hbb>>hist4", "GenJet_Hbb == GenJet_Hbb_PF", "HIST");
    TH1F *hist4 = (TH1F*)gPad->GetPrimitive("hist4");
    hist4->SetLineColor(kMagenta); // Color del nuevo histograma
    hist4->SetTitle("GenJet_Hbb == GenJet_Hbb_PF");            // Quitar el título del gráfico
    hist4->GetXaxis()->SetTitle("Match"); // Título del eje x
    hist4->GetYaxis()->SetTitle("Events"); // Título del eje y
    hist4->SetStats(0);       
    hist4->SetLineWidth(2);


    // Añadir el conteo de cada bin en el histograma
    for (int i = 1; i <= hist4->GetNbinsX(); ++i) {
        int binContent4 = (int)hist4->GetBinContent(i);
        double x = hist4->GetBinCenter(i);
        double y4 = binContent4 - 0.05 * binContent4; // Ajustar la posición del texto

        // Dibujar el texto con el número de entradas en cada bin, rotado 90 grados
        TLatex latex;
        latex.SetTextAngle(90); // Rotar el texto 90 grados
        latex.SetTextSize(0.025);
        latex.SetTextColor(kMagenta);
        latex.DrawLatex(x, y4, Form("%d", binContent4)); // Texto del histograma
    }


    auto legend3 = new TLegend(0.7, 0.8, 0.9, 0.9);
    legend3->AddEntry(hist4, "GenJet_Hbb == GenJet_Hbb_PF", "l");
    legend3->Draw();
    // Guardar el tercer canvas en el archivo
    c3->Write();


    TCanvas *c4 = new TCanvas("c4", "Canvas 4", 800, 600);

    // Dibujar deltaR_values cuando GenJet_Hbb == 1
    tree->Draw("deltaR_values>>hist5", "match_info == 0", "HIST");
    TH1F *hist5 = (TH1F*)gPad->GetPrimitive("hist5");
    hist5->SetLineColor(kOrange); // Color del histograma para GenJet_Hbb == 1
    hist5->SetTitle("DeltaR(genJet,genpart)");           // Quitar el título del gráfico
    hist5->GetXaxis()->SetTitle("deltaR_values"); // Título del eje x
    hist5->GetYaxis()->SetTitle("Events"); // Título del eje y
    hist5->SetStats(0);            // Quitar las estadísticas del histograma
    hist5->SetLineWidth(2);


    // Dibujar deltaR_values cuando GenJet_Hbb == 0
    tree->Draw("deltaR_values>>hist6", "match_info == 1", "HIST SAME");
    TH1F *hist6 = (TH1F*)gPad->GetPrimitive("hist6");
    hist6->SetLineColor(kBlue); // Color del histograma para GenJet_Hbb == 0
    hist6->SetStats(0);          // Quitar las estadísticas del histograma
    hist6->SetLineWidth(2);

    double maxY = hist6->GetMaximum(); // Obtener el máximo del histograma 5
    hist5->GetYaxis()->SetRangeUser(0, maxY * 1.1);

    // Crear la leyenda
    auto legend2 = new TLegend(0.7, 0.8, 0.9, 0.9); // Posición de la leyenda
    legend2->AddEntry(hist5, "DeltaR no match", "l");
    legend2->AddEntry(hist6, "DeltaR match", "l");
    legend2->Draw();

    hist5->GetXaxis()->SetRangeUser(0, 6); // Ajustar el rango del eje x

    // Guardar el cuarto canvas en el archivo
    c4->Write();

    // Crear un nuevo canvas para GenJet_Hbb cuando sea diferente de GenJet_Hbb_PF
    TCanvas *c5 = new TCanvas("c5", "Canvas 5", 800, 600);

    // Filtrar los eventos donde GenJet_Hbb es diferente de GenJet_Hbb_PF
    tree->Draw("GenJet_Hbb>>hist7", "GenJet_Hbb != GenJet_Hbb_PF", "HIST");
    TH1F *hist7 = (TH1F*)gPad->GetPrimitive("hist7");
    hist7->SetLineColor(kCyan); // Color del nuevo histograma
    hist7->SetTitle("GenJet_Hbb when GenJet_Hbb != GenJet_Hbb_PF"); // Título del gráfico
    hist7->GetXaxis()->SetTitle("Match"); // Título del eje x
    hist7->GetYaxis()->SetTitle("Events"); // Título del eje y
    hist7->SetStats(0); // Quitar las estadísticas del histograma
    hist7->SetLineWidth(2);

    // Dibujar el histograma para GenJet_Hbb cuando coincide con GenJet_Hbb_PF
    tree->Draw("GenJet_Hbb>>hist8", "GenJet_Hbb == GenJet_Hbb_PF", "HIST SAME");
    TH1F *hist8 = (TH1F*)gPad->GetPrimitive("hist8");
    hist8->SetLineColor(kMagenta); // Color del histograma para coincidencias
    hist8->SetLineWidth(2);

    // Añadir el conteo de cada bin en el nuevo histograma
    for (int i = 1; i <= hist7->GetNbinsX(); ++i) {
        int binContent7 = (int)hist7->GetBinContent(i);
        double x = hist7->GetBinCenter(i);
        double y7 = binContent7 - 0.05 * binContent7; // Ajustar la posición del texto

        // Dibujar el texto con el número de entradas en cada bin, rotado 90 grados
        TLatex latex;
        latex.SetTextAngle(90); // Rotar el texto 90 grados
        latex.SetTextSize(0.025);
        latex.SetTextColor(kCyan);
        latex.DrawLatex(x, y7, Form("%d", binContent7)); // Texto del histograma
    }

    // Añadir leyenda con conteos
    auto legend4 = new TLegend(0.7, 0.8, 0.9, 0.9);
    int totalMatch = 0; // Contador de coincidencias
    for (int i = 1; i <= hist8->GetNbinsX(); ++i) {
        totalMatch += hist8->GetBinContent(i);
    }
    int totalNonMatch = 0; // Contador de no coincidencias
    for (int i = 1; i <= hist7->GetNbinsX(); ++i) {
        totalNonMatch += hist7->GetBinContent(i);
    }
    legend4->AddEntry(hist7, Form("GenJet_Hbb != GenJet_Hbb_PF: %d events", totalNonMatch), "l");
    legend4->AddEntry(hist8, Form("GenJet_Hbb == GenJet_Hbb_PF: %d events", totalMatch), "l");
    legend4->Draw();

    // Guardar el quinto canvas en el archivo
    c5->Write();

    // Cerrar el archivo de salida
    outputFile->Close();
}


