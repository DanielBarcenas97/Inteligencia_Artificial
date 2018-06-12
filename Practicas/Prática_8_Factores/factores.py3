# -*- coding: utf-8 -*-
__author__ = "Ángel Iván Gladín García"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "angelgladin@ciencias.unam.mx"
__status__ = "Terminado"

import itertools

def tabla_de_valores(l_variables):
    aux = [x.valores_posibles for x in l_variables]
    return list(map(list, itertools.product(*aux)))


class Variable:
    
    def __init__(self, nombre, valores_posibles):
        self.nombre = nombre
        self.valores_posibles = [str(x) for x in valores_posibles]

    def __str__(self):
        return self.nombre + " : " + str(self.valores_posibles)


class Factor:

    def __init__(self, alcance, valores, tabla_valores):
        self.alcance = alcance
        self.valores = valores
        self.tabla_valores = tabla_valores
        self.nombre_vars = list(map(lambda x: x.nombre, self.alcance))

    def __str__(self):
        s = ''
        s += ((8 +(8*(len(self.nombre_vars)+1))) * '-') + '\n'
        for x in self.nombre_vars:
            s += '| ' + x + '\t'
        s += '|' + '  P(' + ','.join(self.nombre_vars) + ')\n'
        s += ((8 +(8*(len(self.nombre_vars)+1))) * '-') + '\n'
        for i in range(len(self.tabla_valores)):
            s += '| ' + '\t| '.join(self.tabla_valores[i]) + '\t|  ' + str(self.valores[i]) + '\n'
        s += ((8 +(8*(len(self.nombre_vars)+1))) * '-') + '\n'
        return s
    
    def __union_vars_factores(self, f2):
        l = list(self.alcance)
        for x in f2.alcance:
            if x not in l:
                l.append(x)
        return l

    def __subconjunto_de_vars_y_estado(self, a, b):
        s1 = set()
        s2 = set()
        for x, y in a:
            s1.add(x+y)
        for x, y in b:
            s2.add(x+y)
        return s1.issubset(s2)        

    def multiplica(self, f2):
        nuevas_variables = self.__union_vars_factores(f2)
        nueva_nombre_vars = list(map(lambda x: x.nombre, nuevas_variables))
        nueva_tabla_valores = tabla_de_valores(nuevas_variables)
        nuevos_valores = [1 for _ in range(len(nueva_tabla_valores))]

        # Emparejar éste factor con la nueva tabla de valores.
        for valor_f1, estado_vars_f1 in zip(self.valores, self.tabla_valores):
            a = list(zip(self.nombre_vars, estado_vars_f1))
            # Asignar valores nuevos al la nueva tabla de valores.
            for i, estado_vars_fr in enumerate(nueva_tabla_valores):
                b = list(zip(nueva_nombre_vars, estado_vars_fr))
                if self.__subconjunto_de_vars_y_estado(a, b):
                    nuevos_valores[i] = valor_f1

        for valor_f2, estado_vars_f2 in zip(f2.valores, f2.tabla_valores):
            a = list(zip(f2.nombre_vars, estado_vars_f2))
            # Asignar valores nuevos al la nueva tabla de valores.
            for i, estado_vars_fr in enumerate(nueva_tabla_valores):
                b = list(zip(nueva_nombre_vars, estado_vars_fr))
                if self.__subconjunto_de_vars_y_estado(a, b):
                    nuevos_valores[i] *= valor_f2

        return Factor(nuevas_variables, nuevos_valores, nueva_tabla_valores)

    def reduccion(self, variable, valor_r):
        nuevas_variables = list(filter(lambda x: x.nombre != variable, self.alcance))
        nueva_tabla_valores = tabla_de_valores(nuevas_variables)
        nuevos_valores = []

        pos_variable = self.nombre_vars.index(variable)

        for valor, estado_vars in zip(self.valores, self.tabla_valores):
            # Checar la posición de la variable respecto al estado de las variables
            if estado_vars[pos_variable] == valor_r:
                nuevos_valores.append(valor)

        return Factor(nuevas_variables, nuevos_valores, nueva_tabla_valores)

    def nomalizacion(self, variable, valor_r):
        sum_vals_reduccion = sum(self.reduccion(variable, valor_r).valores)
        
        nueva_tabla_valores = []
        nuevos_valores = []

        pos_variable = self.nombre_vars.index(variable)

        for valor, estado_vars in zip(self.valores, self.tabla_valores):
            # Checar la posición de la variable respecto al estado de las variables
            if estado_vars[pos_variable] == valor_r:
                nueva_tabla_valores.append(estado_vars)
                nuevos_valores.append(valor/sum_vals_reduccion)

        return Factor(list(self.alcance), nuevos_valores, nueva_tabla_valores)

    def marginalizacion(self, variable):
        valores_asociados_var = []
        nuevos_valores = []

        pos_variable = self.nombre_vars.index(variable)
        # Guardo los posibles valores de la variable dada.
        for estado_vars in self.tabla_valores:
            if estado_vars[pos_variable] not in valores_asociados_var:
                valores_asociados_var.append(estado_vars[pos_variable])

        for val in valores_asociados_var:
            nuevos_valores.append(sum(self.reduccion(variable, val).valores))

        f = self.alcance[pos_variable]
        return Factor([f], nuevos_valores, tabla_de_valores([f]))

