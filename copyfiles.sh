#!/bin/sh

# Directorio de entrada en el CERN
inputDir="/eos/user/e/emartinv/cmt/MergeCategorization/run3_2022_preEE/TTto2L2Nu/"

# Directorio de salida en el CIEMAT
outputDir="root://gaexrdoor.ciemat.es//store/user/emartinv/MergeCategorization/run3_2022_preEE/TTto2L2Nu"

# Recorre los subdirectorios y archivos en inputDir y copia cada archivo .root al directorio de salida
for file in $(find ${inputDir} -name "*.root"); do
    # Genera la ruta de destino correspondiente
    subpath=${file#${inputDir}}  # Extrae la ruta relativa a partir de inputDir
    dest=${outputDir}${subpath}

    # Crea el subdirectorio en la salida
    xrdmkdir -p "$(dirname ${dest})"

    # Copia el archivo al destino en CIEMAT
    /usr/bin/xrdcp ${file} ${dest}
done
