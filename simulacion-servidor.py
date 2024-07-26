import random
import math
import time
import numpy
from datetime import datetime, timedelta

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

### C.I. ###

# VARIABLES DE CONTROL
N = 0
H = 0
IPC = 0
VC = 0
M = 0

INS_PETICION = 50000 #cantidad instrucciones promedio por peticion
MEM_PETICION = 5000 #cantidad memoria promedio por peticion (KB)

# VARIABLES DE RESULTADO
CVCS = 0 # cantidad de veces que la capacidad del servidor fue superada
PRF = 0 # promedio de ram faltante
PCF = 0 # promedio de cpu faltante
PPR = 0 # porcentaje de peticiones rechazadas

# VARIABLES DE ESTADO
P = 0

# VARIABLES AUXILIARES
T=0
#TF = 24 * 365 * 10 # 10 años de simulación 24 horas al dia
TF = 24 * 365 * 10
FECHA_INICIAL = datetime(2024, 12, 22)
SPRF = 0 #sumatoria
SPCF = 0 #sumatoria
SPPR = 0 #sumatoria de peticiones rechazadas
CPT = 0 #cantidad de peticiones totales
CVDDoS = 0 #cantidad de veces que hubo ataque DDoS
DDOS_FLAG = False
MANTENIMIENTO_ACTIVO = 0
CAP_CPU = 0
CAP_RAM = 0

HV = 9999999999999

while True:
    try:
        ### VARIABLES DE CONTROL ###
        M = int(input("Cantidad de memoria RAM en GB (M): "))
        N = int(input("Cantidad de nucleos (N): "))
        H = int(input("Cantidad de hilos (H): "))
        VC = int(input("Velocidad clock en GHz (VC): "))
        IPC = int(input("Cantidad de instrucciones por ciclo (IPC): "))
        CAP_CPU = (N * H * IPC * (VC*1000000000) * 3600) / (INS_PETICION)
        CAP_RAM = (M*1000000 / MEM_PETICION)

        CAP_CPU = round(CAP_CPU, 2)
        CAP_RAM = round(CAP_RAM, 2)

        break
    except ValueError:
        print("\nError: Solo se permiten numeros enteros.\n")
        continue

# FDP POISSON CON LAMBDA = 2000
def obtener_PH(): #Peticiones por Hora
    LAMBDA = 2000
    FDP = numpy.random.poisson(LAMBDA)
    return round(FDP)

# 0.08% de probabilidad de recibir ataque DDoS por hora
def ocurrencia_ataque_DDoS():
    global DDOS_FLAG, CVDDoS
    probabilidad = numpy.random.rand()

    if (probabilidad < 0.008):
        DDOS_FLAG = True
        CVDDoS += 1
    else:
        DDOS_FLAG = False

def obtener_hora():
    global T
    return T % 24

def obtener_fecha():
    global T, FECHA_INICIAL
    cant_dias = T // 24
    cant_horas_restantes = obtener_hora()
    fecha_actual = FECHA_INICIAL + timedelta(days=cant_dias, hours=cant_horas_restantes)
    return fecha_actual
    
def es_comienzo_trimestre():
    mes = obtener_fecha().month
    dia = obtener_fecha().day
    
    return (mes == 1 and dia == 1) or (mes == 4 and dia == 1) or (mes == 7 and dia == 1) or (mes == 10 and dia == 1)
    
def es_comienzo_mes():
    dia = obtener_fecha().day
    hora = obtener_hora()
    return dia == 1 and hora == 1

def porcentaje_aumento_evento(mes_evento, dia_evento):
    fecha = obtener_fecha()
    evento = datetime(fecha.year, mes_evento, dia_evento)

    if fecha.day == dia_evento and fecha.month == mes_evento:
        return 1.15
    else:
        return 1
    
def porcentaje_aumento_evento_anticipado(mes_evento, dia_evento):
    fecha_actual = obtener_fecha()
    evento = datetime(fecha_actual.year, mes_evento, dia_evento)

    dias_restantes = (evento-fecha_actual).days
    
    if dias_restantes >= 0 and dias_restantes < 7:
        return 1 + 0.15 * (-dias_restantes + 5)
    else:
        return 1
    

def mantenimiento():
    global CAP_CPU, CAP_RAM, MANTENIMIENTO_ACTIVO
    CAP_CPU = CAP_CPU * 0.8
    CAP_RAM = CAP_RAM * 0.8
    MANTENIMIENTO_ACTIVO = 2

