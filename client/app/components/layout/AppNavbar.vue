<script setup lang="ts">
const colorMode = useColorMode()
const appConfig = useAppConfig()

const colors = [
  { label: 'Ko\'k',     value: 'blue'   },
  { label: 'Yashil',   value: 'green'  },
  { label: 'Binafsha', value: 'violet' },
  { label: 'Qizil',    value: 'red'    },
  { label: 'Sariq',    value: 'amber'  },
  { label: 'Moviy',    value: 'sky'    },
  { label: 'Pushti',   value: 'pink'   },
]

const selectedColor = ref(appConfig.ui.colors.primary ?? 'blue')

watch(selectedColor, (color) => {
  appConfig.ui.colors.primary = color
})

function toggleMode() {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <header class="border-b border-(--ui-border) bg-(--ui-bg) px-6 py-3">
    <div class="flex items-center justify-between">

      <!-- Logo -->
      <span class="text-xl font-bold text-(--ui-primary)">
        FintechWallet
      </span>

      <!-- O'ng tomon -->
      <div class="flex items-center gap-3">

        <!-- Rang tanlash -->
        <USelect
          v-model="selectedColor"
          :items="colors"
          value-key="value"
          label-key="label"
          size="sm"
        />

        <!-- Dark / Light toggle -->
        <UButton
          :icon="colorMode.value === 'dark'
            ? 'i-lucide-sun'
            : 'i-lucide-moon'"
          variant="ghost"
          @click="toggleMode"
        />

      </div>
    </div>
  </header>
</template>