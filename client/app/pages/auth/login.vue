<script setup lang="ts">
import type { FormError } from '@nuxt/ui';
import { useToast } from '@nuxt/ui/runtime/composables/useToast.js';

definePageMeta({
    layout: "auth",
    middleware: "guest"
})


const state = reactive({
    identifier: '',
    password: '',
})

const { loading, login } = useAuth()
const toast = useToast();
const showPassword = ref(false)
const message = useRoute().query.message

type Schema = typeof state


function validate(state: Partial<Schema>): FormError[] {
    const errors = []
    if (!state.identifier) {
        errors.push({ name: "identifier", message: "Required" })
    } else {
        const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.identifier)
        const phoneOk = /^\+?[\d\s\-()]{7,15}$/.test(state.identifier)
        if (!emailOk && !phoneOk) {
            errors.push({ "name": "identifier", "message": "Email yoki telefon noto'g'ri" })
        }
    }
    if (!state.password) {
        errors.push({ name: "password", message: "Required" })
    } else if (state.password.length < 8) {
        errors.push({ "name": "password", "message": "Kamida 8ta belgidan iborat  bo'lishi  kerak" })
    }
    return errors
}


const isPhone = computed(() =>
    /^[+\d\s\-()]+$/.test(state.identifier) && state.identifier.length > 0
)


async function onSubmit() {
    const result = await login(
        state.identifier,
        state.password
    )

    toast.add({
        title: result.success ? "Muvaffaqiyat" : "Xatolik",
        description: result.message,
        color: result.success ? "primary" : "error"
    })

    if (result.success) {
        await navigateTo("/")
    }
}

onMounted(() => {
    if (message && typeof message === "string") {
        toast.add({
            title: "Muvaffaqiyatli",
            description: message,
            color: "primary"
        })
    }
})


</script>

<template>
    <div class="page">
        <div class="container">
            <!-- Heading -->
            <div class="heading">
                <h1>Kirish</h1>
                <p>Akkauntingizga xush kelibsiz</p>
                <p>Email yoki telefon raqamingizni kiriting</p>
            </div>

            <!-- Form -->
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

                <UFormField name="identifier" class="field">
                    <UInput v-model="state.identifier"
                        :placeholder="isPhone ? '+998 90 000 00 00' : 'email@example.com'"
                        :leading-icon="isPhone ? 'i-lucide-phone' : 'i-lucide-mail'" size="lg" class="w-full"
                        autocomplete="username" />
                </UFormField>

                <UFormField name="password" class="field">
                    <UInput v-model="state.password" :type="showPassword ? 'text' : 'password'" placeholder="Parol"
                        leading-icon="i-lucide-lock" size="lg" class="w-full" autocomplete="current-password">
                        <template #trailing>
                            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                                <UIcon :name="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'" />
                            </button>
                        </template>
                    </UInput>
                </UFormField>

                <div class="forgot">
                    <NuxtLink to="/auth/forgetpassword">Parolni unutdingizmi?</NuxtLink>
                </div>

                <UButton type="submit" block size="lg" :loading="loading" class="submit-btn">
                    Kirish
                </UButton>

            </UForm>

            <!-- Footer -->
            <p class="footer-link">
                Akkaunt yo'qmi?
                <NuxtLink to="/auth/signup">Ro'yxatdan o'ting</NuxtLink>
            </p>

        </div>
    </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';
</style>