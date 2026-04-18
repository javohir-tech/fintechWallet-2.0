<script setup lang="ts">
import AppSidebar from '~/components/layout/AppSidebar.vue';

</script>

<template>
    <AppSidebar>
        <main>
            <slot/>
        </main>
    </AppSidebar>
</template>