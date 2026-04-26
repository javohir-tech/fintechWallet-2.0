<template>
  <div class="rounded-2xl p-5 flex flex-col justify-between bg-primary-500"
       style="aspect-ratio: 1.7;">

    <div class="flex justify-between items-start">
      <div class="w-7 h-5 rounded bg-white/30 border border-white/40" />
      <span class="text-xs text-white/80 bg-white/15 px-2 py-0.5 rounded-full">
        {{ data?.card.card_type }}
      </span>
    </div>

    <div>
      <p class="text-xs text-white/70 mb-0.5">Balans</p>
      <div class="flex items-center gap-2">
        <p class="text-xl font-medium text-white tracking-tight">
          {{ showBalance ? Number(data?.balance).toLocaleString() : '••••••' }}
          <span class="text-sm opacity-80">{{ data?.currency }}</span>
        </p>
        <button @click="showBalance = !showBalance"
                class="bg-white/15 border border-white/25 rounded-md p-1">
          <UIcon
            :name="showBalance ? 'i-heroicons-eye-slash' : 'i-heroicons-eye'"
            class="w-3.5 h-3.5 text-white"
          />
        </button>
      </div>
    </div>

    <div>
      <p class="text-xs text-white/70 tracking-widest mb-1.5">
        {{ formatCardNumber(data?.card.card_number) }}
      </p>
      <div class="flex justify-between items-end">
        <div>
          <p class="text-[9px] text-white/55 uppercase tracking-wide">Karta egasi</p>
          <p class="text-xs text-white font-medium">{{ data?.card.card_holder_name }}</p>
        </div>
        <div class="text-right">
          <p class="text-[9px] text-white/55 uppercase tracking-wide">Muddat</p>
          <p class="text-xs text-white font-medium">
            {{ data?.card.expiry_month }}/{{ data?.card.expiry_year }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IBalance } from '~/types'

defineProps<{
  data: IBalance | null
}>()

const showBalance = useCookie<boolean>('show_balance', {
  default: () => false,
  encode: (val) => String(val),
  decode: (val) => val === 'true',
})

function formatCardNumber(number?: string) {
  if (!number) return ''
  return number.replace(/(\d{4})(?=\d)/g, '$1 ')
}
</script>