import { useSettingsStore } from "~/store/useSettings";
import { useUserStore } from "~/store/useUser";
import uz from "../../i18n/locales/uz.json";
import ru from "../../i18n/locales/ru.json";
import en from "../../i18n/locales/en.json";

export default defineNuxtPlugin(async (nuxtApp) => {
  const settings = useSettingsStore();
  const userStore = useUserStore();
  const appConfig = useAppConfig();

  // User ma'lumotlarini localStorage dan tiklash
  userStore.restoreUser();

  // 1. localStorage dan o'qi
  settings.hydrate();

  // 2. Rangni apply qil
  appConfig.ui.colors.primary = settings.primaryColor;

  // 3. Messagesni to'g'ridan-to'g'ri set qil
  const i18n = nuxtApp.$i18n as {
    setLocaleMessage: (locale: string, messages: object) => void;
    setLocale: (locale: string) => Promise<void>;
  };

  i18n.setLocaleMessage("uz", uz);
  i18n.setLocaleMessage("ru", ru);
  i18n.setLocaleMessage("en", en);

  // 4. Saqlangan tilni set qil
  await i18n.setLocale(settings.locale);
});