def resultados():
    global T, SPPR, SPCF, SPRF, CVDDoS, CPT

    if CVCS != 0:
        PRF = (SPRF * MEM_PETICION) / CVCS / 1000000  # Convierte KB a GB
        PRF = round(PRF)
        PCF = (SPCF * INS_PETICION) / (CVCS * 3600) / 1000000000  # Convierte a GHz
        PCF = round(PCF, 2)
        PPR = (SPPR * 100) / CPT
        PPR = round(PPR, 2)
    else:
        PRF = 0
        PCF = 0
        PPR = 0

    print(f"Cantidad de veces capacidad del servidor superada {CVCS}")
    print(f"Promedio de capacidad de RAM faltante: {PRF} Kbs")
    print(f"Promedio de capacidad de CPU faltante: {PCF} GHz")
    print(f"Porcentaje de peticiones rechazadas: {PPR}%")
    print(f"Cantidad de veces que se sufrio ataque DDoS: {CVDDoS}")


def realizar_simulacion():
    global T, P, CAP_CPU, CAP_RAM, CVCS, MANTENIMIENTO_ACTIVO, SPPR, SPCF,SPRF,CPT
    while True:
        fecha = obtener_fecha()
        
        ### AVANZO EN EL TIEMPO EN UN DELTA T ###

        print(f"{BLUE}Fecha: {fecha}{RESET}")
        
        T += 1

        ### GENERO, CALCULO O USO TODO LO QUE ENTRA ###
        ph = obtener_PH()
        
        #PH horas pico
        if obtener_hora() in [18, 19, 20, 21, 22]:
            ph *= 3
        
        #PH ante ocurrencia de ataque DDOS
        ocurrencia_ataque_DDoS()

        if (DDOS_FLAG):
            print(f"{YELLOW}DDOS{RESET}")
            ph *= 10
            
        #PH ante dia festivo
        
        a1 = porcentaje_aumento_evento_anticipado(11, 20)
        a2 = porcentaje_aumento_evento_anticipado(6, 1)
        a3 = porcentaje_aumento_evento_anticipado(10, 1)
        a4 = porcentaje_aumento_evento_anticipado(12, 24)
        
        a5 = porcentaje_aumento_evento(11, 29)
        a6 = porcentaje_aumento_evento(5, 13)
        a7 = porcentaje_aumento_evento(5, 14)
        a8 = porcentaje_aumento_evento(5, 15)
        a9 = porcentaje_aumento_evento(12, 2)

        ph = ph * a1 * a2 * a3 * a4 * a5 * a6 * a7 * a8 * a9
        
        #PH ante evento trimestral
        if es_comienzo_trimestre() == True:
            print(f"{BLUE}COMIENZO MES{RESET}")
            ph *= 15
        
        ### GENERO, CALCULO O USO TODO LO QUE SALE ###
        
        # Si quedan horas de mantenimiento, restar
        if MANTENIMIENTO_ACTIVO >= 1:
            MANTENIMIENTO_ACTIVO -= 1
            if MANTENIMIENTO_ACTIVO == 0: # si se terminaron las horas de mantenimiento, vuelve a la normalidad
                CAP_CPU = CAP_CPU / 0.8
                CAP_RAM = CAP_RAM / 0.8
            
        # Mantenimiento mensual
        if es_comienzo_mes() == True:
            mantenimiento()
        
        # Si hay ataque DDoS, no hay mantenimiento activo y se duplica la capacidad de cpu o ram => mantenimiento
        if DDOS_FLAG and MANTENIMIENTO_ACTIVO == 0 and (ph >= CAP_CPU*2 or ph >= CAP_RAM*2):
            mantenimiento()
        
        ph = round(ph, 0)

        CPT += ph

        ### MODIFICO VAR DE ESTADO CON TODO LO QUE SALE Y ENTRA ###

        print(f"PH: {ph}")
        print(f"CPU: {CAP_CPU}")
        print(f"RAM: {CAP_RAM}")

        P = min(CAP_CPU, CAP_RAM) - ph
        print(f"P: {P}")
        #hay rechazados

        if P<0:
            print(f"{RED}T: {T}{RESET}")
            CVCS += 1
            SPPR += abs(P) #sumatoria de peticiones rechazadas

            if ph>CAP_CPU:
                SPCF += ph - CAP_CPU

            if ph>CAP_RAM:
                SPRF += ph - CAP_RAM
        else:
            print(f"{GREEN}T: {T}{RESET}")
                
        P = 0

        if T < TF:
            ph = 0
            continue
        else:
            break

    resultados()


def main():
    print("\n\n### Comenzando simulacion ###\n\n")
    realizar_simulacion()
    print("\nFinalizando simulacion...")


if __name__ == "__main__":
    main()
