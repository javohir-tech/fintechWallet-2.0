import axios from "axios";

export default defineNuxtPlugin(() => {
  const updateuser = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    headers: {
      "Content-Type": "application/json",
    },
  });

  updateuser.interceptors.request.use((config) => {
    const token = useCookie("update_token");

    if (token.value) {
      config.headers.Authorization = `Bearer ${token.value}`;
    }

    return config;
  });

  return {
    provide: {
      updateuser,
    },
  };
});
