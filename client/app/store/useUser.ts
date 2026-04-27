import { defineStore } from "pinia";
import type { IUser } from "~/types";

const USER_KEY = "auth_user";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as IUser | null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    isVerifed: (state) => state.user?.auth_status === "done",
  },

  actions: {
    setUser(userData: IUser) {
      this.user = userData;
      if (import.meta.client) {
        localStorage.setItem(USER_KEY, JSON.stringify(userData));
      }
    },

    restoreUser() {
      if (!import.meta.client) return;
      try {
        const raw = localStorage.getItem(USER_KEY);
        if (raw) this.user = JSON.parse(raw) as IUser;
      } catch {
        //
      }
    },

    clearUser() {
      this.user = null;
      if (import.meta.client) {
        localStorage.removeItem(USER_KEY);
      }
    },
  },
});
