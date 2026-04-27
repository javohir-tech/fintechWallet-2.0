export const Transactionservices = {
  balance() {
    return useNuxtApp().$api.get("/wallet/me/");
  },

  lookCard(data: { card_number: string }) {
    return useNuxtApp().$api.post("/card/look/" , data);
  },
};
