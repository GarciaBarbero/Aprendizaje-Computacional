package com.company;

import java.util.ArrayList;
import java.util.List;

public class Funciones {
    /**
     * @param tag etiqueta a evaluar
     * @param value_tag Valor de la etiqueta a evaluar
     * @param tag2 etique sobre la que se evalua
     * @param tabla Tablas
//     * @param base_log base del logaritmo
     * */
    public static double entropia(Tablas tabla, String tag, String value_tag, String tag2){
        List<String> valuesOfTag = tabla.getValuesOfTags(tag2);
        double resultado = 0 ;
        for (String s : valuesOfTag) {
            resultado += entropia(tabla, tag, value_tag, tag2, s);
        }
        return resultado;
    }

    public static double entropia(Tablas tabla, String tag, String value_tag, String tag2, String value_tag2){
        try {
            double population = (tabla.countValueTagCondition(tag,value_tag, tag2, value_tag2)/tabla.countValue(tag, value_tag));
            return (population)+Math.log(population);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
            return -1;
        }
    }

    public static double entropia(Tablas tabla, String tag){
        try {
            long population = tabla.getPopulation();
            List<String> valuesOfTag = tabla.getValuesOfTags(tag);
            double resultado = 0;
            for (String s : valuesOfTag) {
                double particion = tabla.countValue(tag, s)/population;
                resultado += particion + Math.log(particion);
            }
            return resultado;

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
            return -1;
        }
    }


}
