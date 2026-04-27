export const Transactionservices = {
  balance() {
    return useNuxtApp().$api.get("/wallet/me/");
  },

  lookCard(data: { card_number: string }) {
    return useNuxtApp().$api.post("/card/look/", data);
  },

  createTransfer(data: {
    wallet_id: string;
    amount: number;
    idempotency_key: string;
  }) {
    return useNuxtApp().$api.post("/transactions/create-transfer/", data);
  },

  getAllTransactions(params?: {
    status?: string;
    txtype?: string;
    direction?: "in" | "out" | "";
  }) {
    return useNuxtApp().$api.get("/transactions/transactions/", { params });
  },

  getTransactionDetail(id: string) {
    return useNuxtApp().$api.get(`/transactions/transactions/${id}/`);
  },
};
