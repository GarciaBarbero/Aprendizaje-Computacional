package com.company;

import javafx.util.Pair;

import java.util.*;
import java.util.stream.Collectors;

/*
╔════════════════════════════════════════════════════════════════════╗
║							Tabla  									 ║
╠════════╦═══════════╦═══════════╦═══════════╦══════════╦════════════╣
║ Nobres ║ Etiqueta1 ║ Etiqueta2 ║ Etiqueta3 ║ 	...		║ Etiqueta n ║
╠════════╬═══════════╬═══════════╬═══════════╬══════════╬════════════╣
║ Nobre1 │ Eti.Value │ Eti.Value │ Eti.Value │	...		│ Eti.Value	 ║
╠────────┼───────────┼───────────┼───────────┼──────────┼────────────╣
║ Nobre2 │ Eti.Value │ Eti.Value │ Eti.Value │	...		│ Eti.Value	 ║
╠────────┼───────────┼───────────┼───────────┼──────────┼────────────╣
║ Nobre3 │ Eti.Value │ Eti.Value │ Eti.Value │	...		│ Eti.Value	 ║
╠────────┼───────────┼───────────┼───────────┼──────────┼────────────╣
║ Nobre4 │ Eti.Value │ Eti.Value │ Eti.Value │	...		│ Eti.Value	 ║
╚════════╩═══════════╩═══════════╩═══════════╩══════════╩════════════╝
*/
public class Tablas {
  private List<List<String>> Tabla = new ArrayList<List<String>> ();
  private List<String> Tags = new ArrayList<String> ();
  private List<String> Name = new ArrayList<String> ();
  private Map<String, List<String>> ValuesOfTags = new HashMap<String, List<String>>();

//  TODO backtracking
//  private Tablas PARENT = null;
//  private Tablas CHILDREN = null;

//  public Tablas(List<List<String>> tabla, List<String> etiquetas, List<String> nombre, Map<String, List<String>> valuesOfTags) {
//    this.tabla = tabla.stream().map(ArrayList::new).collect(Collectors.toList());
//    this.etiquetas = new ArrayList<String>(etiquetas);
//    this.nombre = new ArrayList<String>(nombre);
//    this.ValuesOfTags = new HashMap<String, List<String>>(valuesOfTags);
//  }
//
//  public Tablas(Tablas parent){
//    this.Tabla =  parent.getTabla();
//    this.Tags = parent.getTags();
//    this.Name = parent.getName();
//    this.ValuesOfTags = parent.getValuesOfTags();
//    this.PARENT = parent;
//  }

  public Tablas(String Tags) {
    this.Tags = split(Tags);
    for (int i = 1; i < this.Tags.size(); i++) {
      this.ValuesOfTags.put(this.Tags.get(i), new ArrayList<String>());
    }
  }

  public void setValue(String dataInput){
    List<String> data = split(dataInput);
    this.Name.add(data.remove(0));
    this.Tabla.add(data);
    for (int i = 0; i < data.size(); i++) {
      List<String> listValueTag = this.ValuesOfTags.get(this.Tags.get(i+1));
      if(!listValueTag.contains(data.get(i))) listValueTag.add(data.get(i));
      this.ValuesOfTags.put(this.Tags.get(i+1), listValueTag);
    }
  }

  public long countValue(String tag, String tag_value) throws Exception {
    int column = this.getIndexTag(tag);

    return this.Tabla.stream().filter(s -> s.get(column).equals(tag_value)).count();
  }

  public long countValueTagCondition(String tag1, String tag_value1, String tag2, String tag_value2) throws Exception {
    int column1 = this.getIndexTag(tag1);
    int column2 = this.getIndexTag(tag2);

    return this.Tabla.stream().filter(s -> (s.get(column1).equals(tag_value1))&&(s.get(column2).equals(tag_value2))).count();
  }

  //    Todo: Alomejor puede ser más eficiente.
  public void removeColumnTag(String tag) throws Exception {
    int column = this.getIndexTag(tag);
    this.Tags.remove(column+1);
    this.Tabla.forEach(strings -> strings.remove(column));
    this.ValuesOfTags.remove(tag);
//    System.out.println(tabla);
  }

  public void removeRowValueTag(String tag, String tag_value) throws Exception {
    Pair<List<String>, List<List<String>>> values = this.filterRowsValue(tag, tag_value);
    values.getKey().forEach(integer -> this.Name.remove(integer));
    values.getValue().forEach(strings -> this.Tabla.remove(strings));
//    this.tabla = this.tabla.stream().filter(strings -> !strings.contains(tag_value)).collect(Collectors.toList());
    this.removeDuplicateValue();
  }

  private int getIndexTag(String tag) throws Exception {
    int column = this.Tags.indexOf(tag)-1;
    if (column < 0) throw new Exception("No existe la tag: " + tag);
    return column;
  }

  private void removeDuplicateValue(){
    int numOfTag = this.Tags.size()-1;
    for (int i = 0; i < numOfTag; i++) {
      int finalI = i;
      List<String> listValueTag = new ArrayList<String>(new LinkedHashSet<>(this.Tabla.stream().map(strings -> strings.get(finalI)).collect(Collectors.toList())));
      this.ValuesOfTags.replace(this.Tags.get(i+1), listValueTag);
    }
  }

  /**
   * <p> Selecciona las filas que contiene la el valor con la etiqueta asignada </p>
   * @return <p>  <p> Pair< List < Integer >, List < List < String > > > </p>
   *              <p> Key: posición del nombre en la lista de nombres </p>
   *              <p> Value: Valora de la fila en la tabla </p>
   *         </p>
   * */
// TODO Alomejor no es todo lo eficiente que debería
  private Pair<List<String>, List<List<String>>> filterRowsValue(String tag, String tag_value) throws Exception {
    int column = this.Tags.indexOf(tag)-1;
    if (column < 0) throw new Exception("No exist la tag: " + tag);
    List<List<String>> row = this.Tabla.stream().filter(strings ->  strings.get(column).equals(tag_value)).collect(Collectors.toList());
    List<String> index = row.stream().map(strings -> this.Name.get(Tabla.indexOf(strings)+1)).collect(Collectors.toList());
    return new Pair(index, row);
  }


  private List<String> split(String dataInput) {
    dataInput = dataInput.replaceAll(":", "").replaceAll(";;+", ";");
    String[] parts = dataInput.split(";");
    List<String> listPart = new ArrayList<>(Arrays.asList(parts));
    return listPart;
  }


//  ============================ GETS & SETS ============================

  public List<List<String>> getTabla() {
    return this.Tabla.stream().map(ArrayList::new).collect(Collectors.toList());
  }

  public List<String> getTags() {
    return new ArrayList<String>(this.Tags);
  }

  public List<String> getName() {
    return new ArrayList<String>(this.Name);
  }

  public Map<String, List<String>> getValuesOfTags() {
    return new HashMap<String, List<String>>(this.ValuesOfTags);
  }

  public List<String> getValuesOfTags(String tag) {
    return new ArrayList<String>(this.ValuesOfTags.get(tag));
  }

  public int getPopulation(){
    return this.Tabla.size();
  }


//  =====================================================================

  @Override
  public String toString() {
    return "Tablas{" +
            "tabla=" + Tabla +
            ", etiquetas=" + Tags +
            ", nombre=" + Name +
            ", ValuesOfTags=" + ValuesOfTags +
            '}';
  }
}
