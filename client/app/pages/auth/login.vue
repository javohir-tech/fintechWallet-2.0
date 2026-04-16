<script setup lang="ts">
import type { FormError } from '@nuxt/ui';

definePageMeta({
    layout: "auth",
})

const state = reactive({
    identifier: '',
    password: '',
})

const { loading, login } = useAuth()
const toast = useToast();

const showPassword = ref(false)
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
    const result = await login("http://localhost:8000/auth/login/",
        state.identifier,
        state.password
    )

    console.log(result)

    toast.add({
        title: result.success ? "Muvaffaqiyat" : "Xatolik",
        description: result.message,
        color: result.success ? "primary" : "error"
    })

    if (result.success) {
        await navigateTo("/")
    }
}
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
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit" @error="console.log">

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
                    <!-- <NuxtLink to="/forgot-password">Parolni unutdingizmi?</NuxtLink> -->
                </div>

                <UButton type="submit" block size="lg" :loading="loading" class="submit-btn">
                    Kirish
                </UButton>

            </UForm>

            <!-- Footer -->
            <p class="register-link">
                Akkaunt yo'qmi?
                <NuxtLink to="/auth/signup">Ro'yxatdan o'ting</NuxtLink>
            </p>

        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

* {
    box-sizing: border-box;
}

.page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'DM Sans', sans-serif;
}

.container {
    width: 100%;
    max-width: 360px;
    padding: 0 24px;
}

/* Heading */
.heading {
    margin-bottom: 36px;
}

.heading h1 {
    font-size: 22px;
    font-weight: 500;
    color: #111;
    letter-spacing: -0.5px;
    margin: 0 0 6px;
}

.dark .heading h1 {
    color: #f5f5f5;
}

.heading p {
    font-size: 13px;
    color: #999;
    margin: 0;
    font-weight: 300;
}

/* Form */
.form {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.form :deep([data-slot="error"]) {
    display: block !important;
}

.field {
    width: 100%;
}

.error-msg {
    font-size: 12px;
    color: #f87171;
    margin: 4px 0 0 2px;
}

/* Eye button */
.eye-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #aaa;
    display: flex;
    align-items: center;
    padding: 0 2px;
    transition: color 0.2s;
}

.eye-btn:hover {
    color: #555;
}

/* Forgot */
.forgot {
    text-align: right;
    margin-top: -4px;
}

.forgot a {
    font-size: 12px;
    color: #aaa;
    text-decoration: none;
    transition: color 0.2s;
}

.forgot a:hover {
    color: #111;
}

.dark .forgot a:hover {
    color: #fff;
}

/* Submit */
.submit-btn {
    margin-top: 8px;
}

/* Register */
.register-link {
    text-align: center;
    font-size: 13px;
    color: #aaa;
    margin-top: 28px;
    font-weight: 300;
}

.register-link a {
    color: #111;
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.2s;
}

.register-link a:hover {
    opacity: 0.6;
}

.dark .register-link a {
    color: #f5f5f5;
}
</style>