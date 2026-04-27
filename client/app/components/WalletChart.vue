<template>
  <div class="border rounded-2xl p-5 space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h2 class="font-semibold text-base">Pul harakati</h2>
        <p class="text-xs text-gray-400 mt-0.5">Kiruvchi va chiquvchi tranzaksiyalar</p>
      </div>

      <!-- Period tabs -->
      <div class="flex gap-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
        <button
          v-for="p in periods"
          :key="p.value"
          class="px-3 py-1 text-xs font-medium rounded-md transition-all"
          :class="activePeriod === p.value
            ? 'bg-white dark:bg-gray-700 shadow text-gray-900 dark:text-white'
            : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'"
          @click="changePeriod(p.value)"
        >
          {{ p.label }}
        </button>
      </div>
    </div>

    <!-- Legend -->
    <div class="flex gap-4">
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-emerald-500" />
        <span class="text-xs text-gray-500">Kiruvchi</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-rose-500" />
        <span class="text-xs text-gray-500">Chiquvchi</span>
      </div>
    </div>

    <!-- Chart -->
    <div class="relative" style="height: 260px">
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin text-2xl text-gray-400" />
      </div>
      <canvas v-show="!loading" ref="canvasRef" />
    </div>

    <!-- Summary -->
    <div class="grid grid-cols-2 gap-3 pt-2 border-t border-gray-100 dark:border-gray-800">
      <div class="space-y-0.5">
        <p class="text-xs text-gray-400">Jami kiruvchi</p>
        <p class="font-semibold text-emerald-600">
          +{{ formatAmount(totalIncome) }} so'm
        </p>
      </div>
      <div class="space-y-0.5">
        <p class="text-xs text-gray-400">Jami chiquvchi</p>
        <p class="font-semibold text-rose-500">
          -{{ formatAmount(totalOutcome) }} so'm
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip,
  Legend
);

interface StatPoint {
  label: string;
  income: number;
  outcome: number;
}

const periods = [
  { value: "daily",   label: "Kunlik" },
  { value: "weekly",  label: "Haftalik" },
  { value: "monthly", label: "Oylik" },
  { value: "yearly",  label: "Yillik" },
];

const activePeriod = ref("monthly");
const loading = ref(false);
const chartData = ref<StatPoint[]>([]);
const canvasRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const totalIncome  = computed(() => chartData.value.reduce((s, d) => s + d.income, 0));
const totalOutcome = computed(() => chartData.value.reduce((s, d) => s + d.outcome, 0));

function formatAmount(val: number) {
  return val.toLocaleString("uz-UZ");
}

async function fetchStats(period: string) {
  loading.value = true;
  try {
    const { data } = await useNuxtApp().$api.get(`/wallet/stats/?period=${period}`);
    chartData.value = data.data as StatPoint[];
    renderChart();
  } catch {
    chartData.value = [];
  } finally {
    loading.value = false;
  }
}

function changePeriod(period: string) {
  activePeriod.value = period;
  fetchStats(period);
}

function getColor(hex: string, alpha: number) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function renderChart() {
  if (!canvasRef.value) return;

  const labels  = chartData.value.map(d => d.label);
  const incomes  = chartData.value.map(d => d.income);
  const outcomes = chartData.value.map(d => d.outcome);

  if (chartInstance) {
    chartInstance.data.labels = labels;
    chartInstance.data.datasets[0].data = incomes;
    chartInstance.data.datasets[1].data = outcomes;
    chartInstance.update();
    return;
  }

  chartInstance = new Chart(canvasRef.value, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Kiruvchi",
          data: incomes,
          borderColor: "#10b981",
          backgroundColor: getColor("#10b981", 0.1),
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#10b981",
        },
        {
          label: "Chiquvchi",
          data: outcomes,
          borderColor: "#f43f5e",
          backgroundColor: getColor("#f43f5e", 0.1),
          fill: true,
          tension: 0.4,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#f43f5e",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) =>
              ` ${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString("uz-UZ")} so'm`,
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11 }, maxRotation: 0 },
        },
        y: {
          grid: { color: "rgba(156,163,175,0.15)" },
          ticks: {
            font: { size: 11 },
            callback: (val) => Number(val).toLocaleString("uz-UZ"),
          },
        },
      },
    },
  });
}

onMounted(() => fetchStats(activePeriod.value));
onUnmounted(() => chartInstance?.destroy());
</script>
