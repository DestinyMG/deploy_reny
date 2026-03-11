<script setup>
import { ref, watch } from 'vue'
import BaseAdmin from '../components/BaseAdmin.vue'

// --- ESTADO PRINCIPAL ---
const ingredientes = ref([
    { nombre: 'Proteína A', precioKilo: null, cantidad: null },
    { nombre: 'Proteína B', precioKilo: null, cantidad: null },
])

const moneda = ref('$')
const resultados = ref(null)
const error = ref('')

// --- GESTIÓN DE FILAS (SIEMPRE DE 2 EN 2) ---
const agregarPar = () => {
    const numActual = ingredientes.value.length
    const nuevaLetraA = String.fromCharCode(65 + numActual) // Siguiente letra
    const nuevaLetraB = String.fromCharCode(66 + numActual) // Siguiente + 1

    ingredientes.value.push(
        { nombre: `Proteína ${nuevaLetraA}`, precioKilo: null, cantidad: null },
        { nombre: `Proteína ${nuevaLetraB}`, precioKilo: null, cantidad: null }
    )
}

const eliminarPar = () => {
    if (ingredientes.value.length > 2) {
        // Eliminar las últimas 2 filas
        ingredientes.value.splice(-2, 2)
        // Limpiar resultados si existían
        if (resultados.value) resultados.value = null
    }
}

const limpiarCalculo = () => {
    resultados.value = null
    error.value = ''
}

// --- CÁLCULOS ---
const calcularCostos = () => {
    error.value = ''

    // Validar que todos los campos estén completos
    for (let ing of ingredientes.value) {
        if (ing.precioKilo === null || ing.precioKilo === '' ||
            ing.cantidad === null || ing.cantidad === '') {
            error.value = '⚠️ Completa todos los campos de precio y cantidad'
            return
        }

        const precio = parseFloat(ing.precioKilo)
        const cantidad = parseFloat(ing.cantidad)

        if (isNaN(precio) || isNaN(cantidad)) {
            error.value = '⚠️ Ingresa valores numéricos válidos'
            return
        }
    }

    calcularResultados()
}

const calcularResultados = () => {
    const detalles = ingredientes.value.map((ing, idx) => {
        const precio = parseFloat(ing.precioKilo)
        const cantidad = parseFloat(ing.cantidad)
        const costoTotal = precio * cantidad

        return {
            index: idx + 1,
            nombre: ing.nombre,
            precioKilo: precio,
            cantidad: cantidad,
            costoTotal: costoTotal
        }
    })

    const costoTotalGeneral = detalles.reduce((sum, item) => sum + item.costoTotal, 0)
    const cantidadTotal = detalles.reduce((sum, item) => sum + item.cantidad, 0)
    const precioPromedio = cantidadTotal > 0 ? costoTotalGeneral / cantidadTotal : 0

    resultados.value = {
        detalles: detalles,
        costoTotal: costoTotalGeneral,
        cantidadTotal: cantidadTotal,
        precioPromedio: precioPromedio
    }
}

// Watch para actualizar automáticamente cuando cambien los valores
watch(ingredientes, () => {
    if (resultados.value) {
        // Verificar si todos los campos están completos antes de recalcular
        const todosCompletos = ingredientes.value.every(ing =>
            ing.precioKilo !== null && ing.precioKilo !== '' &&
            ing.cantidad !== null && ing.cantidad !== ''
        )

        if (todosCompletos) {
            calcularResultados()
        }
    }
}, { deep: true })

// Formateador de moneda
const formatearMoneda = (valor) => {
    if (valor === null || valor === undefined || isNaN(valor)) return `${moneda.value}0.00`
    return `${moneda.value}${valor.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}`
}
</script>

