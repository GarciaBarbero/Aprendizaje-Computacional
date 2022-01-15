import math
import copy

from Tabla import Tablas

class ID3:
    Tabla: Tablas
    Index_Tag: int
    Tag: str
    hijos: {}
    IsFinal = False
    Separador = ','

    def __init__(self, tabla=None):
        self.Tabla = tabla
        self.Index_Tag = None
        self.Tag = None
        self.hijos = None

    def learnDT(self, dir, SEPARADOR = ','):
        self.Separador = SEPARADOR
        name, data, _ = self._separar(dir, SEPARADOR)
        self.Tabla = Tablas(name, data)
        self.next()



    def Pediction(self, value=None, dir=None):
        if not dir is None:
            name , data, num_row = self._separar(dir, self.Separador)
        elif not value is None:
            name, data = value
            num_row = 0
        else:
            raise ValueError("No hay datos para evaluar")

        if num_row > 1:
            aux_data = []
            for row in data:
                row.insert(len(row), self._eval(row, name))
                aux_data.insert(len(aux_data), row)
        else:
            data.insert(len(data), self._eval(data, name))
            aux_data = data
        return aux_data



    def _eval(self, table, name):
        value = None
        if self.IsFinal:
            if not self.Tag is None:
                value = table[name.index(self.Tag)]
                value = self.Tabla.evaluar(self.Tag, value)
            else:
                value = self.Tabla.evaluar()
        else:
            value = table[name.index(self.Tag)]
            value = self.hijos.get(value)._eval(table, name)

        if value is list:
            value = value[0][0]
        return value


    def acuracity(self, dir):
        nama, data, _ = self._separar(dir, self.Separador)
        nama.pop(-1)

        acuracit = [0,0]
        for row in data:
            value_clas = row.pop(-1)
            value_pedict = self._eval(row,nama)
            if value_pedict == value_clas:
                acuracit[1] +=1
            else:
                acuracit[0] += 1
        suma = sum(acuracit)
        acuracit[0] = ("Fallos",acuracit[0]/suma)
        acuracit[1] = ("Aciertos",acuracit[1] / suma)



        return acuracit

    def next(self):
        self.IsFinal, self.Tag = self.Tabla.best()
        if not self.IsFinal:
            self.Index_Tag = self.Tabla.Tags.index(self.Tag)
            self.hijos = self.Tabla.removeTag(self.Tag)

            for key in list(self.hijos.keys()):
                newID3 = ID3(self.hijos.get(key))
                self.hijos.update({key:newID3})
                newID3.next()


    def _separar(self, dir, Separador):
        f = open(dir, "r")
        data_aux = f.read().split("\n")
        name = data_aux.pop(0).split(Separador)
        data = []
        num_row = 0
        for row in data_aux:
            data.append(row.split(Separador))
            num_row +=1

        return name, data, num_row


    def drawDecisionTree(self, deep=0):
        str_ = ""
        if not self.IsFinal:
            str_ += self.Tag
            aux_str = []
            for key in list(self.hijos.keys()):
                str_+="\n "+ ("\t"*deep) + "├" +"─> " + key + ":" +self.hijos.get(key).drawDecisionTree(deep+1)
        else:
            if not self.Tag is None:
                str_ += self.Tag
                str_ += ":"

                values = self.Tabla.get_values_of_tag(self.Tag)
                for val in values:
                    str_+="{ " + val + ":" + self.Tabla.evaluar(self.Tag, val) + " }"
            else:
                str_ += "{ " + self.Tabla.evaluar() + " }"
        return str_

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tree = ID3()
    tree.learnDT("./test2_dual.txt")
    print(tree.drawDecisionTree())
    print(tree.acuracity("./prediccionesTest2.txt"))

