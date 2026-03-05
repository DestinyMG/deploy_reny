<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2' // Importamos para avisos profesionales

const router = useRouter()
const currentView = ref('login')
const showPassword = ref(false)
const isLoading = ref(false)

const form = ref({
    login: { email: '', password: '' },
    register: { nombre: '', apellido: '', ci: '', email: '', password: '' }
})

// Configuración de Notificaciones (Toasts) oscuros
const toast = (title, icon = 'error') => {
    Swal.fire({
        title,
        icon,
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: '#0f0f0f',
        color: '#fff',
        iconColor: icon === 'success' ? '#10b981' : '#ef4444'
    })
}

// Función para manejar el Login
const handleLogin = async () => {
    isLoading.value = true
    try {
        const response = await axios.post('https://deploy-reny.onrender.com/api/login/', {
            email: form.value.login.email,
            password: form.value.login.password
        })

        const token = response.data.access
        const user = response.data.user

        localStorage.setItem('access_token', token)
        localStorage.setItem('user_data', JSON.stringify(user))
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        toast(`Bienvenido, ${user.nombre}`, 'success')

        if (user.rol === 'ADMIN') {
            router.push('/usuarios')
        } else {
            user.tiene_acceso ? router.push('/calculoii') : router.push('/plan')
        }

    } catch (error) {
        const msg = error.response?.data?.detail || "Credenciales inválidas"
        toast(msg)
    } finally {
        isLoading.value = false
    }
}

// Función para manejar el Registro con validaciones de campos Únicos
const handleRegister = async () => {
    isLoading.value = true
    try {
        await axios.post('https://deploy-reny.onrender.com/api/usuarios/', form.value.register)

        await Swal.fire({
            title: '¡CUENTA CREADA!',
            text: 'Tu registro ha sido exitoso. Ahora puedes iniciar sesión.',
            icon: 'success',
            background: '#0f0f0f',
            color: '#fff',
            confirmButtonColor: '#7c3aed'
        })

        currentView.value = 'login'
        // Limpiamos el formulario de registro
        form.value.register = { nombre: '', apellido: '', ci: '', email: '', password: '' }

    } catch (error) {
        console.error(error.response?.data)
        const errors = error.response?.data

        // Lógica para avisar sobre C.I. o Email duplicados
        if (errors?.email) {
            toast("El correo electrónico ya está registrado")
        } else if (errors?.ci) {
            toast("La Cédula de Identidad (C.I.) ya está registrada")
        } else if (errors?.password) {
            toast("La contraseña no cumple los requisitos")
        } else {
            toast("Error al crear la cuenta. Revisa los datos.")
        }
    } finally {
        isLoading.value = false
    }
}

const txtLoginTitle = "Bienvenido de nuevo"
const txtRegisterTitle = "Únete a la élite"
const txtLoginSub = "Ingresa tus credenciales para continuar."
const txtRegisterSub = "Comienza tu experiencia con nosotros hoy."
</script>

