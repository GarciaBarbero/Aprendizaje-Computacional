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

        return value





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


    def

    def drawDecisionTree(self, deep=0):
        str_ = ""
        if not self.IsFinal:
            str_ += self.Tag
            aux_str = []
            for key in list(self.hijos.keys()):
                str_+="\n "+ ("\t"*deep) +"-> " + key + ":" +self.hijos.get(key).print(deep+1)
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
    # f = open("/home/chona/Documentos/Uma/Robotica/Practicas/ID3Tree/test.txt", "r")
    # data_aux = f.read().split("\n")
    # name = data_aux.pop(0).split(SEPARADOR)
    # data = []
    # for row in data_aux:
    #     data.append(row.split(SEPARADOR))
    #
    # tree = Tablas(name, data)
    # print(tree.best())

    tree = ID3()
    tree.learnDT("/home/chona/Documentos/Uma/Robotica/Practicas/ID3Tree/test.txt")
    # tree.learnDT("/home/chona/Documentos/Uma/Robotica/Practicas/ID3Tree/test2_dual.txt")
    print(tree.drawDecisionTree())
    # print(tree.evaluar(value=(["PArt","ASan","ICol","AAnt","Otros"] , ["alta","alto","alto","no","no"])))
    # print(tree.evaluar(value=(["PA","AS","IC","AA","OA"] , ["a","a","a","n","n"])))

    # print(tree.updata())
    # print(tree.erencia)