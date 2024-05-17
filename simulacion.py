import random
import math
import time

CE = 0
C = 0

while True:
    try:
        ### VARIABLES DE CONTROL ###
        C = int(input("Cantidad de cajeros (C): "))
        CE = int(input("Cantidad de cajeros eminent (CE): "))

        break
    except ValueError:
        print("\nError: Solo se permiten numeros enteros.\n")
        continue

HV = 6666666666666
iterationIndex = 0
EVENTO = "C.I."

i = -1
j = -1
x = -1

### C.I. ###
T=0 
TPLL=0
TF = 60 * 60 * 5 * 365 * 10 # 100 años de atencion de turnos de 5 horas (en segundos)
NSC=0 
NSCE=0
SSE=0
SSC=0
STAC=0
STACE=0
NTCE=0
NTC=0
SAC=0 
SACE=0
ITOC = [0] * C
ITOCE = [0] * CE
TPSC = [HV] * C
TPSCE = [HV] * CE
STOC = [0] * C
STOCE = [0] * CE
PTOC = [0] * C
PTOCE = [0] * CE
SLLCE = 0
SLLC = 0





def obtener_primer_puesto_vacio(arreglo):
    for i in range(0, len(arreglo)):
        if arreglo[i] == HV:
            return i
    return -1
    
def obtener_TAC():
    while True:
        R = random.uniform(0.00009, 0.99945)
        TAC = 127.29 + 30.172 * math.tan(math.pi * (R - 0.5))
        TAC = 61*(math.pow((1-R),(-1/1.1319)))
        return  TAC 

def obtener_TACE():
    while True:
        R = random.uniform(0, 1)
        TACE = 59.033 * math.pow((-math.log(1-R)),(1/0.93206))
        return  TACE 


def obtener_IA():
    R = random.uniform(0, 1)
    a = 0.93206
    b = 53.033
    IA = 111.61 * math.pow((- math.log(1 - R)), 1/0.68637) + 61
    return  IA 


def obtener_primer_puesto_vacio_cajero_emminent():
    return obtener_primer_puesto_vacio(TPSCE)


def obtener_primer_puesto_vacio_cajero():
    return obtener_primer_puesto_vacio(TPSC)


def obtener_puesto_menor_tps_de_arreglo(arreglo):
    minTPSLista = HV
    minTPSListaIndex = 0

    for i in range(0, len(arreglo)):
        if arreglo[i] < minTPSLista:
            minTPSLista = arreglo[i]
            minTPSListaIndex = i

    return minTPSListaIndex


def obtener_puesto_menor_tps_cajero_eminent():
    return obtener_puesto_menor_tps_de_arreglo(TPSCE)


def obtener_puesto_menor_tps_cajero():
    return obtener_puesto_menor_tps_de_arreglo(TPSC)


def llegada():

    global T, NSC, NSCE, TPLL, SLLCE, SSC, SSE, TF
    global STACE, STAC, STOC, STOCE
    global ITOCE, ITOC
    global EVENTO
    global PECC, PECCE
    global NTCE
    global NTC
    global NSCE
    global NSC
    global TPSCE
    global SLLC
    global TPSC
    global x
    global SACE, SAC

    T = TPLL
    IA = obtener_IA()
    TPLL = T + IA
    R = random.uniform(0, 1)

    if R <= 0.31:
        if NSCE > CE + 2:
            R = random.uniform(0, 1)
            if R < 0.1:
                SACE = SACE + 1
                return
        NSCE += 1
        SLLCE = SLLCE + T
        if NSCE <= CE:
            x = obtener_primer_puesto_vacio_cajero_emminent()
            TA = obtener_TACE()
            TPSCE[x] = T + TA
            STACE = STACE + TA
            STOCE[x] = STOCE[x] + (T - ITOCE[x]) 
    else:
        if NSC > C + 6:
            R = random.uniform(0, 1)
            if R < 0.3:
                SAC = SAC + 1
                return
        NSC += 1
        SLLC = SLLC + T
        if NSC <= C:
            x = obtener_primer_puesto_vacio_cajero()
            TA = obtener_TAC()
            TPSC[x] = T + TA
            STAC = STAC + TA
            STOC[x] = STOC[x] + (T -ITOC[x])


def resultados():
    global SSE
    global SLLCE
    global NTC, NTCE
    global PTOC
    global PTOCE
    global T
    global PECCE
    global STOCE
    global STACE
    global PECC
    global STOC
    global STAC
    global SSC

    for i in range(0, CE):
        PTOCE[i] = (STOCE[i] * 100) / T

    PECCE = (SSE - SLLCE - STACE) / NTCE

    for j in range(0, C):
        PTOC[j] = (STOC[j] * 100) / T

    PECC = (SSC - SLLC - STAC) / NTC

    PARRCE = SACE *100 / (NTCE + SACE)
    PARRC = SAC * 100 / (NTC + SAC)


    print(f"Promedio de espera en cola de cajero eminent: {PECCE}")
    print(f"Promedio de espera en cola de cajero: {PECC}")
    print(f"Porcentaje de arrepentimientos en cola de cajero: {PARRC}")
    print(f"Porcentaje de arrepentimientos en cola de cajero eminent: {PARRCE}")

    for i in range(0, CE):
        print(f"porcentaje de tiempo ocioso del cajero eminent {i} es: {PTOCE[i]}")

    for j in range(0, C):
        print(f"porcentaje de tiempo ocioso del cajero {j} es: {PTOC[j]}")


def realizar_simulacion():
    global i, j
    global T, NSC, NSCE, TPLL, SSC, SSE, TF
    global STACE, STAC, STOC, STOCE
    global EVENTO
    global PECC, PECCE
    global TPSCE
    global TPSC
    global ITOC, ITOCE
    global NTCE
    global NTC, STTA

    while True:
        i = obtener_puesto_menor_tps_cajero_eminent()
        j = obtener_puesto_menor_tps_cajero()

        if TPSCE[i] <= TPSC[j]:
            if TPSCE[i] < TPLL:
                # Salida cajero eminent
                EVENTO = "Salida Cajero Eminent"
                T = TPSCE[i]
                NSCE -= 1

                if NSCE >= CE:
                    # Generar TA
                    TA = obtener_TACE()
                    TPSCE[i] = T + TA
                    STACE = STACE + TA
                else:
                    ITOCE[i] = T
                    TPSCE[i] = HV

                SSE = SSE + T
                NTCE += 1
            else:
                llegada()
        else:
            if TPSC[j] < TPLL:
                # Salida cajero eminent
                EVENTO = "Salida Cajero"
                T = TPSC[j]
                NSC -= 1

                if NSC >= C:
                    TA = obtener_TAC()
                    TPSC[j] = T + TA
                    STAC = STAC + TA
                else:
                    ITOC[j] = T
                    TPSC[j] = HV
                SSC = SSC + T
                NTC += 1
            else:
                llegada()

        if T < TF:
            continue
        else:
            if NSCE > 0 or NSC > 0:
                TPLL = HV
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
