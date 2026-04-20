<script setup lang="ts">
import type { FormError } from '@nuxt/ui';
import { useToast } from '@nuxt/ui/runtime/composables/useToast.js';
import axios from 'axios';
import { authService } from '~/services/auth.services';
import { useUserStore } from '~/store/useUser';
import { normalizeUser } from '~/utils/mappers/user.mapper';

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

const userStore = useUserStore()

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

        const { data } = await authService.updateUser(payload)
        // console.log(data)
        const access_token = useCookie("access_token")
        const refresh_token = useCookie("refresh_token")
        const verifyToken = useCookie("verify_token")
        const update_token = useCookie("update_token");

        const user = normalizeUser(data.user)

        userStore.setUser(user)

        update_token.value = null
        verifyToken.value = null
        access_token.value = data.tokens.access_token
        refresh_token.value = data.tokens.refresh_token

        toast.add({
            title: "Muvaffaqiyat",
            description: data.message,
            color: "primary"
        })

        await navigateTo("/")
    } catch (err: unknown) {
        let message = "Nimadir xato ketdi"
        if (axios.isAxiosError(err)) {
            message = err?.response?.data?.detail
                ?? err?.response?.data?.username?.[0]
                ?? err?.response?.data?.password?.[0]
        }
        toast.add({
            title: "Xatolik",
            description: message,
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
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

                <!-- Username -->
                <UFormField name="username" class="field">
                    <UInput v-model="state.username" placeholder="foydalanuvchi_nomi" leading-icon="i-lucide-user"
                        size="lg" class="w-full" autocomplete="username" />
                </UFormField>

                <!-- Password -->
                <UFormField name="password" class="field">
                    <UInput v-model="state.password" :type="showPassword ? 'text' : 'password'"
                        placeholder="Yangi parol" leading-icon="i-lucide-lock" size="lg" class="w-full"
                        autocomplete="new-password">
                        <template #trailing>
                            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                                <UIcon :name="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'" />
                            </button>
                        </template>
                    </UInput>
                </UFormField>

                <!-- Confirm Password -->
                <UFormField name="confirmPassword" class="field">
                    <UInput v-model="state.confirmPassword" :type="showConfirm ? 'text' : 'password'"
                        placeholder="Parolni tasdiqlang" leading-icon="i-lucide-lock-keyhole" size="lg" class="w-full"
                        autocomplete="new-password">
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