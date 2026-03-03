import { createRouter, createWebHistory } from 'vue-router'

// Importación de Vistas y Componentes
import Login from '../views/Login.vue'
import CalculoII from '../views/CalculoII.vue'
import CalculoX from '../views/CalculoX.vue'
import VitaminaX from '../views/VitaminaX.vue'
import Costo from '../views/Costo.vue'
import GestionUsuarios from '../views/GestionUsuarios.vue'
import AdquirirPlan from '../views/AdquirirPlan.vue'
import GestionPagos from '../views/GestionPagos.vue'

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },

    // RUTAS DE HERRAMIENTAS (Requieren Login y Acceso Activo)
    { path: '/CalculoII', name: 'CalculoII', component: CalculoII, meta: { requiresAuth: true, requiresAccess: true } },
    { path: '/CalculoX', name: 'CalculoX', component: CalculoX, meta: { requiresAuth: true, requiresAccess: true } },
    { path: '/VitaminaX', name: 'VitaminaX', component: VitaminaX, meta: { requiresAuth: true, requiresAccess: true } },
    { path: '/Costo', name: 'Costo', component: Costo, meta: { requiresAuth: true, requiresAccess: true } },

    // RUTAS ADMINISTRATIVAS (Solo para ADMIN)
    { path: '/Usuarios', name: 'GestionUsuarios', component: GestionUsuarios, meta: { requiresAuth: true, isAdmin: true } },
    { path: '/pagos', name: 'GestionPagos', component: GestionPagos, meta: { requiresAuth: true, isAdmin: true } },

    // RUTA DE PAGO (Solo requiere estar logueado)
    { path: '/plan', name: 'AdquirirPlan', component: AdquirirPlan, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// --- GUARDIA DE NAVEGACIÓN - LÓGICA DEFINITIVA ---
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')
    const userRaw = localStorage.getItem('user_data')
    const userData = userRaw ? JSON.parse(userRaw) : null

    // 1. Si la ruta requiere autenticación y no hay token: AL LOGIN
    if (to.meta.requiresAuth && !token) {
        return next({ name: 'Login' })
    }

    // 2. Si es ADMIN y va a login o cualquier lado, va a GestionUsuarios
    if (userData?.rol === 'ADMIN') {
        if (to.path === '/login' || to.path === '/') {
            return next({ name: 'GestionUsuarios' })
        }
        // Si es admin, puede ir a cualquier ruta admin
        return next()
    }

    // 3. A PARTIR DE AQUÍ SON USUARIOS NORMALES
    // Si intenta ir a rutas de admin, lo mandamos a donde corresponda
    if (to.meta.isAdmin) {
        return next({ name: 'CalculoII' }) // O a plan si está vencido? Lo manejamos después
    }

    // 4. LÓGICA PRINCIPAL PARA USUARIOS NORMALES
    if (userData) {
        // 4.1 Si el usuario NO TIENE ACCESO (plan vencido)
        if (!userData.tiene_acceso) {
            // Solo puede ir a login o plan
            if (to.path === '/login' || to.name === 'AdquirirPlan') {
                return next() // Permite ir a login o plan
            }
            // Cualquier otra ruta lo mandamos a plan
            return next({ name: 'AdquirirPlan' })
        }

        // 4.2 Si el usuario TIENE ACCESO (plan activo)
        else {
            // Si intenta ir a login, lo mandamos a CalculoII
            if (to.path === '/login') {
                return next({ name: 'CalculoII' })
            }
            // Si intenta ir a plan (estando activo), lo mandamos a CalculoII
            if (to.name === 'AdquirirPlan') {
                return next({ name: 'CalculoII' })
            }
            // Para cualquier otra ruta, permitir si requiere acceso
            if (to.meta.requiresAccess) {
                return next() // Tiene acceso, puede pasar
            }
            // Si no requiere acceso específico, también puede pasar
            return next()
        }
    }

    // 5. Si no hay userData pero hay token (caso raro), logout
    if (token && !userData) {
        localStorage.clear()
        return next({ name: 'Login' })
    }

    next()
})

export default router