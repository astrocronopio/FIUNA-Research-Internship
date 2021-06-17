# FI-UNA: Research Internship

        1- Primero necesitamos el archivo "path/to/muones.txt", ese usualmente tiene espacio entre cada línea. Esto no es muy recomendable porque lo uso el script Code/Sh/delete_spaces/sh para eliminarlos

        2- Luego hago el bineado de "path/to/muons_deleted_spaces.txt", puede hacerse así:
            
            * Con Code/Python/bin_muons.py donde hay que definir bines de cuantos vamos a trabajar


        3- El archivo del RTSW path/to/rtsw_plot_data.txt tiene más datos del que necesitamos, por lo que sacamos el header y ejecutamos el script Code/Sh/rtsw_data_utc_phi.sh, donde ahora solo quedan dos columnas: una con el horario UTC y otra del valor Phi, 

        4