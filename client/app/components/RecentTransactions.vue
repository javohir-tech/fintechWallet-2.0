<template>
  <div class="rounded-2xl border p-5 flex flex-col gap-3" style="aspect-ratio: 1.7;">
    <!-- Header -->
    <div class="flex items-center justify-between shrink-0">
      <p class="text-sm font-semibold">So'nggi o'tkazmalar</p>
      <NuxtLink
        to="/transactions"
        class="text-xs text-primary-500 hover:text-primary-600 transition-colors"
      >
        Barchasi →
      </NuxtLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <UIcon name="i-heroicons-arrow-path" class="animate-spin text-gray-400 text-xl" />
    </div>

    <!-- Empty -->
    <div v-else-if="!items.length" class="flex-1 flex flex-col items-center justify-center gap-1">
      <UIcon name="i-heroicons-inbox" class="text-2xl text-gray-300" />
      <p class="text-xs text-gray-400">Tranzaksiyalar yo'q</p>
    </div>

    <!-- List -->
    <div v-else class="flex-1 flex flex-col gap-1 overflow-hidden">
      <div
        v-for="tx in items"
        :key="tx.id"
        class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800
               rounded-lg px-1.5 py-1 transition-colors"
        @click="navigateTo({ path: '/transactionDetail', query: { id: tx.id } })"
      >
        <!-- Icon -->
        <div
          class="w-7 h-7 rounded-full flex items-center justify-center shrink-0"
          :class="tx.direction ? 'bg-emerald-100 dark:bg-emerald-900' : 'bg-rose-100 dark:bg-rose-900'"
        >
          <UIcon
            :name="tx.direction ? 'i-heroicons-arrow-down-left' : 'i-heroicons-arrow-up-right'"
            class="text-xs"
            :class="tx.direction ? 'text-emerald-600' : 'text-rose-500'"
          />
        </div>

        <!-- Name -->
        <p class="flex-1 text-xs font-medium truncate">
          {{ tx.direction ? tx.from_user?.username : tx.to_user?.username }}
        </p>

        <!-- Amount -->
        <p class="text-xs font-semibold shrink-0"
           :class="tx.direction ? 'text-emerald-600' : 'text-rose-500'">
          {{ tx.direction ? '+' : '-' }}{{ fmt(tx.amount) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Transactionservices } from "~/services/transaction.services";
import type { ITransaction } from "~/types";

const loading = ref(true);
const items = ref<ITransaction[]>([]);

function fmt(val: string) {
  return Number(val).toLocaleString("uz-UZ");
}

onMounted(async () => {
  try {
    const { data } = await Transactionservices.getAllTransactions();
    items.value = (data as ITransaction[]).slice(0, 4);
  } catch {
    //
  } finally {
    loading.value = false;
  }
});
</script>