<template>
    <div class="min-h-screen bg-[#050505] flex items-center justify-center p-4 relative overflow-hidden font-sans">

        <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-900/20 rounded-full blur-[120px]"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-900/20 rounded-full blur-[120px]">
        </div>

        <div
            class="relative z-10 w-full max-w-lg bg-[#0f0f0f]/80 backdrop-blur-xl rounded-[2rem] shadow-[0_0_50px_-12px_rgba(139,92,246,0.3)] border border-white/10 p-8 md:p-12 transition-all">

            <div class="text-center mb-10">
                <div
                    class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-3xl shadow-[0_0_20px_rgba(139,92,246,0.5)] mb-6 transform rotate-3">
                    <span class="text-4xl text-white">⚡</span>
                </div>
                <h1 class="text-4xl font-black text-white tracking-tight mb-2 uppercase italic">
                    {{ currentView === 'login' ? txtLoginTitle : txtRegisterTitle }}
                </h1>
                <p class="text-gray-400 font-medium">
                    {{ currentView === 'login' ? txtLoginSub : txtRegisterSub }}
                </p>
            </div>

            <form v-if="currentView === 'login'" @submit.prevent="handleLogin" class="space-y-6 animate-fade-in">
                <div class="group">
                    <label class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Email
                        Corporativo</label>
                    <input type="email" v-model="form.login.email" placeholder="usuario@nexus.com" required
                        class="w-full px-5 py-4 bg-white/5 border border-white/10 rounded-2xl text-white outline-none focus:border-purple-500 transition-all placeholder:text-gray-700" />
                </div>

                <div class="relative group">
                    <label
                        class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Contraseña</label>
                    <input :type="showPassword ? 'text' : 'password'" v-model="form.login.password"
                        placeholder="••••••••" required
                        class="w-full px-5 py-4 bg-white/5 border border-white/10 rounded-2xl text-white outline-none focus:border-purple-500 transition-all" />
                    <button type="button" @click="showPassword = !showPassword"
                        class="absolute right-5 top-[42px] text-gray-500 hover:text-purple-400 transition-colors">
                        <span>{{ showPassword ? '🔓' : '👁️' }}</span>
                    </button>
                </div>

                <button type="submit" :disabled="isLoading"
                    class="w-full py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-black rounded-2xl shadow-lg hover:scale-[1.02] transition-all active:scale-95 uppercase tracking-widest disabled:opacity-50">
                    {{ isLoading ? 'Verificando...' : 'Acceder al Terminal' }}
                </button>
            </form>

            <form v-else @submit.prevent="handleRegister" class="grid grid-cols-2 gap-5 animate-fade-in">
                <div class="col-span-1">
                    <label
                        class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Nombre</label>
                    <input type="text" v-model="form.register.nombre" required
                        class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white outline-none focus:border-purple-500" />
                </div>
                <div class="col-span-1">
                    <label
                        class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Apellido</label>
                    <input type="text" v-model="form.register.apellido" required
                        class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white outline-none focus:border-purple-500" />
                </div>
                <div class="col-span-1">
                    <label class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">C.I.
                        Identidad</label>
                    <input type="text" v-model="form.register.ci" required placeholder=""
                        class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white outline-none focus:border-purple-500" />
                </div>
                <div class="col-span-1">
                    <label
                        class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Email</label>
                    <input type="email" v-model="form.register.email" required
                        class="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white outline-none focus:border-purple-500" />
                </div>
                <div class="col-span-2 relative">
                    <label
                        class="block text-xs font-black text-purple-400 uppercase tracking-widest mb-2 ml-1">Establecer
                        Contraseña</label>
                    <input :type="showPassword ? 'text' : 'password'" v-model="form.register.password" required
                        class="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white outline-none focus:border-purple-500" />
                </div>

                <button type="submit" :disabled="isLoading"
                    class="col-span-2 w-full py-4 bg-white text-black font-black rounded-2xl shadow-lg hover:bg-purple-600 hover:text-white transition-all active:scale-95 uppercase tracking-widest disabled:opacity-50">
                    {{ isLoading ? 'Procesando...' : 'Crear Perfil Élite' }}
                </button>
            </form>

            <div class="mt-10 pt-6 border-t border-white/5 text-center">
                <p class="text-gray-500 font-medium">
                    {{ currentView === 'login' ? '¿No tienes cuenta?' : '¿Ya tienes acceso?' }}
                    <button @click="currentView = currentView === 'login' ? 'register' : 'login'"
                        class="ml-2 text-white font-bold hover:text-purple-400 transition-colors underline underline-offset-4 decoration-purple-500">
                        {{ currentView === 'login' ? 'Regístrate' : 'Inicia sesión' }}
                    </button>
                </p>
            </div>
        </div>
    </div>
</template>




<style scoped>
.animate-fade-in {
    animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.95) translateY(10px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* Scrollbar minimalista para el cuerpo si fuera necesario */
::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4b218b;
}

.animate-fade-in {
    animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>