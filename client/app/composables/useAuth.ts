// import { error } from "#build/ui";
import axios from "axios";
import { authService } from "~/services/auth.services";
import type { IUser } from "~/types";

const loading = ref<boolean>(false);
const data = ref<null | IUser>(null);

export default function useAuth() {

  async function login(identifier: string, password: string) {
    loading.value = true;
    try {
      const response = await authService.login({
        user_input: identifier,
        password: password,
      });
      // console.log(response);
      data.value = response.data.data.user;

      const accessToken = useCookie("access_token");
      const refreshToken = useCookie("refresh_token");
      const verifyToken = useCookie("verify_token");
      const update_token = useCookie("update_token");

      update_token.value = null;
      verifyToken.value = null;

      accessToken.value = response.data.data.token.access_token;
      refreshToken.value = response.data.data.token.refresh_token;

      return {
        success: response.data.success,
        message: response.data.message,
      };
    } catch (err: unknown) {
      let message = "xatolik yuzaga keldi";

      if (axios.isAxiosError(err)) {
        message =
          err.response?.data?.message ||
          err.response?.data?.detail ||
          err.response?.data?.non_field_errors[0];
      }

      return {
        success: false,
        message: message,
      };
    } finally {
      loading.value = false;
    }
  }

  async function logout(){
    try {
      
    } catch (error) {
      
    }
  }

  return { data, loading, login };
}
