import axios, { Axios, type AxiosError } from "axios";
import type {IBalance} from "~/types"
import { Transactionservices } from "~/services/transaction.services";

export default function useBalance<T>() {
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<AxiosError | null>(null);

  async function getBalance() {
    loading.value = true;
    try {
      const response = await Transactionservices.balance();
      data.value = response.data as T
    } catch (err) {
      if (axios.isAxiosError(err)) {
        error.value = err as AxiosError;
      }
    } finally {
      loading.value = false;
    }
  }

  return {data , loading , error , getBalance}
}
