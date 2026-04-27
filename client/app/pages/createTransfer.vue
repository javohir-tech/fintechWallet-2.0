<template>
  <div class="max-w-md mx-auto mt-10 space-y-6">
    <div class="flex items-center gap-3">
      <UButton
        icon="i-heroicons-arrow-left"
        variant="ghost"
        color="neutral"
        @click="navigateTo('/transfer')"
      />
      <h1 class="text-xl font-semibold">Pul o'tkazma</h1>
    </div>

    <!-- Recipient card info -->
    <div
      v-if="recipient"
      class="border rounded-xl p-4 flex items-center gap-4 bg-gray-50 dark:bg-gray-900"
    >
      <div
        class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900
               flex items-center justify-center text-primary-600 font-bold text-lg shrink-0"
      >
        {{ recipient.username.charAt(0).toUpperCase() }}
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-medium truncate">{{ recipient.username }}</p>
        <p class="text-sm text-gray-500 dark:text-gray-400">{{ recipient.masked_number }}</p>
      </div>
      <UBadge color="success" variant="soft">Qabul qiluvchi</UBadge>
    </div>

    <!-- Amount input -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Summa (so'm)</label>
      <UInput
        v-model="amountStr"
        type="number"
        placeholder="Masalan: 50000"
        :disabled="loading"
        size="lg"
        min="1"
      />
    </div>

    <!-- Description (optional) -->
    <div class="space-y-2">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
        Izoh <span class="text-gray-400 font-normal">(ixtiyoriy)</span>
      </label>
      <UInput
        v-model="description"
        placeholder="Masalan: Oshxona uchun"
        :disabled="loading"
      />
    </div>

    <!-- Submit -->
    <UButton
      block
      size="lg"
      :loading="loading"
      :disabled="!canSubmit"
      @click="handleTransfer"
    >
      O'tkazish
    </UButton>
  </div>
</template>

<script setup lang="ts">
import { Transactionservices } from "~/services/transaction.services";
import type { ICard, ITransaction } from "~/types";
import { readCache } from "~/utils/cache";

const route = useRoute();
const toast = useToast();

const wallet_id = computed(() => route.query.wallet_id as string);

// Recipient — cache dan topamiz
const recipient = computed<ICard | null>(() => {
  const cache = readCache();
  for (const card of cache.values()) {
    if (card.wallet_id === wallet_id.value) return card;
  }
  return null;
});

const amountStr = ref("");
const description = ref("");
const loading = ref(false);

const canSubmit = computed(() => {
  const amount = parseFloat(amountStr.value);
  return !!wallet_id.value && amount > 0 && !loading.value;
});

function generateIdempotencyKey(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

async function handleTransfer() {
  const amount = parseFloat(amountStr.value);
  if (!amount || amount <= 0) {
    toast.add({ title: "Summani kiriting", color: "warning", icon: "i-heroicons-exclamation-circle" });
    return;
  }

  loading.value = true;
  try {
    const { data } = await Transactionservices.createTransfer({
      wallet_id: wallet_id.value,
      amount,
      idempotency_key: generateIdempotencyKey(),
    });

    const tx = data as ITransaction;

    await navigateTo({
      path: "/transactionDetail",
      query: { id: tx.id },
    });
  } catch (err: unknown) {
    let message = "Xatolik yuz berdi";
    if (
      err &&
      typeof err === "object" &&
      "response" in err &&
      err.response &&
      typeof err.response === "object" &&
      "data" in err.response
    ) {
      const d = err.response.data as Record<string, unknown>;
      message =
        (d.detail as string) ??
        (d.non_field_errors as string[])?.[0] ??
        message;
    }
    toast.add({ description: message, color: "error" });
  } finally {
    loading.value = false;
  }
}
</script>
