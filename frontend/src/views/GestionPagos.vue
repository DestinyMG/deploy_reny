<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import BaseAdmin from '../components/BaseAdmin.vue'

const pagos = ref([])
const loading = ref(true)

// Configuración base de SweetAlert para evitar repetir estilos
const swalDark = {
    background: '#050505',
    color: '#fff',
    customClass: {
        popup: 'rounded-[2rem] border border-white/10 shadow-2xl',
        confirmButton: 'rounded-xl font-black px-6 py-3 uppercase text-[10px] tracking-widest',
        cancelButton: 'rounded-xl font-black px-6 py-3 uppercase text-[10px] tracking-widest'
    }
}

const obtenerPagos = async () => {
    loading.value = true
    try {
        const token = localStorage.getItem('access_token')
        const response = await axios.get('http://localhost:8000/api/pagos/reportar/', {
            headers: { Authorization: `Bearer ${token}` }
        })
        pagos.value = response.data
    } catch (error) {
        console.error("Error cargando pagos", error)
    } finally {
        loading.value = false
    }
}

const aprobarPago = async (pago) => {
    const confirm = await Swal.fire({
        ...swalDark,
        title: '<span class="text-white font-black italic uppercase tracking-tighter">¿CONFIRMAR ACTIVACIÓN?</span>',
        html: `<p class="text-gray-400 text-xs uppercase font-bold tracking-widest">Se activarán <b>${pago.plan_solicitado === 'MONTHLY' ? '30 días' : '365 días'}</b> para <br><span class="text-emerald-400">${pago.usuario_nombre} ${pago.usuario_apellido}</span></p>`,
        icon: 'question',
        iconColor: '#10b981',
        showCancelButton: true,
        confirmButtonColor: '#059669',
        cancelButtonColor: '#1f1f1f',
        confirmButtonText: 'SÍ, APROBAR Y ACTIVAR',
        cancelButtonText: 'CANCELAR'
    })

    if (confirm.isConfirmed) {
        try {
            const token = localStorage.getItem('access_token')
            // El backend procesará la membresía y ELIMINARÁ el registro automáticamente
            await axios.patch(`http://localhost:8000/api/pagos/reportar/${pago.id}/`,
                { estado: 'APROBADO' },
                { headers: { Authorization: `Bearer ${token}` } }
            )

            Swal.fire({
                ...swalDark,
                title: '¡SISTEMA ACTUALIZADO!',
                text: 'Membresía activada. El reporte ha sido procesado y removido.',
                icon: 'success',
                iconColor: '#10b981',
                timer: 2000,
                showConfirmButton: false
            })
            obtenerPagos() // Refresca la lista (el registro ya no existirá)
        } catch (e) {
            Swal.fire({
                ...swalDark,
                title: 'ERROR',
                text: 'No se pudo procesar la solicitud.',
                icon: 'error',
                confirmButtonColor: '#ef4444'
            })
        }
    }
}

const rechazarPago = async (pago) => {
    const confirm = await Swal.fire({
        ...swalDark,
        title: '<span class="text-white font-black italic uppercase tracking-tighter">¿RECHAZAR REPORTE?</span>',
        text: 'Esta acción eliminará el capture y el registro permanentemente.',
        icon: 'warning',
        iconColor: '#ef4444',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#1f1f1f',
        confirmButtonText: 'SÍ, ELIMINAR TODO',
        cancelButtonText: 'CANCELAR'
    })

    if (confirm.isConfirmed) {
        try {
            const token = localStorage.getItem('access_token')
            // Ejecutamos el DELETE directo al backend
            await axios.delete(`http://localhost:8000/api/pagos/reportar/${pago.id}/`, {
                headers: { Authorization: `Bearer ${token}` }
            })

            Swal.fire({
                ...swalDark,
                title: 'ELIMINADO',
                text: 'El reporte ha sido rechazado y borrado.',
                icon: 'success',
                timer: 1500,
                showConfirmButton: false
            })
            obtenerPagos()
        } catch (e) {
            Swal.fire({
                ...swalDark,
                title: 'ERROR',
                text: 'No se pudo eliminar el registro.',
                icon: 'error'
            })
        }
    }
}

