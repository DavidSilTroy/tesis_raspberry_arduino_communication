import matplotlib.pyplot as plt
import numpy as np


from tesis_sqlite import DB_sensors_sql

db_sql = DB_sensors_sql()

all_from_test = db_sql.get_data_from_column("sensors_tests","*")

tests_names=[]
tests_numbers=0

print("Escriba el número del test que desea graficar: ")

for test in all_from_test:
    tests_names.append(test[1])
    print(f'[{tests_numbers}] = {test[1]}')
    tests_numbers+=1

n_selected= int(input("Número: "))
print("Escriba el dominio en X")


doc_name=tests_names[n_selected]

print(f'El nombre seleccionado es: {doc_name}')

data_from_sql = db_sql.get_data_from_column(doc_name,"*")
yi=[]
xi=[]
yv=[]
yb=[]
ym=[]

max_jump=0
pos_max_jump=0
last_val=0


max_s_val=0
min_s_val=3000
yv_s=994 #valor que debe dar el sensor a determinado peso (10kg, 20kg, 40kg)
# es a 994 para sensores FSR serie 400 a 10kg y 464 para df9-40 a 20kg
yv_r_s=660 #valor que debe dar el sensor a con peso distribuido
# FSR400 => 393 , 660, 769
# FSR402 => 786 , 917, 954
# DF9-40 => 73 , 111.
the_label= 'valor del sensor a 0,036kg'

print(f'Se encontraron {len(data_from_sql)} datos')
from_part=int(input("Desde X en: "))
to_part=int(input("Hasta X en: "))
a=0
total_data=0
for data in data_from_sql:
    if from_part <= a:
        xi.append(a)
        yi.append(data[1])
        yv.append(yv_s)
        yb.append(yv_r_s)
        total_data=total_data+data[1]
        if a>0:
            current_jump=abs(last_val-data[1])
            if current_jump>max_jump:
                max_jump=current_jump
                pos_max_jump=a
        if max_s_val<data[1]:
            max_s_val=data[1]
        if min_s_val>data[1]:
            min_s_val=data[1]
        if to_part<=a:
            break
    a+=1
    last_val = data[1]

med_val= total_data/a
print("")
print(f'El valor mínimo en la gráfica es de {min_s_val}')
print(f'El valor máximo en la gráfica es de {max_s_val}')
print(f'El valor medio en la gráfica es de {med_val}')
print(f'El salto más grande es de {max_jump} en la pisición {pos_max_jump}')

volt_min = 5*min_s_val/1023
volt_max = 5*max_s_val/1023

print(f'El voltaje mínimo en la gráfica es de {volt_min}')
print(f'El voltaje máximo en la gráfica es de {volt_max}')

for i in xi:
    ym.append(med_val)


x = np.array(xi)
y = np.array(yi)
y1 = np.array(yv)
y2 = np.array(yb)
y3 = np.array(ym)


A = np.vstack([x, np.ones(len(x))]).T



m, c = np.linalg.lstsq(A, y, rcond=None)[0]

print(f'La función de la recta es y= {m}*x + {c}')

_ = plt.ylabel(f'Valor de sensor')
_ = plt.xlabel("Número de repeticiones")
#_ = plt.plot(x, y, label='líneas de continuidad', markersize=1)
_ = plt.plot(x, y, 'o', label='Valor de sensor', markersize=1)
#_ = plt.plot(x, y1, label='valor del sensor a 10kg', markersize=3)
_ = plt.plot(x, y3, label='Valor Promedio', markersize=8)
#_ = plt.plot(x, y2, label=the_label, markersize=4)
_ = plt.plot(x, m*x + c, 'r', label=f'Recta que mejor se ajusta', markersize=9)
_ = plt.legend()
plt.title(f'{doc_name}')
plt.show()