<template>
  <div class="p-6 space-y-5">
    <div class="grid grid-cols-3 gap-4">
      <BalanceCard :data="data" />
      <RecentTransactions />
      <QuickTransfer />
    </div>

    <WalletChart />
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

import type { IBalance } from '~/types'

const { data, getBalance } = useBalance<IBalance>()

onMounted(() => getBalance())
</script>
