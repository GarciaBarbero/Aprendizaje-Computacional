package com.company;

import java.util.ArrayList;
import java.util.List;

public class Funciones {
    /**
     * @param tag etiqueta a evaluar
     * @param value_tag Valor de la etiqueta a evaluar
     * @param tag2 etique sobre la que se evalúa
     * @param tabla Tablas
//     * @param base_log base del logaritmo
     * */
    public static double entropy(Tablas tabla, String tag, String value_tag, String tag2){
        List<String> valuesOfTag = tabla.getValuesOfTags(tag2);
        double result = 0 ;
        for (String s : valuesOfTag) {
            result += entropy(tabla, tag, value_tag, tag2, s);
        }
        return result;
    }

    public static double entropy(Tablas tabla, String tag, String value_tag, String tag2, String value_tag2){
        try {
            double population = (tabla.countValueTagCondition(tag,value_tag, tag2, value_tag2)/tabla.countValue(tag, value_tag));
            return (population)+Math.log(population);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
            return -1;
        }
    }

    public static double entropy(Tablas tabla, String tag){
        try {
            long population = tabla.getPopulation();
            List<String> valuesOfTag = tabla.getValuesOfTags(tag);
            double result = 0;
            for (String s : valuesOfTag) {
                double partition = tabla.countValue(tag, s)/population;
                result  += partition + Math.log(partition);
            }
            return result ;

        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
            return -1;
        }
    }


}
