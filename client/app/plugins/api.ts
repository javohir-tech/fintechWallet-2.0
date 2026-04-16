import axios from "axios";

export default defineNuxtPlugin(() => {
  const api = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    headers: {
      "Content-Type": "application/json",
    },
  });

  api.interceptors.request.use((config) => {
    const token = useCookie("access_token")

    if(token.value){
        config.headers.Authorization = `Bearer ${token.value}`
    }

    return config
  });

  return {
    provide : {
        api
    }
  }
});
