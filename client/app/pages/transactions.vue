<template>
  <div class="max-w-2xl mx-auto mt-10 space-y-4">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-semibold">O'tkazmalar tarixi</h1>
      <UBadge v-if="total > 0" color="neutral" variant="soft">
        {{ filtered.length }} / {{ total }}
      </UBadge>
    </div>

    <!-- Filters -->
    <div class="space-y-3">
      <!-- Search -->
      <UInput
        v-model="search"
        placeholder="Ism yoki summa bo'yicha qidirish..."
        icon="i-heroicons-magnifying-glass"
        :ui="{ base: 'w-full' }"
      />

      <div class="flex flex-wrap gap-2">
        <!-- Direction -->
        <div class="flex gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
          <button
            v-for="d in directionOptions"
            :key="d.value"
            class="px-3 py-1 text-xs font-medium rounded-md transition-all"
            :class="direction === d.value
              ? 'bg-white dark:bg-gray-700 shadow text-gray-900 dark:text-white'
              : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'"
            @click="direction = d.value"
          >
            {{ d.label }}
          </button>
        </div>

        <!-- Status -->
        <USelect
          v-model="status"
          :items="statusOptions"
          placeholder="Holat"
          class="w-36"
          size="sm"
        />

        <!-- Type -->
        <USelect
          v-model="txtype"
          :items="typeOptions"
          placeholder="Tur"
          class="w-36"
          size="sm"
        />

        <!-- Reset -->
        <UButton
          v-if="hasFilter"
          variant="ghost"
          color="neutral"
          size="sm"
          icon="i-heroicons-x-mark"
          @click="resetFilters"
        >
          Tozalash
        </UButton>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <UIcon name="i-heroicons-arrow-path" class="animate-spin text-3xl text-primary-500" />
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" class="text-center py-16 space-y-3">
      <UIcon name="i-heroicons-funnel" class="text-4xl text-gray-300" />
      <p class="text-gray-500">
        {{ hasFilter ? 'Filter bo\'yicha natija topilmadi' : 'Hali o\'tkazmalar yo\'q' }}
      </p>
      <UButton v-if="hasFilter" variant="ghost" @click="resetFilters">
        Filterni tozalash
      </UButton>
      <UButton v-else @click="navigateTo('/transfer')">O'tkazma qilish</UButton>
    </div>

    <!-- List -->
    <div v-else class="border rounded-xl overflow-hidden divide-y divide-gray-100 dark:divide-gray-800">
      <div
        v-for="tx in filtered"
        :key="tx.id"
        class="p-4 flex items-center gap-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors"
        @click="navigateTo({ path: '/transactionDetail', query: { id: tx.id } })"
      >
        <!-- Icon -->
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center shrink-0"
          :class="tx.direction ? 'bg-emerald-100 dark:bg-emerald-900' : 'bg-rose-100 dark:bg-rose-900'"
        >
          <UIcon
            :name="tx.direction ? 'i-heroicons-arrow-down-left' : 'i-heroicons-arrow-up-right'"
            :class="tx.direction ? 'text-emerald-600' : 'text-rose-500'"
          />
        </div>

        <!-- Info -->
        <div class="flex-1 min-w-0">
          <p class="font-medium text-sm truncate">
            {{ tx.direction ? tx.from_user?.username : tx.to_user?.username }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ txTypeLabel(tx.txtype) }}
          </p>
        </div>

        <!-- Amount + status -->
        <div class="text-right shrink-0">
          <p
            class="font-semibold text-sm"
            :class="tx.direction ? 'text-emerald-600' : 'text-rose-500'"
          >
            {{ tx.direction ? '+' : '-' }}{{ formatAmount(tx.amount) }} so'm
          </p>
          <UBadge :color="statusColor(tx.status)" variant="soft" size="sm">
            {{ statusLabel(tx.status) }}
          </UBadge>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Transactionservices } from "~/services/transaction.services";
import type { ITransaction } from "~/types";

const transactions = ref<ITransaction[]>([]);
const loading = ref(true);

// ── Filters ───────────────────────────────────────────────────
const search    = ref("");
const direction = ref("");
const status    = ref<string | null>(null);
const txtype    = ref<string | null>(null);

const directionOptions = [
  { label: "Barchasi", value: "" },
  { label: "Kiruvchi",  value: "in" },
  { label: "Chiquvchi", value: "out" },
];

const statusOptions = [
  { label: "Barcha holat",     value: null },
  { label: "Bajarildi",        value: "SUCCESS" },
  { label: "Kutilmoqda",       value: "PENDING" },
  { label: "Muvaffaqiyatsiz",  value: "FAILED" },
  { label: "Qaytarildi",       value: "REVERSED" },
];

const typeOptions = [
  { label: "Barcha tur",  value: null },
  { label: "O'tkazma",    value: "TRANSFER" },
  { label: "To'ldirish",  value: "TOPUP" },
  { label: "Yechish",     value: "WITHDRAW" },
];

const hasFilter = computed(() =>
  !!search.value || !!direction.value || !!status.value || !!txtype.value
);


const total = computed(() => transactions.value.length);

// ── Client-side filter ────────────────────────────────────────
const filtered = computed(() => {
  let list = transactions.value;

  if (direction.value === "in")  list = list.filter(t => t.direction === true);
  if (direction.value === "out") list = list.filter(t => t.direction === false);
  if (status.value)  list = list.filter(t => t.status === status.value);
  if (txtype.value)  list = list.filter(t => t.txtype === txtype.value);

  if (search.value.trim()) {
    const q = search.value.toLowerCase().trim();
    list = list.filter(t => {
      const name = (t.direction ? t.from_user?.username : t.to_user?.username) ?? "";
      return name.toLowerCase().includes(q) || t.amount.includes(q);
    });
  }

  return list;
});

function resetFilters() {
  search.value    = "";
  direction.value = "";
  status.value    = null;
  txtype.value    = null;
}

// ── Helpers ───────────────────────────────────────────────────
function formatAmount(val: string) {
  return parseFloat(val).toLocaleString("uz-UZ");
}

function statusLabel(s: string) {
  const m: Record<string, string> = {
    PENDING: "Kutilmoqda", SUCCESS: "Bajarildi",
    FAILED: "Muvaffaqiyatsiz", REVERSED: "Qaytarildi",
  };
  return m[s] ?? s;
}

function statusColor(s: string) {
  const m: Record<string, string> = {
    PENDING: "warning", SUCCESS: "success",
    FAILED: "error", REVERSED: "neutral",
  };
  return m[s] ?? "neutral";
}

function txTypeLabel(t: string) {
  const m: Record<string, string> = {
    TRANSFER: "O'tkazma", TOPUP: "To'ldirish", WITHDRAW: "Yechish",
  };
  return m[t] ?? t;
}

// ── Fetch ─────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const { data } = await Transactionservices.getAllTransactions();
    transactions.value = data as ITransaction[];
  } catch {
    //
  } finally {
    loading.value = false;
  }
});
</script>
