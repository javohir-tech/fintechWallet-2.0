import axios from "axios";
import type { IUser } from "~/types";

export default function useAuth() {
  const data = ref<null | IUser>(null);
  const loading = ref<boolean>(false);
  const error = ref<null | Error>(null);

  const toast = useToast();

  async function login(apiUrl: string, identifier: string, password: string) {
    loading.value = true;
    try {
      const response = await axios.post(apiUrl, {
        user_input: identifier,
        password: password,
      });
      data.value = response.data.data.user;

      toast.add({
        title: "Success",
        description: "Tizimga muvaffaqiyatli kirdingiz",
        color: "secondary",
      });
      
      return true;
    } catch (err) {
      error.value = err as Error;
      return false;
    } finally {
      loading.value = false;
    }
  }

  return { data, loading, error, login };
}
