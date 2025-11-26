#!/bin/bash
#################################################################################
#  Script Bash para ejecutar el job CNBV_EEFF_Main.py con 5 parámetros
#  específicos y gestionar los logs de salida y error.
#  Nombre: Estados Financieros de la CNBV
#  Autor: Steve Carpio
#  Fecha: 2025-11-26
#################################################################################

# === CONFIGURACIÓN GENERAL ===
NOMBRE_BASH="CNBV_EEFF"
NOMBRE_JOB="CNBV_EEFF_Main.py"
RUTA_JOB="/home/robot/Python/proy_py_cnbv_eeff/"
RUTA_LOG="/srv/apps/MisCompilados/PROY_CNBV_EEFF/LOG/"
PAR1=$1                             # ENTORNO:          [DEV, PRO]
case "$2" in                        # TIPO DE DESCARGA: [1=Trimestral, 2=Mensual, 3=Anual]
    1) PAR2="Trime";;
    2) PAR2="Mensual";;
    3) PAR2="Anual";;
    *) PAR2="Desconocido";;
esac
PAR3=$3                             # TRIMESTRE ANUAL:  [1, 2, 3, 4, 4D]
PAR4=$4                             # AÑO DE EJERCICIO: [2020 <--> 2023]
PAR5=$5                             # TIPO DE FICHEROS: [1=Excel, 2=Pdf]  
DIAS=0


# === DEFINE FECHA DE EJECUCIÓN RESTANDO DIAS Y DEFINE LOG DE SALIDA ===
fecha=$(date -d "$DIAS days ago" +%F)
exe="${RUTA_JOB}src_lnx/$NOMBRE_JOB"
logBase="${RUTA_LOG}${NOMBRE_BASH}_${PAR2}_${PAR3}_${PAR4}_${PAR5}__${PAR1}_${fecha}"

# === ACTIVAR ENTORNO VIRTUAL ===
source "${RUTA_JOB}venv/bin/activate"

# === CONFIGURAR TERM ===
export TERM=xterm      # Para que no de un mensaje de error en la log "err", desde cron no encuentra esta variable 
# o: export TERM=dumb

# === EJECUCIÓN DEL SCRIPT ===
ahora=$(date +"%Y-%m-%d %H.%M")
runjob="python3 $exe $PAR1 $2 $PAR3 $PAR4 $PAR5"
echo "$ahora: Ini bash ${NOMBRE_BASH}.sh: $runjob" 
python3 "$exe" "$PAR1" "$2" "$PAR3" "$PAR4" "$PAR5" > "${logBase}_out.log" 2> "${logBase}_err.log"
ahora=$(date +"%Y-%m-%d %H.%M")
echo "$ahora: Fin bash ${NOMBRE_BASH}.sh: $runjob" 

# === DESACTIVAR ENTORNO VIRTUAL ===
#deactivate