onMounted(obtenerPagos)
</script>

<template>
    <BaseAdmin>
        <div class="max-w-[1200px] mx-auto px-6 py-10">
            <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
                <div>
                    <h2 class="text-3xl font-black text-white italic uppercase tracking-tighter">
                        Validación de <span class="text-purple-500">Pagos Entrantes</span>
                    </h2>
                    <p class="text-slate-500 text-[10px] font-black uppercase tracking-[0.2em]">Cola de aprobación
                        temporal</p>
                </div>
                <button @click="obtenerPagos"
                    class="p-3 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 transition-all">
                    <span v-if="!loading">🔄</span>
                    <span v-else class="inline-block animate-spin">⏳</span>
                </button>
            </header>

            <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="i in 3" :key="i"
                    class="h-96 bg-white/5 animate-pulse rounded-[2rem] border border-white/10"></div>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="pago in pagos" :key="pago.id"
                    class="bg-[#0f0f0f] border border-white/10 rounded-[2rem] overflow-hidden flex flex-col shadow-xl hover:border-white/20 transition-all group">

                    <div class="h-64 bg-black relative overflow-hidden">
                        <img :src="pago.comprobante"
                            class="w-full h-full object-contain p-2 group-hover:scale-105 transition-transform duration-500" />
                        <div class="absolute inset-0 bg-gradient-to-t from-[#0f0f0f] to-transparent opacity-60"></div>
                        <a :href="pago.comprobante" target="_blank"
                            class="absolute bottom-4 right-4 bg-white/10 backdrop-blur-md p-2 rounded-xl text-white text-[10px] font-black uppercase tracking-widest border border-white/10 hover:bg-white/20 transition-all">
                            Ver Original 🔍
                        </a>
                    </div>

                    <div class="p-6 space-y-5">
                        <div class="flex justify-between items-start">
                            <div>
                                <p class="text-[9px] font-black text-purple-400 uppercase tracking-widest mb-1">
                                    Remitente Nexus</p>
                                <h3 class="text-white font-black text-lg uppercase italic leading-none">{{
                                    pago.usuario_nombre }}</h3>
                                <h3 class="text-white font-black text-lg uppercase italic mb-2">{{ pago.usuario_apellido
                                    }}</h3>
                                <div class="flex items-center gap-2">
                                    <span
                                        class="text-[10px] text-slate-500 font-bold tracking-tighter bg-white/5 px-2 py-0.5 rounded">C.I:
                                        {{ pago.usuario_ci }}</span>
                                </div>
                            </div>
                            <div class="text-right">
                                <span class="block text-[9px] font-black text-emerald-400 uppercase italic">Plan
                                    Solicitado</span>
                                <span class="text-xl font-black text-white italic tracking-tighter uppercase">{{
                                    pago.plan_solicitado }}</span>
                            </div>
                        </div>

                        <div class="pt-4 border-t border-white/5 flex gap-3">
                            <button @click="aprobarPago(pago)"
                                class="flex-1 py-4 bg-emerald-600 hover:bg-emerald-500 text-white text-[10px] font-black rounded-2xl uppercase tracking-[0.1em] transition-all active:scale-95 shadow-lg shadow-emerald-900/20">
                                Aprobar
                            </button>
                            <button @click="rechazarPago(pago)"
                                class="px-6 py-4 bg-red-600/10 hover:bg-red-600 text-red-500 hover:text-white text-[10px] font-black rounded-2xl uppercase transition-all border border-red-600/20 active:scale-95">
                                Rechazar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="pagos.length === 0 && !loading"
                class="flex flex-col items-center justify-center py-32 bg-white/[0.02] rounded-[3rem] border border-dashed border-white/10">
                <span class="text-4xl mb-4 opacity-20">🛡️</span>
                <p class="text-slate-500 font-black uppercase tracking-[0.3em] text-xs">Sin reportes pendientes</p>
            </div>
        </div>
    </BaseAdmin>
</template>