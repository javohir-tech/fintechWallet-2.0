import axios, { type AxiosError } from "axios";
import { Transactionservices } from "~/services/transaction.services";

export default function useTransaction<T>() {
  const data = ref<T | null>(null);
  const loading = ref<boolean>(false);
  const error = ref<AxiosError | null>(null);

  async function LookCard(card_number: string){
    loading.value = true;
    try {
      const response = await Transactionservices.lookCard({
        card_number: card_number,
      });
      data.value = response.data as T;
      console.log(response);

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

  function reset(){
    data.value = null
    error.value = null
  }

  return { data, loading, error, LookCard  , reset};
}
