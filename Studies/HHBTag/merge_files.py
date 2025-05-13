import os
import subprocess

# Directorio de origen con los archivos .root
source_dir = "/eos/home-f/fbrivio/HH_Run3/production_September_2024_forHHbtag/run3_2022_postEE/VBFHHto2B2Tau_CV-1_C2V-0_C3-1/cat_base/miniProd_24_10_16_forHHbtag/"

# Directorio de destino para el archivo fusionado
dest_dir = "/eos/user/e/emartinv/HHBtag_Training/merged_Run3_signals/run3_2022_postEE/VBFHHto2B2Tau_CV-1_C2V-0_C3-1/"
dest_file = "data_0.root"

# Crear la lista de archivos .root en el directorio de origen
root_files = [os.path.join(source_dir, file) for file in os.listdir(source_dir) if file.endswith('.root')]

# Crear el comando hadd
hadd_command = ["hadd", "-f", os.path.join(dest_dir, dest_file)] + root_files

# Ejecutar el comando hadd
subprocess.run(hadd_command)


# import os
# import subprocess

# # Directorio de origen con los archivos .root
# source_dir = "/eos/home-f/fbrivio/HH_Run3/production_September_2024_forHHbtag/run3_2022_postEE/VBFHHto2B2Tau_CV-1_C2V-0_C3-1/cat_base/miniProd_24_10_16_forHHbtag/"

# # Directorio de destino para los archivos fusionados
# dest_dir = "/eos/user/e/emartinv/HHBtag_Training/merged_Run3_signals/run3_2022_postEE/VBFHHto2B2Tau_CV-1_C2V-0_C3-1/"
# dest_file_1 = "data_0.root"
# dest_file_2 = "data_1.root"

# # Crear la lista de archivos .root en el directorio de origen
# root_files = [os.path.join(source_dir, file) for file in os.listdir(source_dir) if file.endswith('.root')]

# # Dividir la lista de archivos en dos partes
# mid_index = len(root_files) // 2
# root_files_part1 = root_files[:mid_index]
# root_files_part2 = root_files[mid_index:]

# # Crear y ejecutar el primer comando hadd para la primera mitad de los archivos
# hadd_command_part1 = ["hadd", "-f", os.path.join(dest_dir, dest_file_1)] + root_files_part1
# subprocess.run(hadd_command_part1)

# # Crear y ejecutar el segundo comando hadd para la segunda mitad de los archivos
# hadd_command_part2 = ["hadd", "-f", os.path.join(dest_dir, dest_file_2)] + root_files_part2
# subprocess.run(hadd_command_part2)
