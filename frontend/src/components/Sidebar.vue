<script setup>
import { RouterLink } from 'vue-router'

defineProps(['isOpen'])
defineEmits(['close'])

// Obtenemos el usuario directamente del localStorage
const userData = JSON.parse(localStorage.getItem('user_data') || '{}')

const logout = () => {
    localStorage.clear()
    window.location.href = '/login'
}
</script>

<template>
    <div v-if="isOpen" @click="$emit('close')" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden">
    </div>

    <aside :class="isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
        class="fixed inset-y-0 left-0 w-72 bg-[#050505] transition-transform duration-300 ease-in-out z-50 flex flex-col p-6 text-slate-300 border-r border-white/10 shadow-[20px_0_50px_rgba(0,0,0,0.5)]">

        <button @click="$emit('close')"
            class="lg:hidden absolute right-4 top-6 text-2xl text-slate-500 hover:text-white transition-colors">✕</button>

        <div class="flex items-center gap-3 px-2 mb-12">
            <div
                class="w-10 h-10 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-xl flex items-center justify-center text-white text-2xl shadow-lg shadow-purple-500/20 transform -rotate-3">
                🧪
            </div>
            <span class="text-white font-black tracking-tighter text-xl uppercase italic">Nexus<span
                    class="text-purple-500">Lab</span></span>
        </div>

        <nav class="flex-1 space-y-3 overflow-y-auto pr-2 custom-scroll">

            <template v-if="userData.rol === 'ADMIN'">
                <p class="text-[10px] font-black text-slate-600 uppercase tracking-[3px] mb-4 px-4">Administración</p>

                <router-link to="/usuarios" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group relative overflow-hidden border border-transparent"
                    active-class="bg-purple-500/10 text-purple-400 border-purple-500/20 shadow-[0_0_20px_rgba(168,85,247,0.1)]"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">

                    <span class="text-xl group-hover:rotate-12 transition-transform duration-300">👥</span>

                    <div class="relative h-6 flex-1 overflow-hidden font-bold">
                        <span
                            class="absolute inset-0 transition-transform duration-300 group-hover:-translate-y-full flex items-center">
                            Usuarios
                        </span>
                        <span
                            class="absolute inset-0 transition-transform duration-300 translate-y-full group-hover:translate-y-0 flex items-center text-emerald-400">
                            Usuarios & Pagos
                        </span>
                    </div>
                </router-link>

                <router-link to="/pagos" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group border border-transparent"
                    active-class="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_20px_rgba(16,185,129,0.1)]"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">
                    <span class="text-xl group-hover:scale-110 transition-transform">💳</span>
                    <span class="font-bold">Validar Pagos</span>
                </router-link>
            </template>

            <div class="pt-6">
                <p class="text-[10px] font-black text-slate-600 uppercase tracking-[3px] mb-4 px-4">Herramientas</p>

                <router-link to="/calculoii" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group border border-transparent"
                    active-class="bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">
                    <span class="text-xl group-hover:scale-110 transition-transform">📐</span>
                    <span class="font-bold">Cálculo II</span>
                </router-link>

                <router-link to="/calculox" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group border border-transparent"
                    active-class="bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">
                    <span
                        class="text-2xl leading-none group-hover:scale-125 transition-transform duration-300 ease-out inline-block">
                        ∞
                    </span>
                    <span class="font-bold">Cálculo X</span>
                </router-link>

                <router-link to="/vitaminax" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group border border-transparent"
                    active-class="bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">

                    <span class="group-hover:scale-125 transition-transform duration-300 ease-out inline-block">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                            class="w-6 h-6">
                            <path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"></path>
                            <path d="m8.5 8.5 7 7"></path>
                        </svg>
                    </span>

                    <span class="font-bold">Vitaminax</span>
                </router-link>

                <router-link to="/costo" @click="$emit('close')"
                    class="flex items-center gap-3 px-4 py-3.5 rounded-2xl transition-all group border border-transparent"
                    active-class="bg-indigo-500/10 text-indigo-400 border-indigo-500/20"
                    inactive-class="hover:bg-white/5 text-slate-400 hover:text-white">
                    <span class="text-xl group-hover:scale-110 transition-transform">💰</span>
                    <span class="font-bold">Gestión de Costos</span>
                </router-link>
            </div>
        </nav>

        <button @click="logout"
            class="mt-auto flex items-center justify-center gap-3 px-4 py-4 bg-red-500/5 hover:bg-red-500 text-red-500 hover:text-white rounded-2xl transition-all font-black group border border-red-500/10 hover:border-red-500 uppercase text-[10px] tracking-widest">
            <span class="text-lg group-hover:translate-x-1 transition-transform">🚪</span>
            <span>Cerrar Sesión</span>
        </button>
    </aside>
</template>

<style scoped>
/* Scrollbar personalizada para el menú si hay muchas opciones */
.custom-scroll::-webkit-scrollbar {
    width: 4px;
}

.custom-scroll::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scroll::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

/* Transición suave para el cambio de texto */
.group:hover .translate-y-full {
    transform: translateY(0);
}

.group:hover .translate-y-0 {
    transform: translateY(-100%);
}
</style>