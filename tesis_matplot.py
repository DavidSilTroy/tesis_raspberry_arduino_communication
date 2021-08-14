import time
import matplotlib.pyplot as plt
import numpy as np
from tesis_sqlite import DB_sensors_sql

"""Program to plot the data from my thesis database
The program is mainly in Spanish"""

#Global variables
db_sql = DB_sensors_sql()
all_from_test = db_sql.get_data_from_column("sensors_tests","*")
tests_names=[]
tests_selected = 0
y_all=[]
x_all=[]
tests_selected_names = []

#function to check if the string can be changed to a int
def checkNumber(string_number):
    try:
        number= int(string_number)
        return True
    except ValueError:
        return False

#taking all the names from the tests in the database
for test in all_from_test:
        tests_names.append(test[1])

#just to left space in the terminal
print("")
print("")

#Taking the main data to show the values of the tests
while True:
    print("Escriba el número del test que desea graficar o sólo de enter para continuar: ")
    time.sleep(1)
    tests_numbers=0
    for test in tests_names:
        print(f'[{tests_numbers}] = {test}')
        tests_numbers+=1
        time.sleep(0.01)
    ask_number=input("Número: ")
    if not checkNumber(ask_number):
        if tests_selected>1:
            print("No hay número, continuemos")
        else:
            print("No se seleccionó ningún test")
        break
    n_selected= int(ask_number)
    if n_selected>=tests_numbers:
        print("Número mayor a la cantidad de tests")
        time.sleep(1)
        print("Intenta de nuevo..")
        time.sleep(1)
    elif n_selected < 0:
        print("¿Qué pretendes?..")
        time.sleep(2)
        print("Vamos en serio esta vez..")
        time.sleep(2)
    else:
        doc_name=tests_names[n_selected]
        time.sleep(0.1)
        print(f'Se ha seleccionado: {doc_name}')
        tests_selected_names.append(doc_name)
        time.sleep(0.2)
        print("Escriba el dominio en X")
        time.sleep(0.2)
        #taking the data for the plot
        data_from_sql = db_sql.get_data_from_column(doc_name,"*")
        print(f'Se encontraron {len(data_from_sql)} datos')
        time.sleep(0.2)

        #seting a default start and end of the plot
        from_part=0
        to_part = len(data_from_sql)
        #taking the start of the plot
        while True:
            ask_from_part = input("Desde X en: ")
            if checkNumber(ask_from_part):
                from_part=int(ask_from_part)
                if from_part<0:
                    print("Ese número está por debajo de 0")
                else:
                    break
            else:
                print(f'Ingresa un número entre 0 a {len(data_from_sql)}')
        #taking the end of the plot
        while True:
            ask_to_part =input("Hasta X en: ")      
            if checkNumber(ask_to_part):
                to_part=int(ask_to_part)
                if to_part<1:
                    print("Ese número está por debajo de 0")
                elif to_part>len(data_from_sql):
                    print(f'Sólo se mostrarán los datos hasta el punto {len(data_from_sql)}')
                    break
                else:
                    break
            else:
                print(f'Ingresa un número entre 1 a {len(data_from_sql)}')
        print("")
        print("Si desea agregar un nuevo test..")
        tests_selected+=1
        a=0
        x_i=[]
        y_i=[]
        for data in data_from_sql:
            if from_part <= a:
                x_i.append(a-from_part)
                y_i.append(data[1])
                if to_part<=a:
                    break
            a+=1
        x_all.append(x_i)
        y_all.append(y_i)


print("")
print("Si desea agregar un título, escribalo o sino apaste Enter")
the_title = input("Título: ")
if tests_selected>0:
    print("Graficando..")
    a=0
    _ = plt.ylabel(f'Valor de sensor')
    _ = plt.xlabel("Número de repeticiones")
    for test_name in tests_selected_names:
        x = np.array(x_all[a]) 
        y = np.array(y_all[a])
        _ = plt.plot(x, y, 'o', label=f'Valor de sensor {test_name}', markersize=2)
        a+=1
    _ = plt.legend()
    if len(the_title)>0:
        plt.title(the_title)
    plt.show()
    print("Cerrando el programa")
else:
    print("Cerrando el programa")
