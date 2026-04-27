<template>
  <div class="max-w-md mx-auto mt-10 space-y-6">

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <UIcon name="i-heroicons-arrow-path" class="animate-spin text-3xl text-primary-500" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-16 space-y-3">
      <UIcon name="i-heroicons-exclamation-circle" class="text-4xl text-red-500" />
      <p class="text-gray-600 dark:text-gray-400">Transaksiya topilmadi</p>
      <UButton variant="ghost" @click="navigateTo('/transactions')">Orqaga</UButton>
    </div>

    <!-- Content -->
    <template v-else-if="tx">
      <!-- Header -->
      <div class="text-center space-y-2" id="receipt-header">
        <div
          class="w-16 h-16 rounded-full mx-auto flex items-center justify-center text-2xl"
          :class="statusIcon.bg"
        >
          <UIcon :name="statusIcon.icon" :class="statusIcon.color" />
        </div>
        <h1 class="text-2xl font-bold" :class="statusIcon.color">
          {{ statusLabel }}
        </h1>
        <p class="text-3xl font-semibold text-gray-900 dark:text-white">
          {{ formatAmount(tx.amount) }} so'm
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Komissiya: {{ formatAmount(tx.fee) }} so'm
        </p>
      </div>

      <!-- Receipt card -->
      <div id="receipt-body" class="border rounded-xl divide-y divide-gray-100 dark:divide-gray-800">
        <!-- From -->
        <div class="p-4 flex items-center justify-between gap-3">
          <span class="text-sm text-gray-500 dark:text-gray-400 shrink-0">Jo'natuvchi</span>
          <div class="text-right min-w-0">
            <p class="font-medium text-sm truncate">{{ tx.from_user?.username ?? "—" }}</p>
            <p class="text-xs text-gray-400 font-mono">{{ tx.from_user?.masked_number ?? "" }}</p>
          </div>
        </div>

        <!-- To -->
        <div class="p-4 flex items-center justify-between gap-3">
          <span class="text-sm text-gray-500 dark:text-gray-400 shrink-0">Qabul qiluvchi</span>
          <div class="text-right min-w-0">
            <p class="font-medium text-sm truncate">{{ tx.to_user?.username ?? "—" }}</p>
            <p class="text-xs text-gray-400 font-mono">{{ tx.to_user?.masked_number ?? "" }}</p>
          </div>
        </div>

        <!-- Type -->
        <div class="p-4 flex items-center justify-between">
          <span class="text-sm text-gray-500 dark:text-gray-400">Tur</span>
          <UBadge :color="txTypeColor" variant="soft">{{ txTypeLabel }}</UBadge>
        </div>

        <!-- Status -->
        <div class="p-4 flex items-center justify-between">
          <span class="text-sm text-gray-500 dark:text-gray-400">Holat</span>
          <UBadge :color="statusBadgeColor" variant="soft">{{ statusLabel }}</UBadge>
        </div>

        <!-- Debit / Credit -->
        <div v-if="tx.debit_amount" class="p-4 flex items-center justify-between">
          <span class="text-sm text-gray-500 dark:text-gray-400">Debet</span>
          <span class="text-sm font-mono text-red-500">-{{ formatAmount(tx.debit_amount) }} so'm</span>
        </div>
        <div v-if="tx.credit_amount" class="p-4 flex items-center justify-between">
          <span class="text-sm text-gray-500 dark:text-gray-400">Kredit</span>
          <span class="text-sm font-mono text-green-500">+{{ formatAmount(tx.credit_amount) }} so'm</span>
        </div>

        <!-- Description -->
        <div v-if="tx.description" class="p-4 flex items-center justify-between gap-3">
          <span class="text-sm text-gray-500 dark:text-gray-400 shrink-0">Izoh</span>
          <p class="text-sm text-right truncate">{{ tx.description }}</p>
        </div>

        <!-- ID -->
        <div class="p-4 flex items-center justify-between gap-3">
          <span class="text-sm text-gray-500 dark:text-gray-400 shrink-0">ID</span>
          <p class="text-xs font-mono text-gray-400 truncate">{{ tx.id }}</p>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 no-print">
        <UButton
          block
          variant="outline"
          icon="i-heroicons-arrow-down-tray"
          @click="downloadPDF"
        >
          PDF yuklab olish
        </UButton>
        <UButton
          block
          icon="i-heroicons-list-bullet"
          @click="navigateTo('/transactions')"
        >
          Barcha o'tkazmalar
        </UButton>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { Transactionservices } from "~/services/transaction.services";