if __name__ == '__main__':
    print('########## Ejemplo 1: (Multiplicación) ##########')
    a = Variable('A', ['0', '1'])
    b = Variable('B', ['0', '1'])
    f_a = Factor([a], [.3, .7], tabla_de_valores([a]))

    print('Factor de A', '\n', f_a)
    f_b = Factor([b], [.6, .4], tabla_de_valores([b]))
    print('Factor de B', '\n', f_b)

    f_ab = f_a.multiplica(f_b)
    print('Factor resultante de multiplicar el factor A con B', '\n', f_ab)

    #################################################
    print('########## Ejemplo 2: (Multiplicación) ##########')
    a = Variable('A', ['0', '1'])
    b = Variable('B', ['0', '1'])
    c = Variable('C', ['0', '1'])

    f_ab = Factor([a, b], [.3*.6, .3*.4, .7*.6, .7*.4], tabla_de_valores([a, b]))
    print('Factor de AB', '\n', f_ab)

    f_ac = Factor([a, c], [.27*.54, .1*.4, .66*.9, .32*.15], tabla_de_valores([a, c]))
    print('Factor resultante de multiplicar el factor AB con AC', '\n', f_ab.multiplica(f_ac))
    
    #################################################
    print('########## Ejemplo 3: (Reducción) ##########')
    a = Variable('A', ['0', '1'])
    b = Variable('B', ['0', '1'])

    f_ab = Factor([a, b], [.18, .12, .42, .28], tabla_de_valores([a, b]))
    print('Factor de AB', '\n', f_ab)
    print('Factor resultante de hacer reducción el factor AB con (A=0)', '\n', f_ab.reduccion('A', '0'))
    
    #################################################
    print('########## Ejemplo 4: (Normalización) ##########')
    a = Variable('A', ['0', '1'])
    b = Variable('B', ['0', '1'])

    f_ab = Factor([a, b], [.18, .12, .42, .28], tabla_de_valores([a, b]))
    print('Factor de AB', '\n', f_ab)
    print('Factor resultante de hacer normalización del factor AB con (A=0)', '\n', f_ab.nomalizacion('A', '0'))

    #################################################
    print('########## Ejemplo 5: (Marginalización) ##########')
    a = Variable('A', ['0', '1'])
    b = Variable('B', ['0', '1'])

    f_ab = Factor([a, b], [.18, .12, .42, .28], tabla_de_valores([a, b]))
    print('Factor de AB', '\n', f_ab)
    print('Factor resultante de hacer marginalización del factor AB con A', '\n', f_ab.marginalizacion('A'))
