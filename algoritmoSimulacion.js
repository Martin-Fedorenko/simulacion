const HV = 999999
let T
let TF
let TPLL
let NTCE //personas totales CE
let NTC //personas totales C
let STAC //sumatoria TA C
let STAE //sumatoria TA CE
let SLLCE //sumatoria llegadas CE
let SLLC //sumatoria llegadas C
let SSE //sumatoria salida CE
let SSC //sumatoria salida C
let PEC //promedio espera C
let PECE //promedio espera CE

let TPSCE = [] //tiempo proxima salida
let TPSC = []
let ITOCE = [] //intervalo tiempo ocioso
let ITOC = []
let STOCE = [] //sumatoria tiempo ocioso
let STOC = []
let PTOCE = [] //porcentaje de tiempo ocioso
let PTOC = []

function inicializar_array(array, tam_array, valor){
    for(let i = 0; i < tam_array; i++){
        array[i] = valor;
    }
}

function inicializacion(N, M){
    inicializar_array(TPSCE, N, HV)
    inicializar_array(TPSC, M, HV)
    inicializar_array(ITOCE, N, 0)
    inicializar_array(ITOC, M, 0)
    inicializar_array(STOCE, N, 0)
    inicializar_array(STOC, M, 0)
    inicializar_array(PTOCE, N, 0)
    inicializar_array(PTOC, M, 0)
    
    let T = 0
    let TF = 0
    let TPLL = 0
    let NTCE = 0 //personas totales CE
    let NTC = 0 //personas totales C
    let STAC = 0 //sumatoria TA C
    let STAE = 0 //sumatoria TA CE
    let SLLCE = 0 //sumatoria llegadas CE
    let SLLC = 0 //sumatoria llegadas C
    let SSE = 0 //sumatoria salida CE
    let SSC = 0 //sumatoria salida C
}

function algoritmo(C, CE){

    inicializacion(C, CE)

    while(T < TF){
        metodologia(C, CE)
    }

    while(NSC > 0 && NSCE > 0){
        metodologia(C, CE)
        TPLL = HV
    }

    PEC = (SSC - SLLC - STAC) / NTC //promedio espera
    PECE = (SSE - SLLCE - STAE) / NTC //promedio espera

    for(let i = 0; i < CE; i++){
        ITOCE[i] = STOCE[i] * 100 / T
    }

    for(let i = 0; i < C; i++){
        ITOC[i] = STOC[i] * 100 / T
    }

    //FALTA ARREPENTIMIENTO

    //imprimir
}

function metodologia(N, M){
    let i = menor(TPSC)
    let j = menor(TPSCE)

    if(TPSC[j] <= TPSCE[i]){
        if(TPLL <= TPSC[j]){
            llegada(C, CE)
        }else{
            salida_C(j, C, CE)
        }
    }else{
        if(TPLL <= TPSCE[i]){
            llegada(C, CE)
        }else{
            salida_CE(i, C, CE)
        }
    }
}

function llegada(C, CE){
    SPS += (TPLL - T) * NS
    T = TPLL
    let ia = generar_ia()
    TPLL = T + ia
    //arrepentimiento?
    NS++
    NT++
    if(NS <= M){
        let i = TPSC.indexOf(HV) //profesor libre
        let tap = generar_tac()
        TPSC[i] = T + tap
        STAP += tap
        STOP[i] += T - ITOP[i]
    }else if(NS <= M + N){
        let i = TPSCE.indexOf(HV) //ayudante libre
        let taa = generar_tae()
        TPSCE[i] = T + taa
        STAA += taa
        STOA[i] += T - ITOA[i]
    }
}

function salida_C(i, C, CE){
    SPS += (TPSC[i] - T) * NS
    T = TPSC[i]
    NS--
    if(NS >= M){
        let tap = generar_tac()
        TPSC[i] = T + tap
        STAP += tap
    }else{
        ITOP[i] = T
        TPSC[i] = HV
    }
}

function salida_CE(i, N, M){
    SPS += (TPSCE[i] - T) * NS
    T = TPSCE[i]
    NS--
    if(NS >= M + N){
        let taa = generar_tae()
        TPSCE[i] = T + taa
        STAA += taa
    }else{
        ITOA[i] = T
        TPSCE[i] = HV
    }
}

function menor(array){
    let i = 0
    for(let j = 0; j < array.length; j++){
        if(array[j] < array[i]){
            i = j
        }
    }
    return i
}

function generar_tac(){
    return Math.random();
}

function generar_tae(){
    return Math.random();
}

function generar_ia(){
    return Math.random();
}

algoritmo(2, 4)
console.log()
