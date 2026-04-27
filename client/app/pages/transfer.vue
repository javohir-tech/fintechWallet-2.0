<template>
  <div class="max-w-md mx-auto mt-10 space-y-4">
    <h1 class="text-xl font-semibold">Pul o'tkazma</h1>

    <!-- Input + button -->
    <div class="flex gap-2">
      <UInput
        v-model="card_number"
        placeholder="Karta raqamini kiriting"
        :disabled="loading"
        class="flex-1"
        maxlength="16"
        @focus="isFocused = true"
        @blur="onBlur"
      />
      <UButton :loading="loading" :disabled="card_number.length !== 16" @click="handleSubmit">
        Qidirish
      </UButton>
    </div>

    <!-- ✅ Yozayotganda autocomplete (input fokusda va ma'lumot yo'q) -->
    <Transition name="fade">
      <div
        v-if="isFocused && card_number.length > 0 && suggestions.length > 0 && !data"
        class="border rounded-xl overflow-hidden divide-y divide-gray-100 dark:divide-gray-800"
      >
        <div
          v-for="card in suggestions"
          :key="card.card_number"
          class="p-3 flex items-center gap-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          @mousedown.prevent="selectFromSuggestion(card)"
        >
          <div
            class="w-9 h-9 rounded-full bg-primary-100 dark:bg-primary-900
                   flex items-center justify-center text-primary-600 font-bold shrink-0"
          >
            {{ card.username.charAt(0).toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-sm truncate">{{ card.username }}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ card.masked_number }}</p>
          </div>
          <span class="text-xs font-mono text-gray-400 shrink-0">
            <span class="text-gray-700 dark:text-gray-200">{{ card.card_number.slice(0, card_number.length) }}</span>{{ card.card_number.slice(card_number.length) }}
          </span>
        </div>
      </div>
    </Transition>

    <!-- ✅ Tanlangan / topilgan karta -->
    <Transition name="fade">
      <div
        v-if="data"
        class="border rounded-xl p-4 flex items-center gap-4 cursor-pointer
               hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
        @click="goToTransfer"
      >
        <div
          class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900
                 flex items-center justify-center text-primary-600 font-bold text-lg shrink-0"
        >
          {{ data.username.charAt(0).toUpperCase() }}
        </div>
        <div class="flex-1 min-w-0">
          <p class="font-medium truncate">{{ data.username }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400">{{ data.masked_number }}</p>
        </div>
        <UIcon name="i-heroicons-chevron-right" class="text-gray-400 shrink-0" />
      </div>
    </Transition>

    <!-- ✅ Saqlangan kartalar — inputga teginmasdan tanlash uchun -->
    <Transition name="fade">
      <div v-if="!data && !card_number && cachedCards.length > 0" class="space-y-2">
        <p class="text-sm text-gray-500 dark:text-gray-400 font-medium">Saqlangan kartalar</p>
        <div class="border rounded-xl overflow-hidden divide-y divide-gray-100 dark:divide-gray-800">
          <div
            v-for="card in cachedCards"
            :key="card.card_number"
            class="p-3 flex items-center gap-3 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            @click="selectFromSuggestion(card)"
          >
            <div
              class="w-9 h-9 rounded-full bg-primary-100 dark:bg-primary-900
                     flex items-center justify-center text-primary-600 font-bold shrink-0"
            >
              {{ card.username.charAt(0).toUpperCase() }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-sm truncate">{{ card.username }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ card.masked_number }}</p>
            </div>
            <UIcon name="i-heroicons-chevron-right" class="text-gray-400 shrink-0" />
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { ICard } from "~/types";

const card_number = ref("");
const isFocused = ref(false);
const toast = useToast();

const { data, loading, LookCard, reset, searchCache, selectCard } = useTransaction<ICard>();

// ✅ Har o'zgarishda:
// 1. data ni tozalash
// 2. Cache dan qidirish
// 3. 16 ta va cache da yo'q → API
watch(card_number, async (val) => {
  reset(); // data = null bo'ladi → suggestions chiqadi

  if (val.length === 16 && !suggestions.value.length) {
    await handleSubmit();
  }
});

// ✅ Cache dagi barcha kartalar (input bo'sh bo'lganda ko'rsatish uchun)
const cachedCards = computed(() => searchCache(""));

// ✅ Cache dan prefix bo'yicha filter
const suggestions = computed(() => searchCache(card_number.value));

async function handleSubmit() {
  if (!card_number.value.trim()) {
    toast.add({
      title: "Karta raqamini kiriting",
      color: "warning",
      icon: "i-heroicons-exclamation-circle",
    });
    return;
  }

  const response = await LookCard(card_number.value);

  if (!response.success) {
    toast.add({
      description: response.message,
      color: "error",
    });
  }
}

// ✅ Suggestion tanlanganda
function selectFromSuggestion(card: ICard) {
  selectCard(card);
  card_number.value = card.card_number;
  isFocused.value = false;
  goToTransfer();
}

// ✅ Blur — mousedown.prevent bilan suggestion bosilishiga to'sqinlik qilmaydi
function onBlur() {
  setTimeout(() => {
    isFocused.value = false;
  }, 150);
}

function goToTransfer() {
  navigateTo({
    path: "/createtransfer",
    query: { wallet_id: data.value?.wallet_id },
  });
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>