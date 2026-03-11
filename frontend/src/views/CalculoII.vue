<script setup>
import { ref, watch } from 'vue'
import BaseAdmin from '../components/BaseAdmin.vue'

// --- LÓGICA DEL CÁLCULO BASE ---
const inputs = ref({ pa: null, pb: null, pe: null, pv: null })
const resultados = ref(null)
const error = ref('')

// --- LÓGICA DE APORTES NUTRICIONALES ---
const mostrarAportes = ref(false)
const nutrientes = ref([
    { id: 'ms', label: ' Materia Seca (MS)', a: 0, b: 0 },
    { id: 'em', label: 'En. Metabólica (EM)', a: 0, b: 0 },
    { id: 'fdb', label: 'Fibra Det. Neutro (FDN)', a: 0, b: 0 },
    { id: 'cen', label: 'Ceniza', a: 0, b: 0 },
    { id: 'fc', label: 'Fibra Cruda', a: 0, b: 0 },
    { id: 'ee', label: 'Ext. Etéreo (EE)', a: 0, b: 0 },
    { id: 'ca', label: 'Calcio (Ca)', a: 0, b: 0 },
    { id: 'p', label: 'Fósforo (P)', a: 0, b: 0 },
])

// --- FACTOR DE VITAMINA ---
const factorVitamina = () => {
    if (!inputs.value.pv) return 1
    const vit = parseFloat(inputs.value.pv) || 0
    return (100 - vit) / 100
}

const calcular = () => {
    const { pa, pb, pe, pv } = inputs.value
    error.value = ''; resultados.value = null; mostrarAportes.value = false

    if (pa === null || pb === null || pe === null) {
        error.value = "⚠️ Completa todos los campos."; return
    }

    // Validación sin considerar vitamina
    if (!(pa < pe && pe < pb)) {
        error.value = "❌ Error: Debe cumplirse %A < %E < %B"; return
    }

    const K = pb - pa
    const pa_calc = (pb - pe) / K
    const pb_calc = (pe - pa) / K

    // Aplicar factor de vitamina a los pesos
    const factor = factorVitamina()
    const pesoA_ajustado = pa_calc * factor * 100
    const pesoB_ajustado = pb_calc * factor * 100

    resultados.value = {
        pesoA: pesoA_ajustado, // Pesos ajustados por vitamina
        pesoB: pesoB_ajustado,
        pesoA_base: pa_calc * 100, // Pesos base (sin vitamina) para referencia
        pesoB_base: pb_calc * 100,
        finalA: parseFloat((pa_calc * pa).toFixed(2)),
        finalB: parseFloat((pe - (pa_calc * pa)).toFixed(2)),
        finalE: pe,
        vitamina: pv || 0,
        factor: factor * 100
    }
}

// Fórmula: (InputNutrienteA * (PesoA_ajustado/100)) + (InputNutrienteB * (PesoB_ajustado/100))
const calcularTotalNutriente = (n) => {
    if (!resultados.value) return 0
    const x1 = resultados.value.pesoA / 100
    const x2 = resultados.value.pesoB / 100
    return ((n.a * x1) + (n.b * x2)).toFixed(2)
}

// Watch para cuando cambia la vitamina, recalcular si hay resultados
// VERSIÓN SEGURA
watch(() => inputs.value.pv, (nuevoValor, valorAnterior) => {
    // Solo recalcular si:
    // 1. Hay resultados previos
    // 2. El valor realmente cambió (no es el mismo)
    // 3. El nuevo valor es un número válido
    if (resultados.value &&
        nuevoValor !== valorAnterior &&
        !isNaN(parseFloat(nuevoValor))) {

        // Usar setTimeout para evitar ciclos
        setTimeout(() => {
            calcular()
        }, 0)
    }
}, { deep: false }) // Importante: no deep
</script>

