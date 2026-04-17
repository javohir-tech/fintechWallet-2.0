<script setup lang="ts">
import type { FormError } from '@nuxt/ui';
import { useToast } from '@nuxt/ui/runtime/composables/useToast.js';
import axios from 'axios';
import { authService } from '~/services/auth.services';

definePageMeta({
    layout: "auth",
    middleware: "guest"
})

const PASSWORD_REGEX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/

const state = reactive({
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
            password: state.password,
        }

        const {data} = await authService.passwordReset(payload)

        toast.add({
            title: "Muvaffaqiyat",
            description: data.message,
            color: "primary"
        })

        await navigateTo("/auth/login")
    } catch (err: unknown) {
        let message = "Nimadir xato ketdi"
        if (axios.isAxiosError(err)) {
            message = err?.response?.data?.detail
                ?? err?.response?.data?.password?.[0]
                ?? "Nimadir xato ketdi"
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
                <h1>Yangi parol</h1>
                <p>Yangi parolingizni kiriting</p>
            </div>

            <!-- Form -->
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

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
                <NuxtLink to="/auth/login">Kirish</NuxtLink>
            </p>

        </div>
    </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';
</style>