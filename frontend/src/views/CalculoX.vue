<script setup>
import { ref, watch, nextTick } from 'vue'
import BaseAdmin from '../components/BaseAdmin.vue'

// --- ESTADO PRINCIPAL ---
const objetivo = ref(null)
const ingredientes = ref([
    { valor: null, nutri: { ms: null, em: null, fdn: null, cen: null, fc: null, ee: null, ca: null, p: null } },
    { valor: null, nutri: { ms: null, em: null, fdn: null, cen: null, fc: null, ee: null, ca: null, p: null } },
    { valor: null, nutri: { ms: null, em: null, fdn: null, cen: null, fc: null, ee: null, ca: null, p: null } },
    { valor: null, nutri: { ms: null, em: null, fdn: null, cen: null, fc: null, ee: null, ca: null, p: null } },
])

const resultados = ref(null)
const error = ref('')

// --- VARIABLES DE CONTROL PARA PREVENIR BUCLES ---
const actualizando = ref(false)
const ultimaActualizacion = ref(0)

const nombresNutrientes = {
    ms: 'MS',
    em: 'EM',
    fdn: 'FDN',
    cen: 'Cen',
    fc: 'FC',
    ee: 'EE',
    ca: 'Ca',
    p: 'P'
}

// --- GESTIÓN DE FILAS ---
const agregarPar = () => {
    const nuevo = () => ({ valor: null, nutri: { ms: null, em: null, fdn: null, cen: null, fc: null, ee: null, ca: null, p: null } })
    ingredientes.value.push(nuevo(), nuevo())
}

const eliminarPar = () => {
    if (ingredientes.value.length > 4) ingredientes.value.splice(-2, 2)
}

const limpiarCalculo = () => {
    resultados.value = null
    error.value = ''
}

// --- LÓGICA DE CÁLCULO ---
const calcularX = () => {
    error.value = '';
    const datos = ingredientes.value.map(i => parseFloat(i.valor))
    const n = datos.length
    const mitad = n / 2
    const obj = parseFloat(objetivo.value)

    if (isNaN(obj) || datos.some(v => isNaN(v))) {
        error.value = "⚠️ Completa todos los campos."; return
    }

    const menores = datos.filter(v => v < obj)
    const mayores = datos.filter(v => v > obj)

    if (menores.length !== mitad || mayores.length !== mitad) {
        error.value = `❌ Balance: Se requieren ${mitad} valores < ${obj} y ${mitad} > ${obj}.`; return
    }

    const K = mayores.reduce((a, b) => a + b, 0) - menores.reduce((a, b) => a + b, 0)
    let x_final = new Array(n)
    for (let i = 0; i < mitad; i++) {
        x_final[i] = (datos[n - 1 - i] - obj) / K
        x_final[n - 1 - i] = (obj - datos[i]) / K
    }

    resultados.value = {
        detalles: ingredientes.value.map((ing, idx) => ({
            index: idx + 1,
            proporcionX: x_final[idx] * 100,
            x_decimal: x_final[idx],
            aporteProteico: ing.valor * x_final[idx]
        })),
        sumaX: 100,
        aporteTotal: obj,
        nutriFinales: { ms: 0, em: 0, fdn: 0, cen: 0, fc: 0, ee: 0, ca: 0, p: 0 }
    }
    actualizarNutrientes()
}

// --- FUNCIÓN ACTUALIZAR NUTRIENTES OPTIMIZADA ---
const actualizarNutrientes = () => {
    if (!resultados.value) return

    // Prevenir ejecuciones múltiples en menos de 300ms
    const ahora = Date.now()
    if (ahora - ultimaActualizacion.value < 300) {
        console.warn('Actualización muy frecuente prevenida')
        return
    }
    ultimaActualizacion.value = ahora

    let m = { ms: 0, em: 0, fdn: 0, cen: 0, fc: 0, ee: 0, ca: 0, p: 0 }
    ingredientes.value.forEach((ing, idx) => {
        const prop = resultados.value.detalles[idx].x_decimal
        Object.keys(m).forEach(key => {
            const valorNutri = parseFloat(ing.nutri[key]) || 0
            m[key] += (valorNutri * prop)
        })
    })
    resultados.value.nutriFinales = m
}

