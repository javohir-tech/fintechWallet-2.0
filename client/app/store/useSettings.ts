import { defineStore } from "pinia";

export type SidebarSide = "left" | "right";
export type PrimaryColor =
  | "red" | "orange" | "amber" | "yellow" | "lime" | "green"
  | "emerald" | "teal" | "cyan" | "sky" | "blue" | "indigo"
  | "violet" | "purple" | "fuchsia" | "pink" | "rose";

export interface SettingsState {
  primaryColor: PrimaryColor;
  sidebarSide: SidebarSide;
  locale: string;
}

export const STORAGE_KEY = "app_settings";

export const DEFAULTS: SettingsState = {
  primaryColor: "green",
  sidebarSide: "left",
  locale: "uz",
};

export const useSettingsStore = defineStore("settings", {
  state: (): SettingsState => ({ ...DEFAULTS }),

  actions: {
    hydrate() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          const saved = JSON.parse(raw) as Partial<SettingsState>;
          this.primaryColor = saved.primaryColor ?? DEFAULTS.primaryColor;
          this.sidebarSide  = saved.sidebarSide  ?? DEFAULTS.sidebarSide;
          this.locale       = saved.locale        ?? DEFAULTS.locale;
        }
      } catch {
        // localStorage o'qib bo'lmasa defaults qoladi
      }
    },

    setColor(color: PrimaryColor) {
      this.primaryColor = color;
      this._persist();
    },

    setSidebarSide(side: SidebarSide) {
      this.sidebarSide = side;
      this._persist();
    },

    setLocale(locale: string) {
      this.locale = locale;
      this._persist();
    },

    reset() {
      this.primaryColor = DEFAULTS.primaryColor;
      this.sidebarSide  = DEFAULTS.sidebarSide;
      this.locale       = DEFAULTS.locale;
      localStorage.removeItem(STORAGE_KEY);
    },

    _persist() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          primaryColor: this.primaryColor,
          sidebarSide:  this.sidebarSide,
          locale:       this.locale,
        })
      );
    },
  },
});
