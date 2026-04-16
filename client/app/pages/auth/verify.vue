<script setup lang="ts">
definePageMeta({
  layout: false,
})

const route = useRoute()

// Register sahifasidan kelgan identifier
const identifier = computed(() => route.query.identifier as string || '')

const isPhone = computed(() =>
  /^[+\d\s\-()]+$/.test(identifier.value)
)

// OTP — 6 ta raqam, har biri alohida input
const digits = reactive(['', '', '', '', '', ''])
const inputRefs = ref<HTMLInputElement[]>([])

const code = computed(() => digits.join(''))

const loading = ref(false)
const resendCooldown = ref(0)
let cooldownTimer: ReturnType<typeof setInterval> | null = null

// ─── Resend countdown ─────────────────────────────────────────────────────────

function startCooldown() {
  resendCooldown.value = 60
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

// ─── OTP input handlers ───────────────────────────────────────────────────────

function onInput(index: number, event: Event) {
  const val = (event.target as HTMLInputElement).value.replace(/\D/g, '')
  digits[index] = val.slice(-1)

  if (val && index < 5) {
    nextTick(() => inputRefs.value[index + 1]?.focus())
  }

  if (code.value.length === 6) {
    onSubmit()
  }
}

function onKeydown(index: number, event: KeyboardEvent) {
  if (event.key === 'Backspace' && !digits[index] && index > 0) {
    digits[index - 1] = ''
    nextTick(() => inputRefs.value[index - 1]?.focus())
  }
}

function onPaste(event: ClipboardEvent) {
  event.preventDefault()
  const pasted = event.clipboardData?.getData('text').replace(/\D/g, '').slice(0, 6) || ''
  pasted.split('').forEach((char, i) => {
    if (i < 6) digits[i] = char
  })
  nextTick(() => {
    const next = Math.min(pasted.length, 5)
    inputRefs.value[next]?.focus()
    if (pasted.length === 6) onSubmit()
  })
}

// ─── Submit ───────────────────────────────────────────────────────────────────

async function onSubmit() {
  if (code.value.length < 6) return
  loading.value = true
  try {
    // TODO: Kodni backendga yuborish
    // await useFetch('/api/auth/verify-code', {
    //   method: 'POST',
    //   body: {
    //     identifier: identifier.value,
    //     code: code.value,
    //   },
    // })

    console.log('Verify:', { identifier: identifier.value, code: code.value })

    // TODO: Muvaffaqiyatli bo'lganda qayerga yo'naltirish kerakligini belgilang
    // await navigateTo('/dashboard')
  } finally {
    loading.value = false
  }
}

// ─── Resend ───────────────────────────────────────────────────────────────────

async function resend() {
  if (resendCooldown.value > 0) return

  // TODO: Qayta kod yuborish
  // await useFetch('/api/auth/send-code', {
  //   method: 'POST',
  //   body: { identifier: identifier.value },
  // })

  digits.fill('')
  nextTick(() => inputRefs.value[0]?.focus())
  startCooldown()
}
</script>

<template>
  <div class="page">
    <div class="container">

      <div class="logo">
        <span class="logo-dot" />
      </div>

      <div class="heading">
        <h1>Tasdiqlash</h1>
        <p>
          {{ isPhone ? 'Telefon raqamiga' : 'Emailga' }} yuborilgan
          6 xonali kodni kiriting
        </p>
        <span class="identifier">{{ identifier }}</span>
      </div>

      <!-- OTP inputs -->
      <div class="otp-wrapper" @paste="onPaste">
        <input
          v-for="(digit, i) in digits"
          :key="i"
          :ref="(el) => { if (el) inputRefs[i] = el as HTMLInputElement }"
          :value="digit"
          type="text"
          inputmode="numeric"
          maxlength="1"
          class="otp-input"
          :class="{ filled: digit, loading: loading }"
          :disabled="loading"
          @input="onInput(i, $event)"
          @keydown="onKeydown(i, $event)"
        />
      </div>

      <!-- Submit -->
      <UButton
        block
        size="lg"
        :loading="loading"
        :disabled="code.length < 6 || loading"
        class="submit-btn"
        @click="onSubmit"
      >
        Tasdiqlash
      </UButton>

      <!-- Resend -->
      <div class="resend">
        <button
          type="button"
          :disabled="resendCooldown > 0"
          class="resend-btn"
          :class="{ disabled: resendCooldown > 0 }"
          @click="resend"
        >
          {{ resendCooldown > 0 ? `Qayta yuborish (${resendCooldown}s)` : 'Qayta yuborish' }}
        </button>
      </div>

      <!-- Back -->
      <p class="back-link">
        <NuxtLink to="/register">← Orqaga</NuxtLink>
      </p>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  font-family: 'DM Sans', sans-serif;
}
.dark .page { background: #0a0a0a; }

.container {
  width: 100%;
  max-width: 360px;
  padding: 0 24px;
}

.logo { margin-bottom: 40px; }
.logo-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #111;
}
.dark .logo-dot { background: #fff; }

.heading { margin-bottom: 36px; }
.heading h1 {
  font-size: 22px;
  font-weight: 500;
  color: #111;
  letter-spacing: -0.5px;
  margin: 0 0 6px;
}
.dark .heading h1 { color: #f5f5f5; }
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
.dark .identifier { color: #aaa; }

/* OTP */
.otp-wrapper {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.otp-input {
  flex: 1;
  height: 52px;
  text-align: center;
  font-size: 20px;
  font-weight: 500;
  font-family: 'DM Sans', sans-serif;
  color: #111;
  background: #fff;
  border: 1.5px solid #e5e5e5;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.2s;
  -moz-appearance: textfield;
}
.otp-input::-webkit-outer-spin-button,
.otp-input::-webkit-inner-spin-button { -webkit-appearance: none; }

.otp-input:focus {
  border-color: #111;
}
.otp-input.filled {
  border-color: #111;
}
.otp-input.loading {
  opacity: 0.5;
  cursor: not-allowed;
}

.dark .otp-input {
  background: #111;
  border-color: #2a2a2a;
  color: #f5f5f5;
}
.dark .otp-input:focus,
.dark .otp-input.filled {
  border-color: #fff;
}

/* Submit */
.submit-btn { margin-bottom: 16px; }

/* Resend */
.resend { text-align: center; margin-bottom: 24px; }
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
.resend-btn:hover { opacity: 0.6; }
.resend-btn.disabled {
  color: #bbb;
  cursor: default;
}
.resend-btn.disabled:hover { opacity: 1; }
.dark .resend-btn { color: #f5f5f5; }
.dark .resend-btn.disabled { color: #444; }

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
.back-link a:hover { color: #111; }
.dark .back-link a:hover { color: #fff; }
</style>