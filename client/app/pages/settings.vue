<template>
  <div class="max-w-lg mx-auto mt-10 space-y-8">
    <h1 class="text-xl font-semibold">{{ $t('settings.title') }}</h1>

    <!-- Appearance section -->
    <section class="border rounded-xl divide-y divide-gray-100 dark:divide-gray-800">

      <!-- Primary color -->
      <div class="p-4 flex items-center justify-between gap-4">
        <div>
          <p class="text-sm font-medium">{{ $t('settings.color') }}</p>
          <p class="text-xs text-gray-400 mt-0.5">{{ currentColor?.label }}</p>
        </div>
        <USelect
          v-model="selectedColor"
          :items="colorOptions"
          class="w-44"
          @update:model-value="applyColor"
        >
          <template #leading>
            <span
              class="w-3 h-3 rounded-full shrink-0 ml-1"
              :style="{ backgroundColor: currentColor?.hex }"
            />
          </template>
          <template #item="{ item }">
            <span
              class="w-3 h-3 rounded-full shrink-0"
              :style="{ backgroundColor: item.hex }"
            />
            <span>{{ item.label }}</span>
          </template>
        </USelect>
      </div>

      <!-- Theme -->
      <div class="p-4 flex items-center justify-between gap-4">
        <p class="text-sm font-medium">{{ $t('settings.theme') }}</p>
        <USelect
          v-model="colorMode.preference"
          :items="themeOptions"
          class="w-44"
        >
          <template #leading>
            <UIcon :name="currentTheme?.icon ?? ''" class="ml-1" />
          </template>
          <template #item="{ item }">
            <UIcon :name="item.icon" />
            <span>{{ item.label }}</span>
          </template>
        </USelect>
      </div>

      <!-- Sidebar side -->
      <div class="p-4 flex items-center justify-between gap-4">
        <p class="text-sm font-medium">{{ $t('settings.sidebar') }}</p>
        <USelect
          v-model="selectedSide"
          :items="sideOptions"
          class="w-44"
          @update:model-value="settings.setSidebarSide"
        >
          <template #leading>
            <UIcon :name="currentSide?.icon ?? ''" class="ml-1" />
          </template>
          <template #item="{ item }">
            <UIcon :name="item.icon" />
            <span>{{ item.label }}</span>
          </template>
        </USelect>
      </div>
    </section>

    <!-- Language section -->
    <section class="border rounded-xl divide-y divide-gray-100 dark:divide-gray-800">
      <div class="p-4 flex items-center justify-between gap-4">
        <p class="text-sm font-medium">{{ $t('settings.language') }}</p>
        <USelect
          v-model="selectedLocale"
          :items="langOptions"
          class="w-44"
          @update:model-value="applyLocale"
        >
          <template #leading>
            <span class="ml-1">{{ currentLang?.flag }}</span>
          </template>
          <template #item="{ item }">
            <span>{{ item.flag }}</span>
            <span>{{ item.label }}</span>
          </template>
        </USelect>
      </div>
    </section>

    <!-- Reset -->
    <UButton
      block
      color="error"
      variant="outline"
      icon="i-heroicons-arrow-uturn-left"
      @click="handleReset"
    >
      Barcha sozlamalarni asliga qaytarish
    </UButton>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore, type PrimaryColor, type SidebarSide, DEFAULTS } from "~/store/useSettings";

const settings = useSettingsStore();
const colorMode = useColorMode();
const appConfig = useAppConfig();
const { setLocale: i18nSetLocale, t } = useI18n();
const toast = useToast();

// ── Colors ───────────────────────────────────────────────────
const colors = [
  { value: "red",     label: "Red",     hex: "#ef4444" },
  { value: "orange",  label: "Orange",  hex: "#f97316" },
  { value: "amber",   label: "Amber",   hex: "#f59e0b" },
  { value: "yellow",  label: "Yellow",  hex: "#eab308" },
  { value: "lime",    label: "Lime",    hex: "#84cc16" },
  { value: "green",   label: "Green",   hex: "#22c55e" },
  { value: "emerald", label: "Emerald", hex: "#10b981" },
  { value: "teal",    label: "Teal",    hex: "#14b8a6" },
  { value: "cyan",    label: "Cyan",    hex: "#06b6d4" },
  { value: "sky",     label: "Sky",     hex: "#0ea5e9" },
  { value: "blue",    label: "Blue",    hex: "#3b82f6" },
  { value: "indigo",  label: "Indigo",  hex: "#6366f1" },
  { value: "violet",  label: "Violet",  hex: "#8b5cf6" },
  { value: "purple",  label: "Purple",  hex: "#a855f7" },
  { value: "fuchsia", label: "Fuchsia", hex: "#d946ef" },
  { value: "pink",    label: "Pink",    hex: "#ec4899" },
  { value: "rose",    label: "Rose",    hex: "#f43f5e" },
] as const;

const colorOptions = colors.map(c => ({ ...c, value: c.value }));
const selectedColor = computed({
  get: () => settings.primaryColor,
  set: (val: PrimaryColor) => applyColor(val),
});
const currentColor = computed(() => colors.find(c => c.value === settings.primaryColor));

function applyColor(val: PrimaryColor) {
  settings.setColor(val);
  appConfig.ui.colors.primary = val;
}

// ── Theme ─────────────────────────────────────────────────────
const themeOptions = computed(() => [
  { value: "light",  label: t("settings.theme_light"),  icon: "i-heroicons-sun" },
  { value: "dark",   label: t("settings.theme_dark"),   icon: "i-heroicons-moon" },
  { value: "system", label: t("settings.theme_system"), icon: "i-heroicons-computer-desktop" },
]);
const currentTheme = computed(() => themeOptions.value.find(m => m.value === colorMode.preference));

// ── Sidebar ───────────────────────────────────────────────────
const sideOptions = computed(() => [
  { value: "left" as SidebarSide,  label: t("settings.sidebar_left"),  icon: "i-heroicons-bars-3-bottom-left" },
  { value: "right" as SidebarSide, label: t("settings.sidebar_right"), icon: "i-heroicons-bars-3-bottom-right" },
]);
const sidebarCookie = useCookie<SidebarSide>('sidebar_side', { default: () => 'left' })
const selectedSide = computed({
  get: () => sidebarCookie.value,
  set: (val: SidebarSide) => {
    sidebarCookie.value = val
    settings.setSidebarSide(val)
  },
});
const currentSide = computed(() => sideOptions.value.find(s => s.value === sidebarCookie.value));

// ── Language ──────────────────────────────────────────────────
const langs = [
  { value: "uz", label: "O'zbek",  flag: "🇺🇿" },
  { value: "ru", label: "Русский", flag: "🇷🇺" },
  { value: "en", label: "English", flag: "🇬🇧" },
];
const langOptions = langs;
const selectedLocale = computed({
  get: () => settings.locale,
  set: (val: string) => applyLocale(val),
});
const currentLang = computed(() => langs.find(l => l.value === settings.locale));

async function applyLocale(code: string) {
  settings.setLocale(code);
  await i18nSetLocale(code);
}

// ── Reset ─────────────────────────────────────────────────────
async function handleReset() {
  settings.reset();
  sidebarCookie.value = DEFAULTS.sidebarSide;
  appConfig.ui.colors.primary = DEFAULTS.primaryColor;
  colorMode.preference = "system";
  await i18nSetLocale(DEFAULTS.locale);
  toast.add({ title: "Sozlamalar asliga qaytarildi", color: "success", icon: "i-heroicons-check-circle" });
}
</script>
