<template>
  <div class="rounded-2xl border p-5 flex flex-col gap-3" style="aspect-ratio: 1.7;">
    <!-- Header -->
    <div class="flex items-center justify-between shrink-0">
      <p class="text-sm font-semibold">Tez o'tkazma</p>
      <NuxtLink
        to="/transfer"
        class="text-xs text-primary-500 hover:text-primary-600 transition-colors"
      >
        Yangi →
      </NuxtLink>
    </div>

    <!-- Empty -->
    <div v-if="!cards.length" class="flex-1 flex flex-col items-center justify-center gap-1">
      <UIcon name="i-heroicons-credit-card" class="text-2xl text-gray-300" />
      <p class="text-xs text-gray-400">Saqlangan kartalar yo'q</p>
      <NuxtLink to="/transfer" class="text-xs text-primary-500 mt-1">O'tkazma qilish</NuxtLink>
    </div>

    <!-- Cards grid -->
    <div v-else class="flex-1 flex flex-col gap-1 overflow-hidden">
      <div
        v-for="card in cards"
        :key="card.card_number"
        class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800
               rounded-lg px-1.5 py-1 transition-colors"
        @click="goTransfer(card)"
      >
        <!-- Avatar -->
        <div
          class="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-900
                 flex items-center justify-center text-primary-600 font-bold text-xs shrink-0"
        >
          {{ card.username.charAt(0).toUpperCase() }}
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="text-xs font-medium truncate">{{ card.username }}</p>
          <p class="text-[10px] text-gray-400 font-mono">{{ card.masked_number }}</p>
        </div>

        <!-- Send button -->
        <div class="w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900
                    flex items-center justify-center shrink-0">
          <UIcon name="i-heroicons-arrow-up-right" class="text-primary-600 text-xs" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { readCache } from "~/utils/cache";
import type { ICard } from "~/types";

const cards = ref<ICard[]>([]);

onMounted(() => {
  const cache = readCache();
  cards.value = Array.from(cache.values()).slice(0, 4);
});

function goTransfer(card: ICard) {
  navigateTo({ path: "/createtransfer", query: { wallet_id: card.wallet_id } });
}
</script>
