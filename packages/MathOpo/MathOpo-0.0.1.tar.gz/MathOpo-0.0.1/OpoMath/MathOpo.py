import re


class Number_System():

    def __init__(self,numbers):
        self.numbers=numbers
    #MUESTRA EL TIPO DE NÚMERO QUE ES.
    def type_of_number(self):
            '''
            Esta fucnion devuelve un diccionario string donde muestra el tipo de número.
            N:Número Natural
            Z:Número Entero
            Q:Número Racional
            I:Número Irracional
            :return: dict
            '''
            dicc_number = dict()
            numbers = re.split(",",self.numbers)
            for num in numbers:
                # compruebo si es un número positio o negativo.
                if re.match(r"^\d+$", str(num)):
                    dicc_number[str(num)] ="N"
                elif re.match("r^-?\d+$",str(num)):
                    dicc_number[str(num)] = "Z"
                # comprueba si los número son Entros
                elif re.search(r"^-?\d+\/\d+$", str(num)) or re.search(r"^-?\d+\.(\d)\1+\d$",str(num)):
                    dicc_number[str(num)] = "Q"
                #COmprobamos si número es irracional con esta expreción regular
                elif not re.search(r"^-?\d+\.(\d)\1+\d$",str(num)):
                    dicc_number[str(num)] = "I"
                    #Falta solucionar lo de nuemro racionales y irracionales.
                else:
                    return f"The value is not digit."
            return dicc_number


    #MUESTRA LOS NÚMERO PARES
    def is_pare(self):
        '''
        Esta fución comprueba si el número es par o no
        :return: boolean or boolean list()
        '''
        #lista de boolean
        bool_list = list()
        #Si contiene coma y que no lleve espacio entonce entra aquí y separa los números
        if "," in self.numbers and not " " in self.numbers:
            numbers = re.split(",",self.numbers)
            #comprueba si el número es par o imapar
            for num in numbers:
                operation = int(num) % 2
                if operation == 0:
                    bool_list.append(True)
                else:
                    bool_list.append(False)
            return bool_list

        elif " " in self.numbers:
            print("I can do the operation, because it has got space.")
        #Si el parametro contiene solo un número entonce entra en esta condición
        else:
            operation = int(self.numbers) % 2
            boolean = False
            if operation == 0:
                boolean = True
            return boolean
    #COMPRUEBA LOS NÚMERO QUE SÓN DIVISIBLES
    def divisible_with(self):
        '''
        Muestra los número que són divisible, depende del parametro que añadas nos puede devolver una list() o un número dict()
        :param divider:
        :return: list() or dict()
        '''

        dict_pare = dict()
        #COMPRUEBA SI CONTIENE COMA Y QUE NO LLEVA ESPCIO
        if "," in self.numbers and not " " in self.numbers:
            numbers = re.split(",",self.numbers)
            #RECORRE LOS DOS NÚMERO QUE HEMOS INDICADO
            for key in numbers:
                #DECLARA DE NUEVO LA LISTA
                list_pare = list()
                #DIVIDE 1 HASTA EL NÚMERO QUE HAYAMOS INDICADO
                for i in range(1, int(key)+1):
                    print(i)
                    # si el residuo es 0 entonce entra en la condición
                    if int(key) % i == 0:
                        #ALMACENA EN UNA ARRAY
                        list_pare.append(i)

                #ALMACENA EN UN DICCIONARIO
                dict_pare[key]=list_pare

            return dict_pare
        else:
            list_pare = list()

            #RECORRE EL BUCLE DESDE 1 HASTA EL CANTIDAD DE NÚMERO QUE HAYAS INDICADO.
            for i in range(1, int(self.numbers)):
                #si el residuo es 0 entonce entra en la condición
                if int(self.numbers) % i == 0:
                    #alamacena en una array
                    list_pare.append(i)
            #oredena la array
            list_pare.sort()
            return list_pare
    #MUESTRA UN BOOLEAN CUANDO UN NÚMERO ES DIVISIBLE CON EL OTRO
    def is_divisible(self, divider_number):
        '''
         Comprueba si el número es divisible con lo que haya indicado el usuario.
        :param divider_number:
        :return: Boolena
        '''
        result = 0
        boolean = True
        #OPERACIÓN
        result = int(self.numbers) % int(divider_number)
        quotient = int(self.numbers) // int(divider_number)
        #SI EL COCIENTE ES DIFERRENTE QUE 0 Y EL RESIDUO DIFERENTE QUE 0 ENTONCE EL BOOLEAN SERA FALSE DE LO CONTRARIO SERA TRUE
        if result != 0 or quotient < 0:
            boolean = False

        return boolean
    def list_of_not_divisible(self):

        list_no_divisor = list()
        operation_quotinet = 0
        operation_residue = 0
        dict_divisor = dict()
        for num in range(1, int(self.numbers)+1):
            operation_quotinet = int(self.numbers) // num

            operation_residue = int(self.numbers) % num
            #comprueba si el conciente es menor que el numbero indicado
            if operation_quotinet > int(self.numbers):
                break

            elif operation_residue != 0:
                list_no_divisor.append(num)

        list_no_divisor.sort()
        dict_divisor[self.numbers] = list_no_divisor
        return dict_divisor




number = Number_System("20")
print(number.divisible_with())
print(number.list_of_not_divisible())


