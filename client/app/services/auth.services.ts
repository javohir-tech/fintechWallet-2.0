import ForgetPassword from "~/pages/auth/forgetPassword.vue";

export const authService = {
  login(data: { user_input: string; password: string }) {
    return useNuxtApp().$api.post("/auth/login/", data);
  },

  register(data: { email_or_number: string }) {
    return useNuxtApp().$api.post("/auth/signup/", data);
  },

  forgetPassword(data: { email_or_number: string }) {
    return useNuxtApp().$api.post("/auth/forget/", data);
  },

  logout(data: { refresh: string }) {
    return useNuxtApp().$api.post("/auth/logout/", data);
  },

  passwordReset(data: { password: string }) {
    return useNuxtApp().$updateuser.post("/auth/password/", data);
  },

  verify(data: { code: string }) {
    return useNuxtApp().$verify.post("/auth/verify/", data);
  },

  updateVerify() {
    return useNuxtApp().$verify.post("/auth/update_verify/");
  },

  updateUser(data: { username: string; password: string }) {
    return useNuxtApp().$updateuser.patch("/auth/update/", data);
  },
};
