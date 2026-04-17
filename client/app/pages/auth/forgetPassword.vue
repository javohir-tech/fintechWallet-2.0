<script setup lang="ts">
import type { FormError } from '@nuxt/ui';
import { useToast } from '@nuxt/ui/runtime/composables/useToast.js';
import axios from 'axios';
import { authService } from '~/services/auth.services';

definePageMeta({
    layout: "auth",
    middleware: "guest"
})

const state = reactive({
    identifier: '',
})

const toast = useToast()
const loading = ref(false)

type Schema = typeof state

function validate(state: Partial<Schema>): FormError[] {
    const errors: FormError[] = []

    if (!state.identifier) {
        errors.push({ name: 'identifier', message: 'Required' })
    } else {
        const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.identifier)
        const phoneOk = /^\+?[\d\s\-()]{7,15}$/.test(state.identifier)
        if (!emailOk && !phoneOk) {
            errors.push({ name: 'identifier', message: "Email yoki telefon noto'g'ri" })
        }
    }

    return errors
}

const isPhone = computed(() =>
    /^[+\d\s\-()]+$/.test(state.identifier) && state.identifier.length > 0
)

async function onSubmit() {
    loading.value = true
    try {
        const payload = {
            email_or_number: state.identifier,
        }

        const { data } = await authService.forgetPassword(payload)

        const verify_token = useCookie("verify_token")
        verify_token.value = data.token

        toast.add({
            title: "Muvaffaqiyat",
            description: data.message,
            color: "primary"
        })

        await navigateTo({ path: "/auth/verify", query: { identifier: state.identifier , from : "forget" } })
    } catch (err: unknown) {
        let message = "Nimadir xato ketdi"
        if (axios.isAxiosError(err)) {
            message = err?.response?.data?.detail
                ?? err?.response?.data?.non_field_errors?.[0]
                ?? err?.response?.data?.email_or_number?.[0]
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
                <h1>Parolni tiklash</h1>
                <p>Email yoki telefon raqamingizni kiriting</p>
                <p>Tasdiqlash kodi yuboriladi</p>
            </div>

            <!-- Form -->
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

                <UFormField name="identifier" class="field">
                    <UInput v-model="state.identifier"
                        :placeholder="isPhone ? '+998 90 000 00 00' : 'email@example.com'"
                        :leading-icon="isPhone ? 'i-lucide-phone' : 'i-lucide-mail'" size="lg" class="w-full"
                        autocomplete="username" />
                </UFormField>

                <UButton type="submit" block size="lg" :loading="loading" class="submit-btn">
                    Kodni yuborish
                </UButton>

            </UForm>

            <!-- Footer -->
            <p class="footer-link">
                Esladingizmi?
                <NuxtLink to="/auth/login">Kirish</NuxtLink>
            </p>

        </div>
    </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';
</style>