<template>
    <BaseAdmin>
        <div class="max-w-6xl mx-auto space-y-8 pb-10">

            <div class="flex flex-col gap-2">
                <h2 class="text-3xl font-black text-white tracking-tight italic">
                    <span class="text-indigo-500">#</span> CÁLCULO II
                </h2>
                <p class="text-slate-500 font-medium tracking-wide text-sm uppercase">Determinación de Mezclas Proteicas
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div class="lg:col-span-5 bg-white/5 border border-white/10 p-8 rounded-[2.5rem] backdrop-blur-md">
                    <div class="space-y-6">
                        <div v-for="(label, key) in { pa: '%A (Ingrediente A)', pb: '%B (Ingrediente B)', pe: '%E (Objetivo)' }"
                            :key="key">
                            <label
                                class="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3 ml-1">{{
                                    label }}</label>
                            <input type="number" v-model="inputs[key]"
                                class="w-full bg-[#020617] border border-white/10 rounded-2xl px-6 py-4 text-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all"
                                placeholder="0.00" />
                        </div>

                        <!-- Nuevo input para vitamina -->
                        <div>
                            <label
                                class="block text-[10px] font-black text-emerald-500 uppercase tracking-widest mb-3 ml-1">kg
                                Vitamina a Restar (Opcional)</label>
                            <input type="number" v-model="inputs.pv"
                                class="w-full bg-[#020617] border border-emerald-500/30 rounded-2xl px-6 py-4 text-white focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 outline-none transition-all"
                                placeholder="0.00" />
                        </div>

                        <button @click="calcular"
                            class="w-full py-5 bg-indigo-600 hover:bg-indigo-500 text-white font-black rounded-2xl transition-all shadow-xl shadow-indigo-600/20 active:scale-95">
                            CALCULAR BALANCE
                        </button>

                        <!-- Indicador del factor de vitamina -->
                        <div v-if="inputs.pv"
                            class="text-center p-2 bg-emerald-500/5 rounded-xl border border-emerald-500/20">
                            <span class="text-[9px] font-black text-emerald-400 uppercase tracking-wider">
                                Factor de ajuste: {{ ((100 - parseFloat(inputs.pv || 0)) / 100).toFixed(2) }} |
                                Restando {{ inputs.pv }}kg de vitamina
                            </span>
                        </div>

                        <p v-if="error"
                            class="p-4 bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-bold rounded-2xl text-center animate-bounce">
                            {{ error }}</p>
                    </div>
                </div>

                <div
                    class="lg:col-span-7 bg-gradient-to-br from-indigo-500/10 to-transparent border border-white/10 p-8 rounded-[2.5rem] min-h-[400px] flex items-center justify-center relative">
                    <div v-if="resultados" class="w-full space-y-8 animate-page-in">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="bg-[#020617] p-6 rounded-3xl border border-white/5 shadow-inner">
                                <span class="text-[10px] text-indigo-400 font-black uppercase tracking-widest">Peso
                                    A</span>
                                <div class="text-3xl font-black text-white mt-1">{{ resultados.pesoA.toFixed(2) }}<span
                                        class="text-sm ml-1 text-slate-600">kg</span></div>
                                <div v-if="resultados.vitamina > 0" class="text-[8px] text-slate-500 mt-1">
                                    Base: {{ resultados.pesoA_base.toFixed(2) }}kg
                                </div>
                            </div>
                            <div class="bg-[#020617] p-6 rounded-3xl border border-white/5 shadow-inner">
                                <span class="text-[10px] text-indigo-400 font-black uppercase tracking-widest">Peso
                                    B</span>
                                <div class="text-3xl font-black text-white mt-1">{{ resultados.pesoB.toFixed(2) }}<span
                                        class="text-sm ml-1 text-slate-600">kg</span></div>
                                <div v-if="resultados.vitamina > 0" class="text-[8px] text-slate-500 mt-1">
                                    Base: {{ resultados.pesoB_base.toFixed(2) }}kg
                                </div>
                            </div>
                        </div>

                        <!-- Mostrar suma de pesos -->
                        <div class="flex justify-between items-center px-2">
                            <span class="text-[10px] font-black text-slate-500 uppercase tracking-widest">Suma
                                Total:</span>
                            <span class="text-xl font-black text-emerald-400">{{ (resultados.pesoA +
                                resultados.pesoB).toFixed(2) }}kg</span>
                            <span v-if="resultados.vitamina > 0" class="text-[8px] text-slate-500">
                                (100% - {{ resultados.vitamina }}kg vitamina)
                            </span>
                        </div>

                        <div
                            class="bg-indigo-600 p-8 rounded-3xl shadow-2xl shadow-indigo-600/20 relative overflow-hidden">
                            <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl font-black italic">RESULT</div>
                            <p class="text-[10px] font-black text-indigo-200 uppercase tracking-[0.3em] mb-6">Balance de
                                Proteína Final</p>
                            <div class="space-y-4">
                                <div class="flex justify-between border-b border-indigo-400/30 pb-2">
                                    <span class="text-indigo-100 font-bold">Aporte A</span>
                                    <span class="font-black text-white">{{ resultados.finalA }}%</span>
                                </div>
                                <div class="flex justify-between border-b border-indigo-400/30 pb-2">
                                    <span class="text-indigo-100 font-bold">Aporte B</span>
                                    <span class="font-black text-white">{{ resultados.finalB }}%</span>
                                </div>

                                <div class="flex justify-between pt-2">
                                    <span class="text-white font-black text-xl italic uppercase">Total Objetivo
                                        (%E)</span>
                                    <span
                                        class="text-3xl font-black text-white underline decoration-indigo-300 underline-offset-8">
                                        {{ resultados.finalE }}%KG
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-else class="text-center group">
                        <div class="text-6xl mb-4 group-hover:scale-110 transition-transform duration-500">📉</div>
                        <p class="text-slate-500 font-black uppercase tracking-[0.3em] text-xs">Aún no hay resultados
                        </p>
                    </div>
                </div>
            </div>

            <div v-if="resultados" class="animate-page-in space-y-6">
                <div class="flex items-center justify-between border-b border-white/10 pb-4">
                    <h3 class="text-xl font-black text-white italic tracking-tight">
                        <span class="text-emerald-500">?</span> ¿Desea calcular aportes nutricionales?
                    </h3>
                    <button @click="mostrarAportes = !mostrarAportes"
                        class="px-6 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full font-black text-[10px] uppercase hover:bg-emerald-500 hover:text-white transition-all">
                        {{ mostrarAportes ? 'Ocultar Panel' : 'Configurar Nutrientes' }}
                    </button>
                </div>

                <div v-if="mostrarAportes" class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <div class="lg:col-span-8 bg-[#020617] border border-white/10 rounded-[2.5rem] overflow-hidden">
                        <table class="w-full text-left">
                            <thead class="bg-white/5 border-b border-white/10">
                                <tr>
                                    <th class="p-4 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                                        Nutriente</th>
                                    <th
                                        class="p-4 text-[10px] font-black text-indigo-400 uppercase tracking-widest text-center">
                                        Ingr. A (%)</th>
                                    <th
                                        class="p-4 text-[10px] font-black text-indigo-400 uppercase tracking-widest text-center">
                                        Ingr. B (%)</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-white/5">
                                <tr v-for="n in nutrientes" :key="n.id"
                                    class="group hover:bg-white/[0.02] transition-colors">
                                    <td class="p-4 text-xs font-bold text-slate-300">{{ n.label }}</td>
                                    <td class="p-2 text-center"><input type="number" v-model="n.a"
                                            class="w-24 bg-white/5 border border-white/10 rounded-xl p-2 text-center text-white outline-none focus:border-emerald-500 transition-all text-xs"
                                            placeholder="0" /></td>
                                    <td class="p-2 text-center"><input type="number" v-model="n.b"
                                            class="w-24 bg-white/5 border border-white/10 rounded-xl p-2 text-center text-white outline-none focus:border-emerald-500 transition-all text-xs"
                                            placeholder="0" /></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div
                        class="lg:col-span-4 bg-gradient-to-br from-emerald-500/20 to-transparent border border-emerald-500/20 p-8 rounded-[2.5rem]">
                        <p class="text-[10px] font-black text-emerald-400 uppercase tracking-[0.3em] mb-6">Total
                            Aportado en Mezcla</p>
                        <div class="space-y-4">
                            <div v-for="n in nutrientes" :key="'res-' + n.id"
                                class="flex justify-between items-center group">
                                <span
                                    class="text-[10px] font-bold text-slate-400 group-hover:text-slate-200 transition-colors uppercase">{{
                                        n.id }}</span>
                                <div class="flex items-center gap-2">
                                    <span class="text-sm font-black text-white">{{ calcularTotalNutriente(n) }}</span>
                                    <span class="text-[9px] text-emerald-500/50 font-black italic">TOTAL</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </BaseAdmin>
</template>

<style scoped>
.animate-page-in {
    animation: pageIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes pageIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>