import copy
import math


class Tablas:
    Tags: [str]
    Value_Class_tag: [list]
    Table: [[str]]

    def __init__(self, tags, tabla, values_clss_tag = None):
        self.Tags = tags
        self.Table = tabla
        self.Value_Class_tag = (list(set(map(lambda x: x[-1], tabla)))) if values_clss_tag is None else values_clss_tag



    def count_values(self):
        valuesClassification = self.Value_Class_tag
        numValueOfTagClas = [0]*len(valuesClassification)
        numValueByTags = {}

        for row in self.Table:
            row = row.copy()
            valOfTagClas = row.pop(-1)
            indexClassVal = valuesClassification.index(valOfTagClas)
            for ind, val in enumerate(row):
                tag = self.Tags[ind]
                # Extraigo el historico
                values_tag = numValueByTags.setdefault(tag, {val:[0]*len(valuesClassification)})
                count_class = values_tag.setdefault(val, [0]*len(valuesClassification))
                count_class[indexClassVal] += 1
                # Actulizo los datos
                values_tag.update({val: count_class})
                numValueByTags.update({tag: values_tag})

            numValueOfTagClas[indexClassVal] += 1

        return (numValueOfTagClas, numValueByTags)

    def best(self):
        """
        Retorn la tag que deve ser evaluada en el sigiente nodo
        Si solo tenemos una Tag o un Valora de clasificar se trermina de expandir el nodo
        :return: esFinal, Tag
        """
        # Si solo tenemos una Tag o un Valora de clasificar se trermina de expandir el nodo
        if len(self.Value_Class_tag) < 2:
            return True, None
        if len(self.Tags)-1 < 2:
            return True, self.Tags[0]

        # Cuento el numero de elemos clasificados en la tabla
        self._num_class_value, self._num_values_tag = self.count_values()

        entropia = {}
        ganacia = {}
        entropia_base = self._entropy(self._num_class_value)
        maxima_ganancia = ("", 0)
        # Calcula las entropias y las ganancias.
        for key in list(self._num_values_tag):
            aux_entropy = [entropia_base]
            for value in list(self._num_values_tag.get(key).values()):
                aux_entropy.insert(0, self._entropy(value))
            entropia.update({key:aux_entropy})
            aux_ganacia = self._ganacia(aux_entropy)
            ganacia.update({key: aux_ganacia})
            if maxima_ganancia[1] < aux_ganacia:
                maxima_ganancia = (key, aux_ganacia)

        return False, maxima_ganancia[0]

    def evaluar(self, tag=None, value=None):
        # Si la tabla no puede espandirse mas, retorna la clasificacion del balor y la etiqueta.
        if len(self.Value_Class_tag) < 2:
            return self.Value_Class_tag[0]
        index = self.Tags.index(tag)
        count = len(list(filter(lambda x: x[index] == value, self.Table)))
        return (count/len(self.Table))*100

    def removeTag(self, tag):
        index = self.Tags.index(tag)
        listValues = list(self._num_values_tag.get(tag).keys())
        hijos = {}

        for valor in listValues:
            aux_name = copy.deepcopy(self.Tags)
            aux_name.pop(index)
            aux_table = copy.deepcopy(self.Table)
            aux_table = list(filter(lambda x: x[index] == valor, aux_table))
            aux_table = list(map(lambda x: x[:index] + x[index+1 :], aux_table))
            newTable = Tablas(aux_name, aux_table)
            hijos.update({valor:newTable})

        return hijos

    def get_values_of_tag(self, tag):
        return list(self._num_values_tag.get(tag).keys())

    def _ganacia(self, element):
        total,ganancia = element.pop(-1)

        for item in element:
            ganancia += -((item[0]/total)*item[1])

        return ganancia

    def _entropy(self, elements):
        total = sum(elements)
        entropy = 0
        for item in elements:
            if item != 0:
                parcial = (item / total)
                entropy += -(parcial * math.log(parcial, 2))

        return total,entropy