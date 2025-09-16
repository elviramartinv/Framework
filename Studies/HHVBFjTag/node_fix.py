import ROOT
from array import array
import os
import sys
# Abrir el archivo ROOT en modo UPDATE
input_path = "/eos/user/e/emartinv/vbfjets_Training/training_skims_cclub/2022EE_VBFHHto2B2Tau_CV_1_C2V_1_kl_1.root"
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file {input_path} does not exist.")

file = ROOT.TFile.Open(input_path, "UPDATE")
tree = file.Get("Event")

# Crear un nuevo archivo para almacenar los datos modificados
new_file = ROOT.TFile("/eos/user/e/emartinv/vbfjets_Training/training_skims_cclub_correct/2022EE_VBFHHto2B2Tau_CV_1_C2V_1_C3_1.root", "RECREATE")
new_tree = tree.CloneTree(0)  # Clonar el árbol sin copiar los eventos aún

# Variable para almacenar el valor de node_index
node_index_correct = array('i', [9])

# Asociar la variable a la rama existente
new_tree.Branch("node_index_correct", node_index_correct, "node_index_correct/I")

# Iterar sobre los eventos y modificar el valor de node_index_correct
for i in range(tree.GetEntries()):
    tree.GetEntry(i)
    node_index_correct[0] = 9
    new_tree.Fill()

# Guardar los cambios en el nuevo archivo
new_tree.Write()
new_file.Close()
file.Close()


####
# 1-1-1: 0
# 1-0-1: 1
# 1.74-1.37-14.4: 2
# -0.012-0.030-10.2: 3
# -0.758-1.44--19.3: 4
# -0.962-0.959--1.43: 5
# -1.21-1.94--0.94: 6
# -1.60-2.72--1.36: 7
# -1.83-3.57--3.39: 8
# -2.12-3.87--5.96: 9