// --- ÚNICO WATCH PARA INGREDIENTES (SIMPLIFICADO) ---
watch(ingredientes, () => {
    // Si ya existen resultados (las proporciones X), actualiza los nutrientes al escribir
    if (resultados.value) {
        actualizarNutrientes()
    }
}, { deep: true })

// --- WATCH PARA OBJETIVO (MEJORADO) ---
watch(objetivo, (nuevoValor, valorAnterior) => {
    if (resultados.value && nuevoValor !== valorAnterior) {
        // Limpiar resultados si cambia el objetivo
        resultados.value = null
    }
})

</script>

<!-- EL TEMPLATE SE QUEDA IGUAL, SIN CAMBIOS -->

<template>
    <BaseAdmin>
        <div class="max-w-[1300px] mx-auto px-2 sm:px-6 py-6 space-y-6">

            <div class="flex flex-col gap-4 border-b border-white/10 pb-6">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-black text-white italic tracking-tighter uppercase">DISEÑO <span
                            class="text-indigo-500">X</span></h2>
                    <button v-if="resultados" @click="limpiarCalculo"
                        class="text-[9px] font-black text-red-400 uppercase border border-red-500/20 px-3 py-1.5 rounded-lg">
                        Reiniciar
                    </button>
                </div>

                <div
                    class="bg-[#020617] p-4 rounded-2xl border border-indigo-500/30 flex justify-between items-center shadow-xl">
                    <span
                        class="text-[10px] font-black text-indigo-400 uppercase leading-none">Proteína<br>Objetivo:</span>
                    <div class="flex items-center gap-2">
                        <input type="number" v-model="objetivo" :disabled="resultados"
                            class="w-16 bg-transparent text-white font-black text-3xl text-right outline-none disabled:opacity-50"
                            placeholder="0" />
                        <span class="text-indigo-400 font-black text-xl">%</span>
                    </div>
                </div>
            </div>

            <div class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl">
                <div
                    class="hidden sm:grid grid-cols-2 p-3 bg-white/5 border-b border-white/10 text-[9px] font-black text-slate-500 uppercase text-center tracking-widest">
                    <div>Identificador</div>
                    <div>Proteína (%)</div>
                </div>

                <div class="divide-y divide-white/5 bg-[#020617]/40">
                    <div v-for="(ing, idx) in ingredientes" :key="idx"
                        class="flex sm:grid sm:grid-cols-2 items-center justify-between p-4 sm:p-3">
                        <div class="text-lg font-black text-slate-600 italic uppercase">a{{ idx + 1 }}</div>
                        <div class="flex justify-end sm:justify-center">
                            <input type="number" v-model="ing.valor" :disabled="resultados"
                                class="w-24 sm:w-32 bg-[#020617] border border-white/10 rounded-xl py-2.5 text-white font-black text-center text-lg outline-none focus:border-indigo-500 disabled:opacity-30 transition-all shadow-inner"
                                placeholder="0.0" />
                        </div>
                    </div>
                </div>

                <div v-if="!resultados"
                    class="p-4 flex flex-col sm:flex-row gap-3 border-t border-white/10 bg-white/[0.02]">
                    <div class="flex gap-2 w-full sm:w-auto">
                        <button @click="agregarPar"
                            class="flex-1 sm:flex-none px-4 py-3 bg-emerald-500/10 text-emerald-400 rounded-xl text-[10px] font-black uppercase border border-emerald-500/20">+
                            Par</button>
                        <button @click="eliminarPar"
                            class="flex-1 sm:flex-none px-4 py-3 bg-red-500/10 text-red-400 rounded-xl text-[10px] font-black uppercase border border-red-500/20">-
                            Par</button>
                    </div>
                    <button @click="calcularX"
                        class="w-full sm:ml-auto px-8 py-4 bg-indigo-600 text-white font-black rounded-xl uppercase text-xs tracking-widest shadow-lg active:scale-95 transition-all">
                        Calcular Proporciones
                    </button>
                </div>
            </div>

            <p v-if="error"
                class="p-3 bg-red-500/10 text-red-400 text-center font-bold rounded-xl text-[10px] uppercase tracking-wider">
                {{ error }}</p>

            <transition name="slide-up">
                <div v-if="resultados" class="space-y-8">

                    <div class="bg-[#020617] border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl">
                        <div class="overflow-x-auto">
                            <table class="w-full text-center min-w-[300px]">
                                <thead
                                    class="bg-white/5 border-b border-white/10 text-[9px] font-black text-slate-500 uppercase tracking-widest">
                                    <tr>
                                        <th class="p-4">ID</th>
                                        <th class="p-4 text-indigo-400 italic">Inclusión (X)</th>
                                        <th class="p-4 text-right pr-6">Aporte</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-white/5">
                                    <tr v-for="item in resultados.detalles" :key="item.index">
                                        <td class="p-4 font-black text-slate-500 italic text-lg uppercase">a{{
                                            item.index }}</td>
                                        <td class="p-4">
                                            <span class="text-white font-black text-2xl tracking-tighter">
                                                {{ item.proporcionX.toFixed(2) }}
                                                <span class="text-sm font-medium text-slate-400 ml-1">KG</span>
                                            </span>
                                        </td>
                                        <td class="p-4 text-right pr-6 font-mono font-black text-indigo-400 text-lg">{{
                                            item.aporteProteico.toFixed(2) }}%</td>
                                    </tr>
                                </tbody>
                                <tfoot class="bg-indigo-600/10 border-t border-indigo-500/30">
                                    <tr class="font-black italic text-sm">
                                        <td class="p-4 text-[9px] text-indigo-400 uppercase tracking-tighter text-left">
                                            Totales</td>
                                        <td class="p-4 text-emerald-400 text-xl font-black">100kg</td>
                                        <td class="p-4 text-right pr-6 text-white text-xl">{{
                                            resultados.aporteTotal.toFixed(2) }}%</td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>

                    <div class="space-y-6">
                        <div class="flex items-center gap-3">
                            <div class="h-px flex-1 bg-white/10"></div>
                            <h3 class="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">Carga
                                Nutricional</h3>
                            <div class="h-px flex-1 bg-white/10"></div>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden">
                            <div class="overflow-x-auto custom-scroll">
                                <table class="w-full text-center border-collapse min-w-[700px]">
                                    <thead class="bg-white/5 text-[8px] font-black text-slate-500 uppercase">
                                        <tr>
                                            <th class="p-3 border-r border-white/5">ID</th>
                                            <th v-for="(label, key) in nombresNutrientes" :key="key" class="p-3">{{
                                                label }}</th>
                                        </tr>
                                    </thead>
                                    <tbody class="divide-y divide-white/5 bg-[#020617]/40">
                                        <tr v-for="(ing, idx) in ingredientes" :key="idx">
                                            <td class="p-3 font-black text-slate-600 italic">a{{ idx + 1 }}</td>
                                            <td class="p-3" v-for="key in Object.keys(nombresNutrientes)" :key="key">
                                                <input type="number" v-model="ing.nutri[key]"
                                                    class="w-12 bg-transparent border-b border-indigo-500/20 text-center text-white font-bold text-xs outline-none focus:border-indigo-500 transition-all"
                                                    placeholder="0" />
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                            <div v-for="(val, key) in resultados.nutriFinales" :key="key"
                                class="bg-indigo-500/5 border border-white/10 p-4 rounded-2xl text-center">
                                <p class="text-[8px] font-black text-slate-500 uppercase mb-1">{{ nombresNutrientes[key]
                                }}</p>
                                <div class="text-xl font-black text-indigo-100 italic">
                                    {{ val.toFixed(2) }}<span class="text-[10px] ml-0.5 text-indigo-500">{{ key === 'em'
                                        ? '' : '' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </transition>
        </div>
    </BaseAdmin>
</template>

<style scoped>
.slide-up-enter-active {
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from {
    opacity: 0;
    transform: translateY(30px);
}

.custom-scroll::-webkit-scrollbar {
    height: 6px;
}

.custom-scroll::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.2);
    border-radius: 10px;
}

input:disabled {
    cursor: not-allowed;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}
</style>