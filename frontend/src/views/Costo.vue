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
        <div class="max-w-[1300px] mx-auto px-2 sm:px-6 py-6 space-y-6">

            <!-- Header -->
            <div class="flex flex-col gap-4 border-b border-white/10 pb-6">
                <div class="flex justify-between items-center">
                    <h2 class="text-2xl font-black text-white italic tracking-tighter uppercase">
                        CALCULADORA DE <span class="text-emerald-400">COSTOS</span>
                    </h2>
                    <div class="flex items-center gap-2">
                        <select v-model="moneda"
                            class="bg-[#020617] border border-white/10 rounded-lg px-2 py-1 text-white text-xs font-black uppercase">
                            <option value="$">$ (USD)</option>
                            <option value="€">€ (EUR)</option>
                            <option value="£">£ (GBP)</option>
                            <option value="¥">¥ (JPY)</option>
                        </select>
                        <button v-if="resultados" @click="limpiarCalculo"
                            class="text-[9px] font-black text-red-400 uppercase border border-red-500/20 px-3 py-1.5 rounded-lg">
                            Reiniciar
                        </button>
                    </div>
                </div>

                <!-- Resumen rápido cuando hay resultados -->
                <div v-if="resultados" class="grid grid-cols-3 gap-3">
                    <div class="bg-emerald-500/10 border border-emerald-500/30 p-3 rounded-xl">
                        <p class="text-[8px] font-black text-emerald-400 uppercase">Costo Total</p>
                        <p class="text-xl font-black text-white">{{ formatearMoneda(resultados.costoTotal) }}</p>
                    </div>
                    <div class="bg-indigo-500/10 border border-indigo-500/30 p-3 rounded-xl">
                        <p class="text-[8px] font-black text-indigo-400 uppercase">Cantidad Total</p>
                        <p class="text-xl font-black text-white">{{ resultados.cantidadTotal.toFixed(2) }} kg</p>
                    </div>
                    <div class="bg-amber-500/10 border border-amber-500/30 p-3 rounded-xl">
                        <p class="text-[8px] font-black text-amber-400 uppercase">Precio Promedio</p>
                        <p class="text-xl font-black text-white">{{ formatearMoneda(resultados.precioPromedio) }}/kg</p>
                    </div>
                </div>
            </div>

            <!-- Tabla de ingredientes -->
            <div class="bg-white/5 border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl">
                <!-- Headers -->
                <div
                    class="hidden sm:grid grid-cols-3 p-3 bg-white/5 border-b border-white/10 text-[9px] font-black text-slate-500 uppercase text-center tracking-widest">
                    <div>Ingrediente</div>
                    <div>Precio por kg</div>
                    <div>Cantidad (kg)</div>
                </div>

                <!-- Filas de ingredientes (nombres NO editables) -->
                <div class="divide-y divide-white/5 bg-[#020617]/40">
                    <div v-for="(ing, idx) in ingredientes" :key="idx"
                        class="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 sm:p-3 items-center">

                        <!-- Nombre (NO editable) -->
                        <div class="flex items-center gap-2">
                            <span class="text-lg font-black text-slate-600 italic w-8">#{{ idx + 1 }}</span>
                            <span class="text-white font-medium text-sm">{{ ing.nombre }}</span>
                        </div>

                        <!-- Precio por kilo -->
                        <div class="flex items-center gap-1">
                            <span class="text-emerald-400 font-black text-lg">{{ moneda }}</span>
                            <input type="number" v-model="ing.precioKilo" step="0.01" min="0"
                                class="flex-1 bg-[#020617] border border-white/10 rounded-xl py-2.5 px-3 text-white font-black text-right outline-none focus:border-emerald-500 transition-all"
                                placeholder="0.00" />
                        </div>

                        <!-- Cantidad -->
                        <div class="flex items-center gap-1">
                            <input type="number" v-model="ing.cantidad" step="0.001" min="0"
                                class="flex-1 bg-[#020617] border border-white/10 rounded-xl py-2.5 px-3 text-white font-black text-right outline-none focus:border-emerald-500 transition-all"
                                placeholder="0.000" />
                            <span class="text-slate-500 font-black text-sm">kg</span>
                        </div>
                    </div>
                </div>

                <!-- Botones de acción (siempre de 2 en 2) -->
                <div v-if="!resultados"
                    class="p-4 flex flex-col sm:flex-row gap-3 border-t border-white/10 bg-white/[0.02]">
                    <div class="flex gap-2 w-full sm:w-auto">
                        <button @click="agregarPar"
                            class="flex-1 sm:flex-none px-4 py-3 bg-emerald-500/10 text-emerald-400 rounded-xl text-[10px] font-black uppercase border border-emerald-500/20">
                            + Agregar Par
                        </button>
                        <button @click="eliminarPar" v-if="ingredientes.length > 2"
                            class="flex-1 sm:flex-none px-4 py-3 bg-red-500/10 text-red-400 rounded-xl text-[10px] font-black uppercase border border-red-500/20">
                            - Quitar Par
                        </button>
                    </div>
                    <button @click="calcularCostos"
                        class="w-full sm:ml-auto px-8 py-4 bg-emerald-600 text-white font-black rounded-xl uppercase text-xs tracking-widest shadow-lg active:scale-95 transition-all">
                        Calcular Costos
                    </button>
                </div>
            </div>

            <!-- Mensaje de error -->
            <p v-if="error"
                class="p-3 bg-red-500/10 text-red-400 text-center font-bold rounded-xl text-[10px] uppercase tracking-wider">
                {{ error }}
            </p>

            <!-- Tabla de resultados detallados -->
            <transition name="slide-up">
                <div v-if="resultados" class="space-y-6">

                    <!-- Tabla detallada -->
                    <div class="bg-[#020617] border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl">
                        <div class="overflow-x-auto">
                            <table class="w-full text-center">
                                <thead
                                    class="bg-white/5 border-b border-white/10 text-[9px] font-black text-slate-500 uppercase tracking-widest">
                                    <tr>
                                        <th class="p-4">#</th>
                                        <th class="p-4">Ingrediente</th>
                                        <th class="p-4">Precio/kg</th>
                                        <th class="p-4">Cantidad</th>
                                        <th class="p-4 text-right pr-6">Costo Total</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-white/5">
                                    <tr v-for="item in resultados.detalles" :key="item.index">
                                        <td class="p-4 font-black text-slate-500 italic">{{ item.index }}</td>
                                        <td class="p-4 font-medium text-white">{{ item.nombre }}</td>
                                        <td class="p-4 text-emerald-400 font-black">{{ formatearMoneda(item.precioKilo)
                                            }}/kg</td>
                                        <td class="p-4 text-white font-black">{{ item.cantidad.toFixed(3) }} kg</td>
                                        <td class="p-4 text-right pr-6 font-mono font-black text-emerald-400 text-lg">
                                            {{ formatearMoneda(item.costoTotal) }}
                                        </td>
                                    </tr>
                                </tbody>
                                <tfoot class="bg-emerald-600/10 border-t border-emerald-500/30">
                                    <tr class="font-black italic text-sm">
                                        <td colspan="4"
                                            class="p-4 text-[9px] text-emerald-400 uppercase tracking-tighter text-left">
                                            COSTO TOTAL
                                        </td>
                                        <td class="p-4 text-right pr-6 text-white text-xl">
                                            {{ formatearMoneda(resultados.costoTotal) }}
                                        </td>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>

                    <!-- Resumen adicional -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="bg-indigo-500/5 border border-white/10 p-6 rounded-2xl">
                            <p class="text-[8px] font-black text-slate-500 uppercase mb-2">Detalle de Cantidades</p>
                            <div class="space-y-2">
                                <div v-for="item in resultados.detalles" :key="item.index"
                                    class="flex justify-between text-sm">
                                    <span class="text-slate-400">{{ item.nombre }}</span>
                                    <span class="text-white font-black">{{ item.cantidad.toFixed(2) }} kg</span>
                                </div>
                                <div class="border-t border-white/10 pt-2 mt-2 flex justify-between font-black">
                                    <span class="text-indigo-400">Total</span>
                                    <span class="text-white">{{ resultados.cantidadTotal.toFixed(2) }} kg</span>
                                </div>
                            </div>
                        </div>

                        <div class="bg-amber-500/5 border border-white/10 p-6 rounded-2xl">
                            <p class="text-[8px] font-black text-slate-500 uppercase mb-2">Análisis de Costos</p>
                            <div class="space-y-3">
                                <div>
                                    <p class="text-xs text-slate-400 mb-1">Precio Promedio Ponderado</p>
                                    <p class="text-3xl font-black text-amber-400">{{
                                        formatearMoneda(resultados.precioPromedio) }}/kg</p>
                                </div>
                                <div class="pt-2 border-t border-white/10">
                                    <p class="text-xs text-slate-400 mb-1">Distribución del Costo</p>
                                    <div v-for="item in resultados.detalles" :key="item.index" class="mb-1">
                                        <div class="flex justify-between text-xs">
                                            <span class="text-slate-400">{{ item.nombre }}</span>
                                            <span class="text-white">{{ ((item.costoTotal / resultados.costoTotal) *
                                                100).toFixed(2) }}%</span>
                                        </div>
                                        <div class="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                                            <div class="bg-emerald-500 h-1 rounded-full"
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
.slide-up-enter-active {
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-up-enter-from {
    opacity: 0;
    transform: translateY(30px);
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}
</style>