import os
import subprocess

# Directorio de origen con los archivos .root
source_dir = "/eos/home-f/fbrivio/HH_Run3/production_June_2024/PreprocessRDF/run3_2023_preBPix/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p00/cat_base/miniProd_24_06/"

# Directorio de destino para el archivo fusionado
dest_dir = "/eos/user/e/emartinv/HHBtag_Training/merged_Run3_signals/run3_2023_preBPix/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p00/"
dest_file = "data_0.root"

# Crear la lista de archivos .root en el directorio de origen
root_files = [os.path.join(source_dir, file) for file in os.listdir(source_dir) if file.endswith('.root')]

# Crear el comando hadd
hadd_command = ["hadd", "-f", os.path.join(dest_dir, dest_file)] + root_files

# Ejecutar el comando hadd
subprocess.run(hadd_command)