<template>
    <BaseAdmin>
        <div class="max-w-[1300px] mx-auto px-3 sm:px-6 py-6 space-y-6">

            <div class="flex flex-col gap-6 border-b border-white/10 pb-6">
                <div class="flex flex-col xs:flex-row justify-between items-start xs:items-center gap-4">
                    <h2 class="text-xl sm:text-2xl font-black text-white italic tracking-tighter uppercase shrink-0">
                        CALCULADORA DE <span class="text-emerald-400">COSTOS</span>
                    </h2>
                    <div class="flex items-center gap-2 w-full xs:w-auto">
                        <select v-model="moneda"
                            class="flex-1 xs:flex-none bg-[#020617] border border-white/10 rounded-lg px-3 py-2 text-white text-xs font-black uppercase outline-none focus:border-emerald-500">
                            <option value="$">$ (USD)</option>
                            <option value="€">€ (EUR)</option>
                            <option value="£">£ (GBP)</option>
                            <option value="¥">¥ (JPY)</option>
                        </select>
                        <button v-if="resultados" @click="limpiarCalculo"
                            class="flex-1 xs:flex-none text-[10px] font-black text-red-400 uppercase border border-red-500/20 px-4 py-2 rounded-lg bg-red-500/5 hover:bg-red-500/10 transition-colors">
                            Reiniciar
                        </button>
                    </div>
                </div>

                <div v-if="resultados" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div
                        class="bg-emerald-500/10 border border-emerald-500/30 p-4 rounded-xl flex flex-col justify-center min-w-0">
                        <p class="text-[9px] font-black text-emerald-400 uppercase mb-1 tracking-wider">Costo Total</p>
                        <p class="text-xl sm:text-2xl font-black text-white break-all leading-none">
                            {{ formatearMoneda(resultados.costoTotal) }}
                        </p>
                    </div>
                    <div
                        class="bg-indigo-500/10 border border-indigo-500/30 p-4 rounded-xl flex flex-col justify-center min-w-0">
                        <p class="text-[9px] font-black text-indigo-400 uppercase mb-1 tracking-wider">Cantidad Total
                        </p>
                        <p class="text-xl sm:text-2xl font-black text-white break-all leading-none">
                            {{ resultados.cantidadTotal.toFixed(2) }} <span class="text-xs text-indigo-400">kg</span>
                        </p>
                    </div>
                    <div
                        class="bg-amber-500/10 border border-amber-500/30 p-4 rounded-xl flex flex-col justify-center min-w-0">
                        <p class="text-[9px] font-black text-amber-400 uppercase mb-1 tracking-wider">Precio Promedio
                        </p>
                        <p class="text-xl sm:text-2xl font-black text-white break-all leading-none">
                            {{ formatearMoneda(resultados.precioPromedio) }}<span
                                class="text-xs text-amber-400">/kg</span>
                        </p>
                    </div>
                </div>
            </div>

            <div
                class="bg-white/5 border border-white/10 rounded-[1.5rem] sm:rounded-[2rem] overflow-hidden shadow-2xl">
                <div
                    class="hidden sm:grid grid-cols-3 p-4 bg-white/5 border-b border-white/10 text-[10px] font-black text-slate-500 uppercase text-center tracking-widest">
                    <div>Ingrediente</div>
                    <div>Precio por kg</div>
                    <div>Cantidad (kg)</div>
                </div>

                <div class="divide-y divide-white/5 bg-[#020617]/40">
                    <div v-for="(ing, idx) in ingredientes" :key="idx"
                        class="flex flex-col sm:grid sm:grid-cols-3 gap-4 p-5 sm:p-3 items-center">

                        <div class="flex items-center gap-3 w-full">
                            <span class="text-xl font-black text-slate-700 italic shrink-0">#{{ idx + 1 }}</span>
                            <div class="flex-1 bg-white/5 px-3 py-2 rounded-lg border border-white/5">
                                <span class="text-white font-bold text-sm truncate block">{{ ing.nombre }}</span>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 sm:contents gap-3 w-full">
                            <div class="flex items-center gap-2 group">
                                <span class="text-emerald-400 font-black text-lg w-4">{{ moneda }}</span>
                                <input type="number" v-model="ing.precioKilo" step="0.01" min="0"
                                    class="w-full bg-[#020617] border border-white/10 rounded-xl py-3 px-3 text-white font-black text-right outline-none focus:border-emerald-500 transition-all shadow-inner"
                                    placeholder="0.00" />
                            </div>

                            <div class="flex items-center gap-2 group">
                                <input type="number" v-model="ing.cantidad" step="0.001" min="0"
                                    class="w-full bg-[#020617] border border-white/10 rounded-xl py-3 px-3 text-white font-black text-right outline-none focus:border-emerald-500 transition-all shadow-inner"
                                    placeholder="0.000" />
                                <span class="text-slate-500 font-black text-xs uppercase w-4">kg</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="!resultados"
                    class="p-5 flex flex-col sm:flex-row gap-3 border-t border-white/10 bg-white/[0.02]">
                    <div class="grid grid-cols-2 gap-3 w-full sm:w-auto">
                        <button @click="agregarPar"
                            class="px-4 py-4 bg-emerald-500/10 text-emerald-400 rounded-xl text-[10px] font-black uppercase border border-emerald-500/20 active:scale-95 transition-all">
                            + Agregar Par
                        </button>
                        <button @click="eliminarPar" v-if="ingredientes.length > 2"
                            class="px-4 py-4 bg-red-500/10 text-red-400 rounded-xl text-[10px] font-black uppercase border border-red-500/20 active:scale-95 transition-all">
                            - Quitar Par
                        </button>
                    </div>
                    <button @click="calcularCostos"
                        class="w-full sm:ml-auto sm:w-64 py-4 bg-emerald-600 text-white font-black rounded-xl uppercase text-[11px] tracking-[0.2em] shadow-lg active:scale-95 transition-all">
                        Calcular Costos
                    </button>
                </div>
            </div>

            <transition name="slide-up">
                <div v-if="resultados" class="space-y-6 pb-10">

                    <div
                        class="bg-[#020617] border border-white/10 rounded-[1.5rem] sm:rounded-[2rem] overflow-hidden shadow-2xl">
                        <div class="overflow-x-auto scrollbar-hide">
                            <table class="w-full text-center min-w-[600px] border-collapse">
                                <thead
                                    class="bg-white/5 border-b border-white/10 text-[10px] font-black text-slate-500 uppercase tracking-widest">
                                    <tr>
                                        <th class="p-4 text-left pl-6">#</th>
                                        <th class="p-4 text-left">Ingrediente</th>
                                        <th class="p-4">Precio/kg</th>
                                        <th class="p-4">Cantidad</th>
                                        <th class="p-4 text-right pr-6">Costo Total</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-white/5">
                                    <tr v-for="item in resultados.detalles" :key="item.index"
                                        class="hover:bg-white/[0.02] transition-colors">
                                        <td class="p-4 text-left pl-6 font-black text-slate-600 italic">#{{ item.index
                                        }}</td>
                                        <td class="p-4 text-left font-bold text-white uppercase text-xs">{{ item.nombre
                                        }}</td>
                                        <td class="p-4 text-emerald-400 font-black text-sm">{{
                                            formatearMoneda(item.precioKilo) }}/kg</td>
                                        <td class="p-4 text-white/70 font-black text-sm">{{ item.cantidad.toFixed(2) }}
                                            kg</td>
                                        <td
                                            class="p-4 text-right pr-6 font-mono font-black text-emerald-400 text-lg sm:text-xl break-all">
                                            {{ formatearMoneda(item.costoTotal) }}
                                        </td>
                                    </tr>
                                </tbody>
                                <tfoot class="bg-emerald-600/10 border-t border-emerald-500/30">
                                    <tr class="font-black italic">
                                        <td colspan="4"
                                            class="p-5 text-[10px] text-emerald-400 uppercase text-left pl-6 tracking-widest">
                                            COSTO TOTAL FINAL</td>
                                        <td class="p-5 text-right pr-6 text-white text-xl sm:text-3xl break-all">{{
                                            formatearMoneda(resultados.costoTotal) }}</td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div class="bg-indigo-500/5 border border-white/10 p-6 rounded-[2rem]">
                            <p class="text-[10px] font-black text-indigo-400 uppercase mb-6 tracking-widest">
                                Distribución de Cantidades</p>
                            <div class="space-y-4">
                                <div v-for="item in resultados.detalles" :key="item.index"
                                    class="flex items-center justify-between group">
                                    <span
                                        class="text-slate-400 text-xs font-bold group-hover:text-white transition-colors">{{
                                            item.nombre }}</span>
                                    <div class="flex items-center gap-3">
                                        <span class="text-white font-black text-sm">{{ item.cantidad.toFixed(2)
                                        }}</span>
                                        <span class="text-indigo-500/50 text-[10px] font-black uppercase">kg</span>
                                    </div>
                                </div>
                                <div class="border-t border-white/10 pt-4 mt-2 flex justify-between items-end">
                                    <span class="text-indigo-400 font-black text-xs uppercase">Suma Total</span>
                                    <span class="text-white text-2xl font-black italic">{{
                                        resultados.cantidadTotal.toFixed(2) }} <span class="text-xs">kg</span></span>
                                </div>
                            </div>
                        </div>

                        <div class="bg-amber-500/5 border border-white/10 p-6 rounded-[2rem]">
                            <p class="text-[10px] font-black text-amber-400 uppercase mb-6 tracking-widest">Análisis de
                                Impacto Económico</p>
                            <div class="space-y-5">
                                <div class="bg-[#020617] p-4 rounded-xl border border-white/5">
                                    <p class="text-[9px] text-slate-500 font-black uppercase mb-1">Precio Promedio
                                        Ponderado</p>
                                    <p class="text-3xl font-black text-amber-400 italic break-all leading-none">
                                        {{ formatearMoneda(resultados.precioPromedio) }}<span
                                            class="text-xs ml-1">/kg</span>
                                    </p>
                                </div>

                                <div class="space-y-3">
                                    <p class="text-[9px] text-slate-500 font-black uppercase tracking-tighter">
                                        Participación en el Costo Total</p>
                                    <div v-for="item in resultados.detalles" :key="item.index">
                                        <div class="flex justify-between text-[10px] mb-1 font-bold">
                                            <span class="text-slate-400">{{ item.nombre }}</span>
                                            <span class="text-emerald-400">{{ ((item.costoTotal / resultados.costoTotal)
                                                * 100).toFixed(2) }}%</span>
                                        </div>
                                        <div class="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                                            <div class="bg-emerald-500 h-full rounded-full transition-all duration-1000"
                                                :style="{ width: (item.costoTotal / resultados.costoTotal * 100) + '%' }">
                                            </div>
                                        </div>
                                    </div>
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
/* Reset de inputs para evitar desbordamientos visuales */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type=number] {
    -moz-appearance: textfield;
}

/* Scroll suave para tablas en móvil */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

/* Animación de entrada */
.slide-up-enter-active {
    transition: all 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from {
    opacity: 0;
    transform: translateY(40px);
}

/* Ajustes para pantallas muy angostas */
@media (max-width: 360px) {
    .text-xl {
        font-size: 1.125rem;
    }

    .text-2xl {
        font-size: 1.25rem;
    }
}
</style>