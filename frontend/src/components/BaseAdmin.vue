<script setup>
import { ref } from 'vue'
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'
import Footer from './Footer.vue';

const isSidebarOpen = ref(false)
</script>

<template>
    <div class="flex min-h-screen bg-[#020617] text-slate-200">
        <Sidebar :isOpen="isSidebarOpen" @close="isSidebarOpen = false" />

        <div class="flex-1 lg:ml-72 flex flex-col min-w-0">
            <Header @openMenu="isSidebarOpen = true" />

            <main class="p-4 lg:p-10 pt-2 bg-gradient-to-b from-[#0f172a]/50 to-[#020617]">
                <div class="max-w-7xl mx-auto animate-page-in">
                    <slot />
                </div>
            </main>
            <Footer />
        </div>
    </div>
</template>

<style scoped>
.animate-page-in {
    animation: pageIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes pageIn {
    from {
        opacity: 0;
        transform: scale(0.99);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>