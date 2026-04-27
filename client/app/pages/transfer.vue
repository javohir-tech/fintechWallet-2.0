<template>
    <div class="max-w-md mx-auto mt-10 space-y-4">
        <h1 class="text-xl font-semibold">Pul o'tkazma</h1>

        <!-- Input + button -->
        <div class="flex gap-2">
            <UInput v-model="card_number" placeholder="Karta raqamini kiriting" :disabled="loading" class="flex-1"
                @keyup.enter="handleSubmit" />
            <UButton :loading="loading" @click="handleSubmit">
                Qidirish
            </UButton>
        </div>

        <Transition name="fade">
            <div v-if="data" class="border rounded-xl p-4 flex items-center gap-4 cursor-pointer
               hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors" @click="goToTransfer">
                <!-- Avatar -->
                <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900
                 flex items-center justify-center text-primary-600 font-bold text-lg">
                    {{ data.username.charAt(0).toUpperCase() }}
                </div>

                <!-- Ma'lumotlar -->
                <div class="flex-1 min-w-0">
                    <p class="font-medium truncate">{{ data.username }}</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400">
                        {{ data.masked_number }}
                    </p>
                </div>

                <!-- O'q -->
                <UIcon name="i-heroicons-chevron-right" class="text-gray-400 shrink-0" />
            </div>
        </Transition>
    </div>
</template>

<script setup lang="ts">
import type { ICard } from '~/types';
const card_number = ref("");
const toast = useToast();

const { data, loading, LookCard, reset } = useTransaction<ICard>();

watch(card_number, () => {
    reset();
});

async function handleSubmit() {
    if (!card_number.value.trim()) {
        toast.add({
            title: "Karta raqamini kiriting",
            color: "primary",
            icon: "i-heroicons-exclamation-circle",
        });
        return;
    }

    const response = await LookCard(card_number.value);

    if (!response.success) {
        toast.add({
            description: response.message,
            color: "error"
        })
    }
}

function goToTransfer() {
    navigateTo({ path: "/createtransfer", query: { wallet_id: data.value?.wallet_id  } })
}

</script>