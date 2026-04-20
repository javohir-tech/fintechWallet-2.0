import axios from "axios";

export default defineNuxtPlugin(() => {
  const api = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    headers: {
      "Content-Type": "application/json",
    },
  });

  api.interceptors.request.use((config) => {
    const token = useCookie("access_token", { default: () => null });

    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`;
    }

    return config;
  });

  // RESPONSE interceptor
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const access_token = useCookie("access_token");
      const refresh_token = useCookie("refresh_token");

      if (error.response?.status === 401 && refresh_token.value) {
        try {
          const { data } = await axios.post(
            `${useRuntimeConfig().public.apiBase}/auth/refresh/`,
            {
              refresh: refresh_token.value,
            },
          );

          access_token.value = data.access;

          error.config.headers.Authorization = `Bearer ${access_token.value}`;
          return api.request(error.config);
        } catch (error) {
          access_token.value = null;
          refresh_token.value = null;
          return navigateTo("/auth/login/");
        }
      }

      return Promise.reject(error);
    },
  );

  return {
    provide: {
      api,
    },
  };
});
