const HV = 999999
let T
let TF
let TPLL
let NT
let NS
let STAA
let STAP
let SPS
let PEC

let TPSA = []
let TPSP = []
let ITOA = []
let ITOP = []
let STOP = []
let STOA = []
let PTOA = []
let PTOP = []

function inicializar_array(array, tam_array, valor){
    for(let i = 0; i < tam_array; i++){
        array[i] = valor; // Fix: Changed tam_array to i
    }
}

function inicializacion(N, M){
    inicializar_array(TPSA, N, HV)
    inicializar_array(TPSP, M, HV)
    inicializar_array(ITOA, N, 0)
    inicializar_array(ITOP, M, 0)
    inicializar_array(STOA, N, 0)
    inicializar_array(STOP, M, 0)
    inicializar_array(PTOA, N, 0)
    inicializar_array(PTOP, M, 0)
    
    T = 0
    TF = 100
    TPLL = 0
    NS = 0
    NT = 0
    STAA = 0
    STAP = 0
    SPS = 0
    PEC = 0
}

function algoritmo(M, N){

    inicializacion(N, M)

    while(T < TF){
        metodologia(N, M)
    }

    while(NS > 0){
        metodologia(N, M)
        TPLL = HV
    }

    PEC = (SPS - STAA - STAP) / NT

    for(let i = 0; i < M; i++){
        PTOA[i] = STOA[i] * 100 / T
    }

    for(let i = 0; i < N; i++){
        PTOP[i] = STOP[i] * 100 / T
    }

    //imprimir
}

function metodologia(N, M){
    let i = menor(TPSA)
    let j = menor(TPSP)

    if(TPSP[j] <= TPSA[i]){
        if(TPLL <= TPSP[j]){
            llegada(N, M)
        }else{
            salida_profesor(j, N, M)
        }
    }else{
        if(TPLL <= TPSA[i]){
            llegada(N, M)
        }else{
            salida_ayudante(i, N, M)
        }
    }
}

function llegada(N, M){
    SPS += (TPLL - T) * NS
    T = TPLL
    let ia = generar_ia()
    TPLL = T + ia
    //arrepentimiento?
    NS++
    NT++
    if(NS <= M){
        let i = TPSP.indexOf(HV) //profesor libre
        let tap = generar_tap()
        TPSP[i] = T + tap
        STAP += tap
        STOP[i] += T - ITOP[i]
    }else if(NS <= M + N){
        let i = TPSA.indexOf(HV) //ayudante libre
        let taa = generar_taa()
        TPSA[i] = T + taa
        STAA += taa
        STOA[i] += T - ITOA[i]
    }
}

function salida_profesor(i, N, M){
    SPS += (TPSP[i] - T) * NS
    T = TPSP[i]
    NS--
    if(NS >= M){
        let tap = generar_tap()
        TPSP[i] = T + tap
        STAP += tap
    }else{
        ITOP[i] = T
        TPSP[i] = HV
    }
}

function salida_ayudante(i, N, M){
    SPS += (TPSA[i] - T) * NS
    T = TPSA[i]
    NS--
    if(NS >= M + N){
        let taa = generar_taa()
        TPSA[i] = T + taa
        STAA += taa
    }else{
        ITOA[i] = T
        TPSA[i] = HV
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

function generar_tap(){
    return Math.random();
}

function generar_taa(){
    return Math.random();
}

function generar_ia(){
    return Math.random();
}

algoritmo(2, 4)
console.log(PEC, PTOA, PTOP)
