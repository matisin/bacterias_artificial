#!/bin/bash
rm resultados.txt
for archivoActual in $(ls -l A-VRP/ | awk '{print $9}');do
    echo $archivoActual >> resultados.txt
    for i in {1..15}
    do
        python2.7 algoritmo.py 5 75 25 75 25 100 50 100 600000 A-VRP/$archivoActual
    done
done
