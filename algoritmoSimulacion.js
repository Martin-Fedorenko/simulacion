const HV = 999999
let T
let TF
let TPLL
let NSC
let NSCE
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
let SACE //sumatoria arrepentidos CE
let SAC //sumatoria arrepentidos C

let TPSCE = [] //tiempo proxima salida
let TPSC = [] //tiempo proxima salida
let ITOCE = [] //intervalo tiempo ocioso
let ITOC = [] //intervalo tiempo ocioso
let STOCE = [] //sumatoria tiempo ocioso
let STOC = [] //sumatoria tiempo ocioso
let PTOCE = [] //porcentaje de tiempo ocioso
let PTOC = [] //porcentaje de tiempo ocioso

function inicializar_array(array, tam_array, valor){
    for(let i = 0; i < tam_array; i++){
        array[i] = valor;
    }
}

function inicializacion(C, CE){
    inicializar_array(TPSCE, CE, HV)
    inicializar_array(TPSC, C, HV)
    inicializar_array(ITOCE, CE, 0)
    inicializar_array(ITOC, C, 0)
    inicializar_array(STOCE, CE, 0)
    inicializar_array(STOC, C, 0)
    inicializar_array(PTOCE, CE, 0)
    inicializar_array(PTOC, C, 0)
    
    T = 0
    TF = 20
    TPLL = 0
    NSC = 0
    NSCE = 0
    NTCE = 0 //personas totales CE
    NTC = 0 //personas totales C
    STAC = 0 //sumatoria TA C
    STAE = 0 //sumatoria TA CE
    SLLCE = 0 //sumatoria llegadas CE
    SLLC = 0 //sumatoria llegadas C
    SSE = 0 //sumatoria salida CE
    SSC = 0 //sumatoria salida C
    PEC = 0 //promedio espera C
    PECE = 0 //promedio espera CE
    SACE = 0 //sumatoria arrepentidos CE
    SAC = 0 //sumatoria arrepentidos C
}

function algoritmo(C, CE){

    inicializacion(C, CE)

    while(T < TF){
        metodologia(C, CE)
    }
    /*
    while(NSC > 0 && NSCE > 0){
        metodologia(C, CE)
        TPLL = HV
    }
    */

    PEC = (SSC - SLLC - STAC) / NTC //promedio espera
    PECE = (SSE - SLLCE - STAE) / NTC //promedio espera

    for(let i = 0; i < CE; i++){
        ITOCE[i] = STOCE[i] * 100 / T
    }

    for(let i = 0; i < C; i++){
        ITOC[i] = STOC[i] * 100 / T
    }
}

function metodologia(C, CE){
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
    T = TPLL
    let ia = generar_ia()
    TPLL = T + ia
    let r = Math.random();
    
    if(r<=0.31){ //eminent
        let a = arrepentimiento_c(C)
        if(!a){
            SLLCE += T
            NSCE++
            if(NSCE<=CE){
                let j = TPSC.indexOf(HV) //buscar puesto
                let tae = generar_tae()
                TPSCE[j] = T + tae
                STAE += tae
                STOCE[j] += (T-ITOCE[j])
            }
        }
    }else{ //normal
        let a = arrepentimiento_ce(CE)
        if(!a){
            SLLC += T
            NSC++
            if(NSC<=C){
                let i = TPSC.indexOf(HV) //buscar puesto
                let tac = generar_tac()
                TPSC[i] = T + tac
                STAC += tac
                STOC[i] += (T-ITOC[i])
            }
        }
        
    }
}

function salida_C(i, C, CE){
    T = TPSC[i]
    NSC--
    if(NSC >= C){
        let tac = generar_tac()
        TPSC[i] = T + tac
        STAC += tac
    }else{
        ITOC[i] = T
        TPSC[i] = HV
    }
    SSC += T
    NTC++
}

function salida_CE(i, C, CE){
    T = TPSCE[i]
    NSCE--
    if(NSCE >= CE){
        let tae = generar_tae()
        TPSCE[i] = T + tae
        STAE += tae
    }else{
        ITOCE[i] = T
        TPSCE[i] = HV
    }
    SSE += T
    NTCE++
}

function arrepentimiento_c(C){
    if(NSCE > C + 8){
        let r = Math.random();
        if(r<0.3){
            SAC++
            return true //si es verdadero se arrepintio
        }else{
            return  false //si es falso no se arrepintio
        }
    }else{
        return  false //si es falso no se arrepintio
    }
}

function arrepentimiento_ce(CE){
    if(NSCE > CE + 2){
        let r = Math.random();
        if(r<0.1){
            SACE++
            return true //si es verdadero se arrepintio
        }else{
            return  false //si es falso no se arrepintio
        }
    }else{
        return  false //si es falso no se arrepintio
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
    let r = Math.random();
    return 1/(Math.PI*30.172*(1+((r-127.9)/30.172)^2))
}

function generar_tae(){
    let r = Math.random();
    return ((Math.E)^(-(r/59.033)^0.93206))*(0.9320/59.033)*(r/59.033)^(0.93206-1)
}

function generar_ia(){
    let r = Math.random();
    return (0.03825/57.964)*(1+ (r+0.45892)/57.964)^(-0.03825-1)
}


algoritmo(2,3)
console.log(PEC, PECE)