import type { ITransaction } from "~/types";

const route = useRoute();
const id = computed(() => route.query.id as string);

const tx = ref<ITransaction | null>(null);
const loading = ref(true);
const error = ref(false);

onMounted(async () => {
  if (!id.value) {
    error.value = true;
    loading.value = false;
    return;
  }
  try {
    const { data } = await Transactionservices.getTransactionDetail(id.value);
    tx.value = data as ITransaction;
  } catch {
    error.value = true;
  } finally {
    loading.value = false;
  }
});

// ── Formatters ──────────────────────────────────────────────
function formatAmount(val: string | null): string {
  if (!val) return "0";
  return parseFloat(val).toLocaleString("uz-UZ");
}

const statusLabel = computed(() => {
  const map: Record<string, string> = {
    PENDING: "Kutilmoqda",
    SUCCESS: "Bajarildi",
    FAILED: "Muvaffaqiyatsiz",
    REVERSED: "Qaytarildi",
  };
  return map[tx.value?.status ?? ""] ?? tx.value?.status ?? "—";
});

const statusBadgeColor = computed(() => {
  const map: Record<string, string> = {
    PENDING: "warning",
    SUCCESS: "success",
    FAILED: "error",
    REVERSED: "neutral",
  };
  return map[tx.value?.status ?? ""] ?? "neutral";
});

const statusIcon = computed(() => {
  const map: Record<string, { icon: string; color: string; bg: string }> = {
    SUCCESS: { icon: "i-heroicons-check-circle", color: "text-green-500", bg: "bg-green-100 dark:bg-green-900" },
    FAILED: { icon: "i-heroicons-x-circle", color: "text-red-500", bg: "bg-red-100 dark:bg-red-900" },
    PENDING: { icon: "i-heroicons-clock", color: "text-yellow-500", bg: "bg-yellow-100 dark:bg-yellow-900" },
    REVERSED: { icon: "i-heroicons-arrow-uturn-left", color: "text-gray-500", bg: "bg-gray-100 dark:bg-gray-800" },
  };
  return map[tx.value?.status ?? ""] ?? map.PENDING;
});

const txTypeLabel = computed(() => {
  const map: Record<string, string> = {
    TRANSFER: "O'tkazma",
    TOPUP: "To'ldirish",
    WITHDRAW: "Yechish",
  };
  return map[tx.value?.txtype ?? ""] ?? tx.value?.txtype ?? "—";
});

const txTypeColor = computed(() => {
  const map: Record<string, string> = {
    TRANSFER: "primary",
    TOPUP: "success",
    WITHDRAW: "warning",
  };
  return map[tx.value?.txtype ?? ""] ?? "neutral";
});

// ── PDF download (print) ─────────────────────────────────────
function downloadPDF() {
  window.print();
}
</script>

<style>
@media print {
  body * {
    visibility: hidden;
  }
  #receipt-header,
  #receipt-header *,
  #receipt-body,
  #receipt-body * {
    visibility: visible;
  }
  #receipt-header {
    position: fixed;
    top: 40px;
    left: 0;
    right: 0;
  }
  #receipt-body {
    position: fixed;
    top: 200px;
    left: 50%;
    transform: translateX(-50%);
    width: 420px;
  }
  .no-print {
    display: none !important;
  }
}
</style>
