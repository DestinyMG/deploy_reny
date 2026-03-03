<script setup>
const creator = {
    name: "Ing Renny Montilla",
    year: new Date().getFullYear(),
    brand: "BIO-TECH"
}
</script>

<template>
    <footer class="mt-auto py-6 px-10 border-t border-white/5 bg-[#020617]/40 backdrop-blur-md">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">

            <div class="flex items-center gap-3">
                <div
                    class="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center border border-white/10 shadow-inner">
                    <span class="text-xs">🧪</span>
                </div>
                <p class="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em]">
                    © {{ creator.year }} <span class="text-slate-300">{{ creator.brand }}</span> — Todos los derechos
                    reservados.
                </p>
            </div>

            <div
                class="flex items-center gap-3 bg-indigo-500/5 px-4 py-2 rounded-xl border border-indigo-500/10 group hover:border-indigo-500/30 transition-all">
                <span class="text-[10px] font-black text-indigo-400 uppercase tracking-widest">
                    Fórmula creada por
                </span>
                <div class="flex items-center gap-2">
                    <div class="h-1 w-4 bg-indigo-500 rounded-full shadow-[0_0_8px_rgba(99,102,241,0.8)]"></div>
                    <p
                        class="text-sm font-black text-white italic tracking-tight group-hover:text-indigo-300 transition-colors">
                        {{ creator.name }}
                    </p>
                </div>
            </div>

        </div>
    </footer>
</template>

<style scoped>
footer {
    /* Asegura que el footer se quede al final si el contenido es poco */
    position: relative;
    z-index: 10;
}
</style>