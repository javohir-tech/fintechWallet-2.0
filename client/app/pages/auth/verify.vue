<script setup lang="ts">
import axios from 'axios'
import { authService } from '~/services/auth.services'

definePageMeta({
  layout: "auth",
  middleware: "verify"
})

const route = useRoute()

// Register sahifasidan kelgan identifier
const identifier = computed(() => route.query.identifier as string || '')
const from = route.query.from as  "forget" | "signup"

const isPhone = computed(() =>
  /^[+\d\s\-()]+$/.test(identifier.value)
)

// OTP — 6 ta raqam, har biri alohida input
const digits = ref(['', '', '', ''])
const inputRefs = ref<HTMLInputElement[]>([])
const toast = useToast()

const code = computed(() => digits.value.join(''))

const loading = ref(false)
const resendCooldown = ref(0)
let cooldownTimer: ReturnType<typeof setInterval> | null = null

// ─── Resend countdown ─────────────────────────────────────────────────────────

function startCooldown() {
  resendCooldown.value = 120
  cooldownTimer = setInterval(() => {
    resendCooldown.value--
    if (resendCooldown.value <= 0 && cooldownTimer) {
      clearInterval(cooldownTimer)
      cooldownTimer = null
    }
  }, 1000)
}

onMounted(() => {
  startCooldown()
  nextTick(() => inputRefs.value[0]?.focus())
})

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})


// ─── Submit ───────────────────────────────────────────────────────────────────

async function onSubmit() {
  if (code.value.length < 4) return
  loading.value = true
  try {

    const { data } = await authService.verify({ code: code.value })
    console.log(data)
    const update_token = useCookie("update_token")

    update_token.value = data.data.update_token

    toast.add({
      title: "Muvaffaqiyatli",
      description: data.message,
      color: "primary"
    })
    if(from === "signup"){
      await navigateTo("/auth/updateuser/")
    }else if(from === 'forget'){
      await navigateTo("/auth/resetpassword/")
    }
  } catch (error: unknown) {

    let message = "Xatolik yuz berdi"
    if (axios.isAxiosError(error)) {
      message = error?.response?.data[0]
        || error?.response?.data?.detail
        || "Xatolik yuz berdi"
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

// ─── Resend ───────────────────────────────────────────────────────────────────

async function resend() {
  if (resendCooldown.value > 0) return
  try {
    const { data } = await authService.updateVerify()
    // console.log(data)
    toast.add({
      title: "Muvaffaqiyatli",
      description: data.message,
      color: "primary"
    })
  } catch (error: unknown) {
    let message = "xatolik yuz berdi"
    if (axios.isAxiosError(error)) {
      message = error?.response?.data[0]
      || error?.response?.data?.detail
    }
    toast.add({
      title: "Xatolik",
      description: message,
      color: "error"
    })
  }

  digits.value.fill('')
  nextTick(() => inputRefs.value[0]?.focus())
  startCooldown()
}
</script>

<template>
  <div class="page">
    <div class="container">
      <div class="heading">
        <h1>Tasdiqlash</h1>
        <p>
          {{ isPhone ? 'Telefon raqamiga' : 'Emailga' }} yuborilgan
          4 xonali kodni kiriting
        </p>
        <span class="identifier">{{ identifier }}</span>
      </div>

      <!-- OTP inputs -->
      <div class="otp-wrapper">
        <UPinInput name="inputRefs" v-model="digits" class="otp_input" length="4" size="xl" />
      </div>

      <!-- Submit -->
      <UButton block size="lg" :loading="loading" :disabled="code.length < 4 || loading" class="submit-btn"
        @click="onSubmit">
        Tasdiqlash
      </UButton>

      <!-- Resend -->
      <div class="resend">
        <button type="button" :disabled="resendCooldown > 0" class="resend-btn"
          :class="{ disabled: resendCooldown > 0 }" @click="resend">
          {{ resendCooldown > 0 ? `Qayta yuborish (${resendCooldown}s)` : 'Qayta yuborish' }}
        </button>
      </div>

      <!-- Back -->
      <p class="back-link">
        <NuxtLink to="/auth/signup">← Orqaga</NuxtLink>
      </p>

    </div>
  </div>
</template>

<style scoped>
@import '@/assets/css/auth.css';

.dark .heading h1 {
  color: #f5f5f5;
}

.heading p {
  font-size: 13px;
  color: #999;
  margin: 0 0 4px;
  font-weight: 300;
}

.identifier {
  font-size: 13px;
  color: #555;
  font-weight: 500;
}

.dark .identifier {
  color: #aaa;
}

/* OTP */
.otp-wrapper {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.otp_input {
  width: 100%;
  justify-content: space-evenly;
}

/* Resend */
.resend {
  text-align: center;
  margin-bottom: 24px;
}

.resend-btn {
  background: none;
  border: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #111;
  cursor: pointer;
  font-weight: 500;
  padding: 0;
  transition: opacity 0.2s;
}

.resend-btn:hover {
  opacity: 0.6;
}

.resend-btn.disabled {
  color: #bbb;
  cursor: default;
}

.resend-btn.disabled:hover {
  opacity: 1;
}

.dark .resend-btn {
  color: #f5f5f5;
}

.dark .resend-btn.disabled {
  color: #444;
}

/* Back */
.back-link {
  text-align: center;
  font-size: 13px;
  margin: 0;
}

.back-link a {
  color: #aaa;
  text-decoration: none;
  font-weight: 300;
  transition: color 0.2s;
}

.back-link a:hover {
  color: #111;
}

.dark .back-link a:hover {
  color: #fff;
}
</style>