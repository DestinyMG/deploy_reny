<script setup>
import { ref, onMounted, computed } from 'vue' // Importamos computed
import axios from 'axios'
import Swal from 'sweetalert2'
import BaseAdmin from '../components/BaseAdmin.vue'

// --- ESTADO ---
const usuarios = ref([])
const loading = ref(true)
const searchQuery = ref('') // Sincronizado con el input

// Configuración de Axios
const token = localStorage.getItem('access_token')
const api = axios.create({
    baseURL: 'https://deploy-reny.onrender.com/api/',
    headers: { Authorization: `Bearer ${token}` }
})

// --- LÓGICA DE FILTRADO EN TIEMPO REAL ---
// Esta función se ejecuta automáticamente cada vez que escribes en searchQuery
const usuariosFiltrados = computed(() => {
    const query = searchQuery.value.toLowerCase().trim()

    // Si el buscador está vacío, devolvemos la lista completa
    if (!query) return usuarios.value

    return usuarios.value.filter(user => {
        const nombreCompleto = `${user.nombre} ${user.apellido}`.toLowerCase()
        const email = user.email?.toLowerCase() || ''
        const ci = user.ci?.toString() || ''

        return nombreCompleto.includes(query) ||
            email.includes(query) ||
            ci.includes(query)
    })
})

// --- MÉTODOS ---
const obtenerUsuarios = async () => {
    loading.value = true
    try {
        const response = await api.get('usuarios/')
        usuarios.value = response.data.filter(u => u.rol === 'USER')
    } catch (error) {
        toast('Error al cargar usuarios', 'error')
    } finally {
        loading.value = false
    }
}

