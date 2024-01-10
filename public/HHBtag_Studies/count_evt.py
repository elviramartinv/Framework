import ROOT
import os

path = "training_ntuples/"
patron = "*.root"

#f = "training_skim/GluGluToRadionToHHTo2B2Tau_M-270.root"

evt = 0
#evt_f = 0
#f_root = ROOT.TFile(f)
#tree_f = f_root.Get("Event")
#events_f = tree_f.GetEntries()
#evt_f += events_f

for archivo in os.listdir(path):
    if archivo.endswith(".root"):
        file_path = os.path.join(path, archivo)
        file_root = ROOT.TFile(file_path)
        tree = file_root.Get("Event")
        events = tree.GetEntries()
        evt += events

print("total events:", evt)
#print("total events:", evt_f)
