import axios from "axios";

export default defineNuxtPlugin(() => {
  const verify = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    headers: {
      "Content-Type": "application/json",
    },
  });

  verify.interceptors.request.use((config) => {
    const token = useCookie("verify_token");

    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`;
    }

    return config;
  });

  return {
    provide: {
      verify,
    },
  };
});
