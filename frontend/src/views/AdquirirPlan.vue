<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Swal from 'sweetalert2'
import { useRouter } from 'vue-router'

const router = useRouter()
const planSeleccionado = ref('MONTHLY')
const archivoSeleccionado = ref(null)
const vistaPrevia = ref(null)
const isLoading = ref(false)
const userData = ref(null)

onMounted(() => {
    const data = localStorage.getItem('user_data')
    if (data) {
        userData.value = JSON.parse(data)
    }
})

const manejarArchivo = (e) => {
    const file = e.target.files[0]
    if (file) {
        archivoSeleccionado.value = file
        vistaPrevia.value = URL.createObjectURL(file)
    }
}

const enviarPago = async () => {
    if (!archivoSeleccionado.value) {
        Swal.fire({
            title: '¡Falta el comprobante!',
            text: 'Por favor, sube una captura de pantalla de tu transferencia.',
            icon: 'warning',
            background: '#0f0f0f',
            color: '#fff'
        })
        return
    }

    isLoading.value = true
    const formData = new FormData()
    formData.append('comprobante', archivoSeleccionado.value)
    formData.append('plan_solicitado', planSeleccionado.value)

    try {
        const token = localStorage.getItem('access_token')
        await axios.post('https://deploy-reny.onrender.com/api/pagos/reportar/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': `Bearer ${token}`
            }
        })

        await Swal.fire({
            title: '¡Reporte Enviado!',
            text: 'Tu pago está siendo verificado. Te notificaremos cuando tu acceso sea activado.',
            icon: 'success',
            background: '#0f0f0f',
            color: '#fff',
            confirmButtonColor: '#7c3aed'
        })

        router.push('/login') // Lo regresamos al login o a una pantalla de espera

    } catch (error) {
        console.error(error)
        Swal.fire('Error', 'Hubo un problema al subir tu pago.', 'error')
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <div class="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden font-sans">
        <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-900/20 rounded-full blur-[120px]"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-emerald-900/10 rounded-full blur-[120px]">
        </div>

        <div
            class="relative z-10 w-full max-w-2xl bg-[#0f0f0f]/80 backdrop-blur-xl rounded-[2.5rem] border border-white/10 p-8 md:p-12 shadow-2xl">

            <header class="text-center mb-10">
                <span class="text-xs font-black text-purple-500 uppercase tracking-[0.3em]">Membresía Nexus</span>
                <h1 class="text-4xl font-black text-white italic uppercase tracking-tighter mt-2">
                    Activa tu <span class="text-emerald-400">Acceso</span>
                </h1>
                <p class="text-gray-400 mt-4 text-sm">Hola <span class="text-white font-bold">{{ userData?.nombre
                }}</span>, selecciona un plan y sube tu comprobante para continuar.</p>
            </header>

            <div class="space-y-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button @click="planSeleccionado = 'MONTHLY'"
                        :class="planSeleccionado === 'MONTHLY' ? 'border-purple-500 bg-purple-500/10 ring-1 ring-purple-500' : 'border-white/5 bg-white/5'"
                        class="relative p-6 rounded-3xl border-2 transition-all text-left overflow-hidden group">
                        <div v-if="planSeleccionado === 'MONTHLY'"
                            class="absolute top-3 right-3 text-purple-500 text-xl">✔</div>
                        <p class="text-xs font-black text-purple-400 uppercase mb-1">Plan Mensual</p>
                        <p class="text-2xl font-black text-white italic">$10.00 <span
                                class="text-xs text-gray-500">/mes</span></p>
                        <p class="text-[10px] text-gray-400 mt-2 font-bold uppercase tracking-widest">30 Días de Acceso
                            Total</p>
                    </button>

                    <!-- <button @click="planSeleccionado = 'ANNUAL'"
                        :class="planSeleccionado === 'ANNUAL' ? 'border-emerald-500 bg-emerald-500/10 ring-1 ring-emerald-500' : 'border-white/5 bg-white/5'"
                        class="relative p-6 rounded-3xl border-2 transition-all text-left overflow-hidden group">
                        <div v-if="planSeleccionado === 'ANNUAL'"
                            class="absolute top-3 right-3 text-emerald-500 text-xl">✔</div>
                        <p class="text-xs font-black text-emerald-400 uppercase mb-1">Plan Anual</p>
                        <p class="text-2xl font-black text-white italic">$100.00 <span
                                class="text-xs text-gray-500">/año</span></p>
                        <p class="text-[10px] text-gray-400 mt-2 font-bold uppercase tracking-widest">Ahorra 2 meses de
                            suscripción</p>
                    </button> -->
                </div>

                <div class="space-y-4">
                    <label class="block text-[10px] font-black text-gray-500 uppercase tracking-widest ml-2">Comprobante
                        de Pago (Capture)</label>
                    <div class="relative group">
                        <input type="file" @change="manejarArchivo" accept="image/*" class="hidden" id="pago-file" />
                        <label for="pago-file"
                            class="cursor-pointer flex flex-col items-center justify-center w-full min-h-[200px] border-2 border-dashed border-white/10 rounded-[2rem] bg-white/[0.02] hover:bg-white/[0.05] hover:border-purple-500/50 transition-all overflow-hidden relative">

                            <div v-if="!vistaPrevia" class="flex flex-col items-center p-6 text-center">
                                <div
                                    class="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform">
                                    🖼️</div>
                                <span class="text-xs font-black text-gray-400 uppercase tracking-wider">Toca para
                                    seleccionar imagen</span>
                                <span class="text-[9px] text-gray-600 mt-2">Formatos aceptados: JPG, PNG</span>
                            </div>

                            <img v-else :src="vistaPrevia" class="w-full h-full object-contain max-h-[300px] p-2" />
                        </label>
                    </div>
                </div>

                <button @click="enviarPago" :disabled="isLoading"
                    class="w-full py-5 bg-white text-black font-black rounded-[1.5rem] uppercase tracking-[0.2em] text-xs shadow-[0_10px_30px_rgba(255,255,255,0.1)] hover:bg-purple-600 hover:text-white hover:scale-[1.02] transition-all active:scale-95 disabled:opacity-50">
                    {{ isLoading ? 'Procesando Envío...' : 'Confirmar Reporte de Pago' }}
                </button>
            </div>

            <p class="text-center text-[9px] text-gray-600 uppercase font-black tracking-widest mt-8">
                Tus datos están protegidos bajo encriptación JWT de 256 bits
            </p>
        </div>
    </div>
</template>