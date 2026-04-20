// import { error } from "#build/ui";
import axios from "axios";
import { authService } from "~/services/auth.services";
import { useUserStore } from "~/store/useUser";
import { normalizeUser } from "~/utils/mappers/user.mapper";

export default function useAuth() {
  const loading = ref<boolean>(false);
  const userStore = useUserStore();

  async function login(identifier: string, password: string) {
    loading.value = true;
    try {
      const response = await authService.login({
        user_input: identifier,
        password: password,
      });
      // console.log(response);
      const user = normalizeUser(response.data.user);
      userStore.setUser(user);
      const accessToken = useCookie("access_token");
      const refreshToken = useCookie("refresh_token");
      const verifyToken = useCookie("verify_token");
      const update_token = useCookie("update_token");

      update_token.value = null;
      verifyToken.value = null;

      accessToken.value = response.data.token.access_token;
      refreshToken.value = response.data.token.refresh_token;

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

  async function logout() {
    try {
      const refresh_token = useCookie("refresh_token");
      const access_token = useCookie("access_token");
      if (typeof refresh_token.value === "string") {
        const { data } = await authService.logout({
          refresh_token: refresh_token.value,
        });
        // console.log(data);
        refresh_token.value = null;
        access_token.value = null;
        userStore.clearUser()
        await navigateTo({ path: "/auth/login/", query: data.message });
      }
    } catch (error: unknown) {
      let message = "hatolik yuzz  berdi";
      if (axios.isAxiosError(error)) {
        console.log(error.response);
        message = error.response?.data?.detail || error.response?.data?.refresh;
      }
      return message;
    }
  }

  return { loading, login, logout };
}
