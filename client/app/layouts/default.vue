<script setup lang="ts">
import type { DropdownMenuItem, NavigationMenuItem } from '@nuxt/ui'

const open = ref(true)

const colorMode = useColorMode()

function getItems(state: 'collapsed' | 'expanded') {
    return [
        {
            label: 'Dashboard',
            icon: 'i-lucide-inbox',
            to: "/",
            // badge: '4',
        },
        {
            label: 'Transfer',
            icon: 'i-lucide-credit-card',
            to: "/transfer"
        },
        {
            label: 'Transactions',
            icon: 'i-lucide-square-activity',
            to: "/transactions"
        },
        {
            label: 'Settings',
            icon: 'i-lucide-settings',
            to : "/settings"
        }
    ] satisfies NavigationMenuItem[]
}

const user = ref({
    name: 'Benjamin Canac',
    avatar: {
        src: 'https://github.com/benjamincanac.png',
        alt: 'Benjamin Canac'
    }
})

const userItems = computed<DropdownMenuItem[][]>(() => [
    [
        {
            label: 'Profile',
            icon: 'i-lucide-user'
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
            to: 'https://github.com/nuxt/ui',
            target: '_blank'
        },
        {
            label: 'Log out',
            icon: 'i-lucide-log-out'
        }
    ]
])
</script>

<template>
    <div class="flex flex-1">
        <USidebar v-model:open="open" collapsible="icon" rail :ui="{
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
                <UNavigationMenu :key="state" :items="getItems(state)" orientation="vertical"
                    :ui="{ link: 'p-1.5 overflow-hidden' }" />
            </template>

            <template #footer>
                <UDropdownMenu :items="userItems" :content="{ align: 'center', collisionPadding: 12 }"
                    :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width) min-w-48' }">
                    <UButton v-bind="user" :label="user?.name" trailing-icon="i-lucide-chevrons-up-down" color="neutral"
                        variant="ghost" square class="w-full data-[state=open]:bg-elevated overflow-hidden" :ui="{
                            trailingIcon: 'text-dimmed ms-auto'
                        }" />
                </UDropdownMenu>
            </template>
        </USidebar>

        <div class="flex-1 flex flex-col">
            <div class="h-(--ui-header-height) shrink-0 flex items-center px-4 border-b border-default">
                <UButton icon="i-lucide-panel-left" color="neutral" variant="ghost" aria-label="Toggle sidebar"
                    @click="open = !open" />
            </div>

            <div class="flex-1 p-4">
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
