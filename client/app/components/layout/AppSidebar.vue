<script setup lang="ts">
import type { DropdownMenuItem, NavigationMenuItem, SidebarProps } from '@nuxt/ui'
import { useUserStore } from '~/store/useUser'
import { useSettingsStore } from '~/store/useSettings'

const open = ref(true)

const colorMode = useColorMode()
const userStore = useUserStore()
const settingsStore = useSettingsStore()
const { t, locale } = useI18n()
const {loading , logout} =  useAuth()

const sidebarSide = useCookie<'left' | 'right'>('sidebar_side', { default: () => 'left' })

const navItems = computed<NavigationMenuItem[]>(() => {
    void locale.value // locale o'zgarganda computed qayta hisoblansin
    return [
        { label: t('nav.dashboard'),    icon: 'i-lucide-inbox',           to: '/' },
        { label: t('nav.transfer'),     icon: 'i-lucide-credit-card',     to: '/transfer' },
        { label: t('nav.transactions'), icon: 'i-lucide-square-activity', to: '/transactions' },
        { label: t('nav.settings'),     icon: 'i-lucide-settings',        to: '/settings' },
    ]
})

const user = computed(() => ({
    name: userStore.user?.username ?? 'Foydalanuvchi',
    avatar: userStore.user?.avatar
        ? { src: userStore.user.avatar, alt: userStore.user.username }
        : undefined,
    label: userStore.user?.username ?? 'Foydalanuvchi',
}))

const userItems = computed<DropdownMenuItem[][]>(() => [
    [
        {
            label: 'Profile',
            icon: 'i-lucide-user',
            to: '/profile'
        },
        {
            label: 'Settings',
            icon: 'i-lucide-settings',
            to: '/settings'
        }
    ],
    [
        {
            label: 'Appearance',
            icon: 'i-lucide-sun-moon',
            children: [
                {
                    label: 'Light',
                    icon: 'i-lucide-sun',
                    type: 'checkbox',
                    checked: colorMode.value === 'light',
                    onUpdateChecked(checked: boolean) {
                        if (checked) {
                            colorMode.preference = 'light'
                        }
                    },
                    onSelect(e: Event) {
                        e.preventDefault()
                    }
                },
                {
                    label: 'Dark',
                    icon: 'i-lucide-moon',
                    type: 'checkbox',
                    checked: colorMode.value === 'dark',
                    onUpdateChecked(checked: boolean) {
                        if (checked) {
                            colorMode.preference = 'dark'
                        }
                    },
                    onSelect(e: Event) {
                        e.preventDefault()
                    }
                }
            ]
        }
    ],
    [
        {
            label: 'GitHub',
            icon: 'i-simple-icons-github',
            to: 'https://github.com/javohir-tech/fintechWallet-2.0',
            target: '_blank'
        },
        {
            label: 'Log out',
            icon: 'i-lucide-log-out', 
            onSelect(){
                logout()
            }
        }
    ]
])

defineProps<Pick<SidebarProps, 'variant' | 'collapsible'>>()

</script>

<template>
    <div class="flex h-screen overflow-hidden" :class="sidebarSide === 'right' ? 'flex-row-reverse' : 'flex-row'">
        <USidebar v-model:open="open" :side="sidebarSide" collapsible="icon" rail :ui="{
            container: 'h-full',
            inner: 'bg-elevated/25 divide-transparent',
            body: 'py-0'
        }">
            <template #header>
                <NuxtLink to="/" class="header">
                    <img src="https://github.com/nuxt.png" alt="logo image">
                    <h2 class="text-(--ui-primary)">
                        Fintech Wallet
                    </h2>
                </NuxtLink>
            </template>

            <template #default="{ state }">
                <UNavigationMenu :key="state" :items="navItems" orientation="vertical"
                    :ui="{ link: 'p-1.5 overflow-hidden' }" />
            </template>

            <template #footer>
                <UDropdownMenu :items="userItems" :content="{ align: 'center', collisionPadding: 12 }"
                    :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width) min-w-48' }">
                    <button
                        class="w-full flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-elevated transition-colors overflow-hidden"
                    >
                        <!-- Avatar yoki initials -->
                        <img
                            v-if="userStore.user?.avatar"
                            :src="userStore.user.avatar"
                            :alt="userStore.user.username"
                            class="w-8 h-8 rounded-full object-cover shrink-0"
                        />
                        <div
                            v-else
                            class="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900
                                   flex items-center justify-center text-primary-600 font-bold text-sm shrink-0"
                        >
                            {{ userStore.user?.username?.charAt(0).toUpperCase() ?? '?' }}
                        </div>

                        <!-- Ism -->
                        <span class="flex-1 text-left text-sm font-medium truncate">
                            {{ userStore.user?.username ?? 'Foydalanuvchi' }}
                        </span>

                        <UIcon name="i-lucide-chevrons-up-down" class="text-dimmed shrink-0 w-4 h-4" />
                    </button>
                </UDropdownMenu>
            </template>
        </USidebar>

        <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
            <div class="h-(--ui-header-height) shrink-0 flex items-center px-4 border-b border-default">
                <UButton icon="i-lucide-panel-left" color="neutral" variant="ghost" aria-label="Toggle sidebar"
                    @click="open = !open" />
            </div>

            <div class="flex-1 overflow-y-auto">
                <slot />
            </div>
        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap');

.header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 0px;
}

.header img {
    width: 36px;
    height: 36px;
    border-radius: 100%;
}

.header h2 {
    font-weight: 700;
    font-family: 'DM Sans', sans-serif;
}
</style>
