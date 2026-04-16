<script setup lang="ts">
definePageMeta({
    layout: "auth",
})

const state = reactive({
    identifier: '',
    password: '',
})

const { loading, login } = useAuth()
const router = useRouter()
const toast = useToast();

const showPassword = ref(false)
// const loading = ref(false)

const isPhone = computed(() =>
    /^[+\d\s\-()]+$/.test(state.identifier) && state.identifier.length > 0
)

const validate = (data: typeof state) => {
    const errors: { path: string; message: string }[] = []

    if (!data.identifier) {
        errors.push({ path: 'identifier', message: 'Majburiy maydon' })
    } else {
        const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.identifier)
        const phoneOk = /^\+?[\d\s\-()]{7,15}$/.test(data.identifier)
        if (!emailOk && !phoneOk)
            errors.push({ path: 'identifier', message: "Email yoki telefon noto'g'ri" })
    }

    if (!data.password)
        errors.push({ path: 'password', message: 'Majburiy maydon' })
    else if (data.password.length < 6)
        errors.push({ path: 'password', message: 'Kamida 6 ta belgi' })

    return errors
}

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

    if(result.success){
       navigateTo("/")
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
            <UForm :validate="validate" :state="state" class="form" @submit="onSubmit">

                <UFormField name="identifier">
                    <UInput v-model="state.identifier"
                        :placeholder="isPhone ? '+998 90 000 00 00' : 'email@example.com'"
                        :leading-icon="isPhone ? 'i-lucide-phone' : 'i-lucide-mail'" size="lg" class="field"
                        autocomplete="username" />
                </UFormField>

                <UFormField name="password">
                    <UInput v-model="state.password" :type="showPassword ? 'text' : 'password'" placeholder="Parol"
                        leading-icon="i-lucide-lock" size="lg" class="field" autocomplete="current-password">
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

.field {
    width: 100%;
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