#include <TSystemDirectory.h>
#include <TSystemFile.h>
#include <TList.h>
#include <TCollection.h>
#include <vector>
#include <iostream>

void total_n_matches() {
    // Carpeta que contiene los archivos .root
    TString dirPath = "/eos/user/e/emartinv/HHBtag_Training/training_skims_Run3_PNet/";

    // Objeto para el directorio
    TSystemDirectory dir(dirPath, dirPath);
    TList *files = dir.GetListOfFiles();
    
    if (!files) {
        std::cerr << "Error: No se pudo abrir el directorio o no contiene archivos." << std::endl;
        return;
    }

    int totalMatchInfo = 0;
    Long64_t totalEntries = 0;

    // Recorre todos los archivos en la carpeta
    TIter next(files);
    TSystemFile *file;
    while ((file = (TSystemFile*)next())) {
        TString fileName = file->GetName();
        
        // Procesa solo archivos con extensión .root
        if (!file->IsDirectory() && fileName.EndsWith(".root")) {
            TString filePath = dirPath + fileName;
            std::cout << "Procesando archivo: " << filePath << std::endl;

            // Abre el archivo y carga el árbol
            TFile *rootFile = TFile::Open(filePath);
            if (!rootFile || rootFile->IsZombie()) {
                std::cerr << "Error al abrir el archivo: " << filePath << std::endl;
                continue;
            }

            TTree *tree = (TTree*)rootFile->Get("Event");
            if (!tree) {
                std::cerr << "No se encontró el árbol 'Event' en el archivo: " << filePath << std::endl;
                rootFile->Close();
                continue;
            }

            // Variables para almacenar ramas
            std::vector<int> *GenJet_Hbb = nullptr;
            std::vector<int> *GenJet_Hbb_PF = nullptr;
            tree->SetBranchAddress("GenJet_Hbb", &GenJet_Hbb);
            tree->SetBranchAddress("GenJet_Hbb_PF", &GenJet_Hbb_PF);

            Long64_t nEntries = tree->GetEntries();
            int matchInfo = 0;

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
                    ++matchInfo;
                }
            }

            // Acumula el total de coincidencias y eventos de todos los archivos
            totalMatchInfo += matchInfo;
            totalEntries += nEntries;

            // Cierra el archivo después de procesarlo
            rootFile->Close();
        }
    }

    // Imprimir el número total de coincidencias frente al total de eventos
    std::cout << "Número total de coincidencias: " << totalMatchInfo << " de " << totalEntries << " eventos en todos los archivos." << std::endl;
}
