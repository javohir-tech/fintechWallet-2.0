export const authService = {
  login(data: { user_input: string; password: string }) {
    return useNuxtApp().$api.post("/auth/login/", data);
  },

  register(data: { email_or_number: string }) {
    return useNuxtApp().$api.post("/auth/signup/", data);
  },

  verify(data: { code: string }) {
    return useNuxtApp().$verify.post("/auth/verify/", data);
  },

  updateVerify(){
    return useNuxtApp().$verify.post("/auth/update_verify/")
  }
};
