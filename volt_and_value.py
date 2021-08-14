
res_1 = 3.8

volt=5
res_2=10

volt_out= volt*res_2/(res_2+res_1)

val_s_read = volt_out*1023/5
print("")
print("")
print(f'voltaje: {volt_out}')
print(f'valor entrada: {val_s_read}')
print("")
print("")
