<script setup lang="ts">
import type { FormError } from '@nuxt/ui';
import { useToast } from '@nuxt/ui/runtime/composables/useToast.js';

definePageMeta({
    layout: "auth",
    middleware: "updateuser"
})

const PASSWORD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

const state = reactive({
    username: '',
    password: '',
    confirmPassword: '',
})

const toast = useToast()
const loading = ref(false)

const showPassword = ref(false)
const showConfirm = ref(false)

type Schema = typeof state

function validate(state: Partial<Schema>): FormError[] {
    const errors: FormError[] = []

    if (!state.username) {
        errors.push({ name: 'username', message: 'Required' })
    } else if (state.username.length < 3) {
        errors.push({ name: 'username', message: "Kamida 3ta belgidan iborat bo'lishi kerak" })
    } else if (!/^[a-zA-Z0-9_]+$/.test(state.username)) {
        errors.push({ name: 'username', message: "Faqat harf, raqam va _ ishlatish mumkin" })
    }

    if (!state.password) {
        errors.push({ name: 'password', message: 'Required' })
    } else if (!PASSWORD_REGEX.test(state.password)) {
        errors.push({
            name: 'password',
            message: "Kamida 8 belgi: katta/kichik harf, raqam va maxsus belgi (@$!%*?&)"
        })
    }

    if (!state.confirmPassword) {
        errors.push({ name: 'confirmPassword', message: 'Required' })
    } else if (state.password !== state.confirmPassword) {
        errors.push({ name: 'confirmPassword', message: "Parollar mos kelmadi" })
    }

    return errors
}

async function onSubmit() {
    loading.value = true
    try {
        const payload = {
            username: state.username,
            password: state.password,
        }

        // TODO: API chaqiruvi shu yerda bo'ladi
        // const result = await updateUser(payload.username, payload.password)

        console.log('Payload:', payload)

        toast.add({
            title: "Muvaffaqiyat",
            description: "Ma'lumotlar yangilandi",
            color: "primary"
        })

        await navigateTo("/")
    } catch (err) {
        toast.add({
            title: "Xatolik",
            description: "Nimadir xato ketdi",
            color: "error"
        })
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="page">
        <div class="container">

            <!-- Heading -->
            <div class="heading">
                <h1>Ma'lumotlarni yangilash</h1>
                <p>Foydalanuvchi nomi va yangi parol kiriting</p>
            </div>

            <!-- Form -->
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit" @error="console.log">

                <!-- Username -->
                <UFormField name="username" class="field">
                    <UInput
                        v-model="state.username"
                        placeholder="foydalanuvchi_nomi"
                        leading-icon="i-lucide-user"
                        size="lg"
                        class="w-full"
                        autocomplete="username"
                    />
                </UFormField>

                <!-- Password -->
                <UFormField name="password" class="field">
                    <UInput
                        v-model="state.password"
                        :type="showPassword ? 'text' : 'password'"
                        placeholder="Yangi parol"
                        leading-icon="i-lucide-lock"
                        size="lg"
                        class="w-full"
                        autocomplete="new-password"
                    >
                        <template #trailing>
                            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                                <UIcon :name="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'" />
                            </button>
                        </template>
                    </UInput>
                </UFormField>

                <!-- Confirm Password -->
                <UFormField name="confirmPassword" class="field">
                    <UInput
                        v-model="state.confirmPassword"
                        :type="showConfirm ? 'text' : 'password'"
                        placeholder="Parolni tasdiqlang"
                        leading-icon="i-lucide-lock-keyhole"
                        size="lg"
                        class="w-full"
                        autocomplete="new-password"
                    >
                        <template #trailing>
                            <button type="button" class="eye-btn" @click="showConfirm = !showConfirm">
                                <UIcon :name="showConfirm ? 'i-lucide-eye-off' : 'i-lucide-eye'" />
                            </button>
                        </template>
                    </UInput>
                </UFormField>

                <UButton type="submit" block size="lg" :loading="loading" class="submit-btn">
                    Saqlash
                </UButton>

            </UForm>

            <!-- Footer -->
            <p class="footer-link">
                Ortga qaytish?
                <NuxtLink to="/auth/login">Kirish sahifasi</NuxtLink>
            </p>

        </div>
    </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';
</style>