const gestionarPlan = async (user) => {
    const { value: formValues } = await Swal.fire({
        title: `<span class="text-white font-black italic tracking-tighter uppercase">ACTUALIZAR PLAN</span>`,
        background: '#0f172a',
        color: '#fff',
        html: `
            <div class="flex flex-col gap-4 text-left p-2">
                <div>
                    <label class="text-[10px] font-black text-emerald-400 uppercase tracking-widest mb-2 block">Seleccionar Plan</label>
                    <select id="swal-plan" class="w-full bg-[#020617] border border-white/10 rounded-xl p-3 text-white outline-none focus:border-emerald-500 transition-all">
                        <option value="FREE" ${user.plan === 'FREE' ? 'selected' : ''}>FREE</option>
                        <option value="MONTHLY" ${user.plan === 'MONTHLY' ? 'selected' : ''}>MONTHLY (30 Días)</option>
                        <option value="ANNUAL" ${user.plan === 'ANNUAL' ? 'selected' : ''}>ANNUAL (365 Días)</option>
                    </select>
                </div>
                <div>
                    <label class="text-[10px] font-black text-emerald-400 uppercase tracking-widest mb-2 block">Vencimiento Manual</label>
                    <input type="date" id="swal-fecha" class="w-full bg-[#020617] border border-white/10 rounded-xl p-3 text-white outline-none focus:border-emerald-500 transition-all" 
                    value="${user.fecha_vencimiento ? user.fecha_vencimiento.split('T')[0] : ''}">
                </div>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'GUARDAR CAMBIOS',
        cancelButtonText: 'CANCELAR',
        confirmButtonColor: '#10b981',
        cancelButtonColor: '#ef4444',
        customClass: {
            popup: 'rounded-[2rem] border border-white/10 shadow-2xl',
            confirmButton: 'rounded-xl font-black px-6 py-3',
            cancelButton: 'rounded-xl font-black px-6 py-3'
        },
        preConfirm: () => {
            const plan = document.getElementById('swal-plan').value
            const fecha = document.getElementById('swal-fecha').value
            if (!plan) return Swal.showValidationMessage('El plan es obligatorio')
            return { plan: plan, fecha_vencimiento: fecha }
        }
    })

    if (formValues) {
        try {
            await api.patch(`usuarios/${user.id}/`, formValues)
            toast('Suscripción actualizada', 'success')
            obtenerUsuarios()
        } catch (error) {
            toast('No se pudo actualizar', 'error')
        }
    }
}

const toast = (title, icon) => {
    Swal.fire({
        title, icon, toast: true, position: 'top-end',
        showConfirmButton: false, timer: 3000,
        background: '#0f172a', color: '#fff'
    })
}

const formatearFecha = (fecha) => {
    if (!fecha) return 'SIN FECHA'
    return new Date(fecha).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(obtenerUsuarios)
</script>

<template>
    <BaseAdmin>
        <div class="max-w-[1300px] mx-auto px-2 sm:px-6 py-6 space-y-6">

            <div class="flex flex-col gap-4 border-b border-white/10 pb-6">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <h2 class="text-2xl font-black text-white italic tracking-tighter uppercase">
                        GESTIÓN DE <span class="text-emerald-400">USUARIOS</span>
                    </h2>

                    <div class="w-full sm:w-80">
                        <div class="relative">
                            <input v-model="searchQuery" type="text" placeholder="BUSCAR POR NOMBRE, EMAIL O C.I..."
                                class="w-full bg-white/5 border border-white/10 rounded-xl py-3 px-4 text-xs font-black text-white outline-none focus:border-emerald-500 transition-all uppercase placeholder:text-slate-600 shadow-inner" />
                            <div class="absolute right-4 top-3 text-slate-600">
                                <span v-if="!searchQuery">🔍</span>
                                <button v-else @click="searchQuery = ''"
                                    class="text-emerald-400 hover:text-white transition-colors">✕</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div class="bg-emerald-500/10 border border-emerald-500/30 p-4 rounded-[1.5rem]">
                        <p class="text-[8px] font-black text-emerald-400 uppercase tracking-widest">Activos</p>
                        <p class="text-2xl font-black text-white">{{usuarios.filter(u => u.tiene_acceso).length}}</p>
                    </div>
                    <div class="bg-red-500/10 border border-red-500/30 p-4 rounded-[1.5rem]">
                        <p class="text-[8px] font-black text-red-400 uppercase tracking-widest">Vencidos</p>
                        <p class="text-2xl font-black text-white">{{usuarios.filter(u => !u.tiene_acceso).length}}</p>
                    </div>
                    <div
                        class="bg-indigo-500/10 border border-indigo-500/30 p-4 rounded-[1.5rem] col-span-2 sm:col-span-1">
                        <p class="text-[8px] font-black text-indigo-400 uppercase tracking-widest">Total Registrados</p>
                        <p class="text-2xl font-black text-white">{{ usuarios.length }}</p>
                    </div>
                </div>
            </div>

            <div class="bg-[#020617]/40 border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl">
                <div class="overflow-x-auto">
                    <table class="w-full text-left">
                        <thead
                            class="bg-white/5 border-b border-white/10 text-[9px] font-black text-slate-500 uppercase tracking-widest text-center">
                            <tr>
                                <th class="p-5 text-left">Usuario</th>
                                <th class="p-5">Estado</th>
                                <th class="p-5">Plan</th>
                                <th class="p-5">Vencimiento</th>
                                <th class="p-5 text-right">Acción</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/5">
                            <tr v-if="loading">
                                <td colspan="5" class="p-20 text-center">
                                    <div class="inline-block animate-spin text-2xl text-emerald-400">⏳</div>
                                    <p class="text-[10px] font-black text-slate-500 uppercase mt-4 tracking-widest">
                                        Procesando Base de Datos...
                                    </p>
                                </td>
                            </tr>

                            <tr v-for="user in usuariosFiltrados" :key="user.id"
                                class="hover:bg-white/[0.02] transition-all group border-l-2 border-transparent hover:border-emerald-500">
                                <td class="p-5">
                                    <div class="flex flex-col">
                                        <span class="text-sm font-black text-white uppercase">{{ user.nombre }} {{
                                            user.apellido }}</span>
                                        <span class="text-[10px] font-medium text-slate-500 lowercase">{{ user.email
                                        }}</span>
                                        <span class="text-[9px] font-black text-indigo-400 mt-1 uppercase">C.I: {{
                                            user.ci || 'N/A' }}</span>
                                    </div>
                                </td>
                                <td class="p-5 text-center">
                                    <span
                                        :class="user.tiene_acceso ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20' : 'bg-red-500/10 text-red-500 border-red-500/20'"
                                        class="px-3 py-1.5 rounded-lg text-[9px] font-black uppercase border italic">
                                        {{ user.tiene_acceso ? 'Activo' : 'Vencido' }}
                                    </span>
                                </td>
                                <td class="p-5 text-center font-black text-white italic text-xs">
                                    {{ user.plan }}
                                </td>
                                <td class="p-5 text-center">
                                    <div class="flex flex-col gap-0.5">
                                        <span class="text-xs font-black text-slate-300 uppercase">
                                            {{ formatearFecha(user.fecha_vencimiento) }}
                                        </span>
                                        <span v-if="user.tiene_acceso"
                                            class="text-[8px] font-black text-emerald-400 italic">
                                            {{ user.dias_restantes }} DÍAS RESTANTES
                                        </span>
                                    </div>
                                </td>
                                <td class="p-5 text-right">
                                    <button @click="gestionarPlan(user)"
                                        class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-[10px] font-black rounded-xl uppercase tracking-widest transition-all active:scale-90 shadow-lg shadow-emerald-900/20">
                                        Gestionar
                                    </button>
                                </td>
                            </tr>

                            <tr v-if="usuariosFiltrados.length === 0 && !loading">
                                <td colspan="5"
                                    class="p-10 text-center italic text-slate-500 text-xs font-bold uppercase tracking-widest">
                                    No se encontraron usuarios que coincidan con "{{ searchQuery }}"
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="text-right text-[10px] font-black text-slate-600 uppercase italic px-4">
                Mostrando {{ usuariosFiltrados.length }} de {{ usuarios.length }} usuarios
            </div>

        </div>
    </BaseAdmin>
</template>

<style scoped>
/* Transiciones suaves para SweetAlert */
:deep(.swal2-container) {
    backdrop-filter: blur(8px);
}

:deep(.swal2-popup) {
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
}

input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1);
    cursor: pointer;
}
</style>