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

      <p class="login-link">
        Akkaunt bor?
        <NuxtLink to="/auth/login">Kirish</NuxtLink>
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
  /* background: #fafafa; */
  font-family: 'DM Sans', sans-serif;
}

/* .dark .page { background: #0a0a0a; } */

.container {
  width: 100%;
  max-width: 360px;
  padding: 0 24px;
}

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

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field {
  width: 100%;
}

.hint {
  font-size: 12px;
  color: #bbb;
  margin: 0;
  font-weight: 300;
  line-height: 1.5;
}

.submit-btn {
  margin-top: 8px;
}

.login-link {
  text-align: center;
  font-size: 13px;
  color: #aaa;
  margin-top: 28px;
  font-weight: 300;
}

.login-link a {
  color: #111;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.login-link a:hover {
  opacity: 0.6;
}

.dark .login-link a {
  color: #f5f5f5;
}
</style>