# TDA-1-TP2
Teoría de Algoritmos 1 - 2c 2021 Trabajo Práctico 2

## requitistos
Solo se necesita python version >= 3.8

## uso del programa
simplemente ejecutar `python3 main.py $path_archivo_depositos` donde `$path_archivo_depositos` no es 
mas que el path al archivo de depositos que representa el grafo de ciudades con 
adyacencias y costos para esos caminos. El archivo usado para el informe fue `depositos_informe.txt`.

Para mas información ejecutar `python3 main.py --help`.

## (opcional) generacion de depositos
ejecutando `python3 gen_depositos.py $N` se genera un archivo `depositos.txt` con 
`$N` cantidad de ciudades (es un número). Sirve para probar el programa. No garantiza que 
el archivo resultante no tenga ciclos negativos ni que todas las ciudades sean alcanzables por algun 
camino. En esos casos se puede correr el programa de nuevo para obtener otro archivo distinto. 
Los archivos se generan al azar con cada ejeución pero se puede forzar la misma generación pasandole 
una semilla con el parámetro `-s`. En los casos que no se especifica, puede verse la semilla usada por la consola.

Tambien pueden cambiarse los rangos de maximo y minimo de costos asi como tambien 
la probabilidad de que, dado un grafo de `$N` ciudades completamente conexo, algun 
lado no este presente en el grafo generado si se modifican las constantes al principio del archivo 
`gen_depositos.py`.

para más información ejecutar `python3 gen_depositos.py --help`.