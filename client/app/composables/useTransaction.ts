import axios, { type AxiosError } from "axios";
import { Transactionservices } from "~/services/transaction.services";
import type { ICard } from "~/types";
import { readCache, writeCache } from "~/utils/cache"; 

export default function useTransaction<T extends ICard>() {
  const data = ref<T | null>(null);
  const loading = ref<boolean>(false);
  const error = ref<AxiosError | null>(null);
  const cache = readCache();

  function searchCache(prefix: string): ICard[] {
  const cache = readCache();
  if (!prefix.trim()) return Array.from(cache.values());
  return Array.from(cache.values()).filter((card) =>
    card.card_number.startsWith(prefix),
  );
}

  async function LookCard(card_number: string) {
    if (cache.has(card_number)) {
      data.value = cache.get(card_number) as T;
      return { success: true, message: "topildi" };
    }

    loading.value = true;
    try {
      const response = await Transactionservices.lookCard({
        card_number: card_number,
      });
      data.value = response.data as T;
      console.log(response);
      // ✅ Cache ga saqlash
      cache.set(card_number, data.value);
      writeCache(cache);
      return {
        success: true,
        message: "topildi",
      };
    } catch (err) {
      let message = "Server Error";
      if (axios.isAxiosError(err)) {
        error.value = err as AxiosError<{ message?: string }>;
        message =
          err?.response?.data?.detail ?? err?.response?.data?.card_number?.[0];
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      loading.value = false;
    }
  }


  function selectCard(card: ICard) {
    data.value = card as T;
  }

  function reset() {
    data.value = null;
    error.value = null;
  }

  return { data, loading, error, LookCard, reset, searchCache , selectCard };
}
