<script setup lang="ts">

import type { FormError } from '@nuxt/ui';
import { authService } from '~/services/auth.services';
definePageMeta({
  layout: "auth",
  middleware: "guest",
})


const state = reactive({
  identifier: '',
})

type Schema = typeof state
const toast = useToast();
const loading = ref(false)

const isPhone = computed(() =>
  /^[+\d\s\-()]+$/.test(state.identifier) && state.identifier.length > 0
)

const validate = (state: Partial<Schema>): FormError[] => {
  const errors = []

  if (!state.identifier) errors.push({ "name": "identifier", "message": "Required" })
  return errors
}

async function onSubmit() {
  loading.value = true
  try {
    const { data } = await authService.register({
      email_or_number: state.identifier
    })

    const verify_token = useCookie("verify_token")
    verify_token.value = data.verify_token
    toast.add({
      title: "Muvaffaqiyat",
      description: "Sizning manzilingizga tastiqlsh kodini yubordik", 
      color : "primary"
    })
    await navigateTo("/auth/verify")
  } catch (error: any) {
    console.log(error.response)
    const message = error.response?.data?.non_field_errors[0]
    toast.add({
      title: "Xatolik",
      description: message, 
      color : "error"
    })
  }
  finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="container">

      <div class="heading">
        <h1>Ro'yxatdan o'tish</h1>
        <p>Email yoki telefon raqamingizni kiriting</p>
      </div>

      <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

        <UFormField name="identifier">
          <UInput v-model="state.identifier" :placeholder="isPhone ? '+998 90 000 00 00' : 'email@example.com'"
            :leading-icon="isPhone ? 'i-lucide-phone' : 'i-lucide-mail'" size="lg" class="field"
            autocomplete="username" />
        </UFormField>

        <p class="hint">
          {{ isPhone
            ? 'Telefon raqamingizga tasdiqlash kodi yuboriladi'
            : 'Emailingizga tasdiqlash kodi yuboriladi'
          }}
        </p>

        <UButton type="submit" block size="lg" :loading="loading" class="submit-btn">
          Kod yuborish
        </UButton>

      </UForm>

      <p class="footer-link">
        Akkaunt bor?
        <NuxtLink to="/auth/login">Kirish</NuxtLink>
      </p>

    </div>
  </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';
</style>