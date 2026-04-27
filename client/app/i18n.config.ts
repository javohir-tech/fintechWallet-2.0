import uz from "../i18n/locales/uz.json";
import ru from "../i18n/locales/ru.json";
import en from "../i18n/locales/en.json";

export default () => ({
  legacy: false,
  fallbackLocale: "uz",
  missingWarn: false,
  fallbackWarn: false,
  messages: { uz, ru, en },
});
