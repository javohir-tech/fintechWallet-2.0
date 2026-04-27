<template>
  <div class="max-w-lg mx-auto mt-10 space-y-6">
    <h1 class="text-xl font-semibold">Profil</h1>

    <!-- Avatar + asosiy ma'lumotlar -->
    <div class="border rounded-xl p-6 flex flex-col items-center gap-4 text-center">
      <!-- Avatar -->
      <div class="relative">
        <img
          v-if="user?.avatar"
          :src="user.avatar"
          :alt="user.username"
          class="w-20 h-20 rounded-full object-cover ring-2 ring-primary-500"
        />
        <div
          v-else
          class="w-20 h-20 rounded-full bg-primary-100 dark:bg-primary-900
                 flex items-center justify-center text-primary-600 font-bold text-3xl"
        >
          {{ userInitial }}
        </div>
      </div>

      <!-- Ism -->
      <div class="space-y-1">
        <h2 class="text-xl font-semibold">{{ user?.username ?? "—" }}</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          {{ user?.email || user?.phone_number || "—" }}
        </p>
        <UBadge :color="authStatusColor" variant="soft" size="sm">
          {{ authStatusLabel }}
        </UBadge>
      </div>
    </div>

    <!-- Wallet ma'lumotlari -->
    <div class="border rounded-xl divide-y divide-gray-100 dark:divide-gray-800">
      <div class="p-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-gray-500 dark:text-gray-400 text-sm">
          <UIcon name="i-heroicons-wallet" />
          <span>Balans</span>
        </div>
        <div v-if="balanceLoading" class="flex items-center gap-2">
          <UIcon name="i-heroicons-arrow-path" class="animate-spin text-gray-400" />
          <span class="text-sm text-gray-400">Yuklanmoqda...</span>
        </div>
        <span v-else class="font-semibold text-lg">
          {{ formattedBalance }}
          <span class="text-sm font-normal text-gray-400 ml-1">{{ balance?.currency ?? "UZS" }}</span>
        </span>
      </div>

      <div v-if="balance?.card" class="p-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-gray-500 dark:text-gray-400 text-sm">
          <UIcon name="i-heroicons-credit-card" />
          <span>Karta</span>
        </div>
        <div class="text-right">
          <p class="text-sm font-medium">{{ balance.card.card_holder_name }}</p>
          <p class="text-xs font-mono text-gray-400">{{ maskedCard }}</p>
        </div>
      </div>

      <div v-if="balance?.card" class="p-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-gray-500 dark:text-gray-400 text-sm">
          <UIcon name="i-heroicons-calendar" />
          <span>Muddati</span>
        </div>
        <span class="text-sm font-mono">
          {{ balance.card.expiry_month }}/{{ balance.card.expiry_year }}
        </span>
      </div>
    </div>

    <!-- Qo'shimcha info -->
    <div class="border rounded-xl divide-y divide-gray-100 dark:divide-gray-800">
      <div class="p-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-gray-500 dark:text-gray-400 text-sm">
          <UIcon name="i-heroicons-identification" />
          <span>ID</span>
        </div>
        <span class="text-xs font-mono text-gray-400 truncate max-w-48">{{ user?.id ?? "—" }}</span>
      </div>

      <div class="p-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-gray-500 dark:text-gray-400 text-sm">
          <UIcon name="i-heroicons-device-phone-mobile" />
          <span>Kirish turi</span>
        </div>
        <UBadge color="neutral" variant="soft" size="sm">
          {{ user?.auth_type === "via_email" ? "Email" : "Telefon" }}
        </UBadge>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex gap-3">
      <UButton
        block
        variant="outline"
        icon="i-heroicons-arrow-path"
        :loading="balanceLoading"
        @click="getBalance"
      >
        Yangilash
      </UButton>
      <UButton
        block
        color="error"
        variant="outline"
        icon="i-lucide-log-out"
        :loading="logoutLoading"
        @click="handleLogout"
      >
        Chiqish
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/store/useUser";
import useAuth from "~/composables/useAuth";
import type { IBalance } from "~/types";

const userStore = useUserStore();
const { logout } = useAuth();

const user = computed(() => userStore.user);

const userInitial = computed(() => {
  const name = user.value?.username ?? "";
  return name.charAt(0).toUpperCase() || "?";
});

const authStatusLabel = computed(() => {
  const map: Record<string, string> = {
    new: "Yangi",
    verifed: "Tasdiqlangan",
    done: "Faol",
    photo_done: "Faol",
    logout: "Chiqib ketgan",
  };
  return map[user.value?.auth_status ?? ""] ?? "—";
});

const authStatusColor = computed(() => {
  const map: Record<string, string> = {
    new: "warning",
    verifed: "info",
    done: "success",
    photo_done: "success",
    logout: "neutral",
  };
  return map[user.value?.auth_status ?? ""] ?? "neutral";
});

// ── Wallet / Balance ─────────────────────────────────────────
const { data: balanceData, loading: balanceLoading, getBalance } = useBalance<IBalance>();
const balance = computed(() => balanceData.value);

const formattedBalance = computed(() => {
  if (!balance.value) return "—";
  return parseFloat(balance.value.balance).toLocaleString("uz-UZ");
});

const maskedCard = computed(() => {
  const num = balance.value?.card?.card_number ?? "";
  if (!num) return "—";
  return `**** **** **** ${num.slice(-4)}`;
});

onMounted(() => {
  getBalance();
});

// ── Logout ───────────────────────────────────────────────────
const logoutLoading = ref(false);

async function handleLogout() {
  logoutLoading.value = true;
  try {
    await logout();
  } finally {
    logoutLoading.value = false;
  }
}
</script>
