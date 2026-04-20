import { defineStore } from "pinia";
import type { IUser } from "~/types";

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
        this.user = userData
    },

    clearUser(){
        this.user = null
    }
  },
});
