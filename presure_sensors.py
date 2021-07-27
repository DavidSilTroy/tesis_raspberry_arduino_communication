import math

fsr_400_radious =2.54   #[mm]
fsr_402_radious =7.34   #[mm]
df9_40_radious  =3.75   #[mm]

piston_width    =22     #[mm] (49, 22, 12)
piston_height   =60     #[mm] (99, 67, 67)
kg_for_press    =34     #[kg]

area_for_press  =   (piston_height/1000)*(piston_width/1000)
force_for_press =   kg_for_press*9.81 # N = (kg*m/s2)
total_pressure  =   force_for_press/area_for_press

def AreaSensor(sensor_radious):
    """the area should be the radious in mm"""
    s_r=sensor_radious/1000
    return math.pi*s_r*s_r
    
# def PresureInSensor(self,sensor_area):
#     return sensor_area*total_pressure

if __name__=='__main__':
    fsr_400_area =AreaSensor(fsr_400_radious)
    fsr_402_area =AreaSensor(fsr_402_radious)
    df9_40_area =AreaSensor(df9_40_radious)
    print("")
    print(f'area FSR-402: {fsr_402_area}')
    print(f'area FSR-400: {fsr_400_area}')
    print(f'area DF9-40: {df9_40_area}')
    print("")
    print(f'Force to press: {force_for_press}')
    print(f'total area is: {area_for_press}')
    print(f'total presure is: {total_pressure}')
    print("")
    print(f'FSR-402 force is: {AreaSensor(fsr_402_radious)*total_pressure} [N]')
    print(f'FSR-400 force is: {AreaSensor(fsr_400_radious)*total_pressure} [N]')
    print(f'DF9-40 force is: {AreaSensor(df9_40_radious)*total_pressure} [N]')