<template>
    <div class="mode">
        <UButton :icon="colorMode.value === 'dark' ? 'i-lucide-sun' : 'i-lucide-moon'" variant="ghost"
            @click="toggleMode">
        </UButton>
    </div>
    <main>
        <slot />
    </main>
</template>

<script setup lang="ts">
const colorMode = useColorMode()

function toggleMode() {
    colorMode.preference = colorMode.value === 'dark' ? 'ligth' : 'dark'
}
</script>

<style scoped>
.mode{
    position: fixed;
    top: 30px;
    right: 30px;
}
</style>