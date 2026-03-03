<script setup>
defineEmits(['openMenu'])

const creator = {
    name: "Renny Montilla",
    role: "Ing Agronomico",
    formula: "Bₚ = ∑(Pᵢₙ) - ∑(Pₒᵤₜ)",
    avatar: "https://ui-avatars.com/api/?name=Pedro+Perez&background=6366f1&color=fff"
}
</script>

<template>
    <header
        class="h-20 lg:h-22 flex items-center justify-between px-6 lg:px-10 sticky top-0 z-40 bg-[#020617]/90 backdrop-blur-xl border-b border-white/10">

        <div class="flex items-center gap-4">
            <button @click="$emit('openMenu')"
                class="lg:hidden w-10 h-10 flex items-center justify-center bg-gradient-to-tr from-indigo-600 to-violet-600 text-white rounded-xl shadow-lg active:scale-95 transition-all">
                <span class="text-2xl">≡</span>
            </button>

            <div class="flex flex-col">
                <h1 class="text-xl lg:text-2xl font-black italic tracking-tight text-white uppercase leading-none">
                    Balance <span class="text-indigo-500">de</span> Proteínas
                </h1>
                <p class="text-[9px] font-bold text-indigo-400/80 mt-1 tracking-widest uppercase">
                    {{ creator.formula }}
                </p>
            </div>
        </div>

        <div
            class="hidden md:flex items-center p-1.5 pr-4 bg-white/[0.03] border border-white/10 rounded-xl hover:bg-white/[0.06] transition-all duration-300 group cursor-default">

            <div class="relative">
                <img :src="creator.avatar" class="w-10 h-10 rounded-lg object-cover border border-white/20"
                    alt="Foto" />
                <div
                    class="absolute -bottom-1 -right-1 w-3 h-3 bg-emerald-500 border-2 border-[#020617] rounded-full shadow-lg">
                </div>
            </div>

            <div class="ml-3 flex flex-col justify-center">
                <h3 class="text-sm font-bold text-white leading-none group-hover:text-indigo-400 transition-colors">
                    {{ creator.name }}
                </h3>
                <div class="flex items-center gap-1.5 mt-1">
                    <span class="text-[8px] font-black text-slate-500 uppercase tracking-tighter">Ing Agronomico</span>
                    <div class="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></div>
                </div>
            </div>
        </div>

        <div class="md:hidden">
            <img :src="creator.avatar" class="w-10 h-10 rounded-lg border border-white/20 shadow-md" />
        </div>

    </header>
</template>

<style scoped>
h1 {
    animation: slideLeft 0.5s ease-out;
}

@keyframes slideLeft {
    from {
        opacity: 0;
        transform: translateX(-15px);
    }

    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>