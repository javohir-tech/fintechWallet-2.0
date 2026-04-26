<template>
  <div class="p-6">
    <div class="grid grid-cols-3 gap-4">

      <BalanceCard :data="data" />

      <div class="rounded-2xl border border-dashed border-gray-200 dark:border-gray-700
                  flex items-center justify-center" style="aspect-ratio: 1.7;">
        <p class="text-sm text-gray-400">Bo'sh slot</p>
      </div>
      <div class="rounded-2xl border border-dashed border-gray-200 dark:border-gray-700
                  flex items-center justify-center" style="aspect-ratio: 1.7;">
        <p class="text-sm text-gray-400">Bo'sh slot</p>
      </div>
    </div>

    <div class="mt-5">
      <!-- diagramma -->
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import type { IBalance } from '~/types'

const { data, getBalance } = useBalance<IBalance>()

onMounted(() => {
  getBalance()
})
</script>