import axios from "axios";
import type { IUser } from "~/types";

const loading = ref<boolean>(false);
const data = ref<null | IUser>(null);

export default function useAuth() {
  async function login(apiUrl: string, identifier: string, password: string) {
    loading.value = true;
    try {
      const response = await axios.post(apiUrl, {
        user_input: identifier,
        password: password,
      });
      console.log(response);
      data.value = response.data.data.user;

      const accessToken = useCookie("access_token");
      const refreshToken = useCookie("refresh_token");

      accessToken.value = response.data.data.token.access_token;
      refreshToken.value = response.data.data.token.refresh_token;

      return {
        success: response.data.success,
        message: response.data.message,
      };
    } catch (err: any) {
      const message =
        err.response?.data?.message ??
        err.response?.data?.detail ??
        err.response?.data?.non_field_errors[0] ??
        "xatolik yuzaga keldi";

      return {
        success: false,
        message: message,
      };
    } finally {
      loading.value = false;
    }
  }

  return { data, loading, login };
}
