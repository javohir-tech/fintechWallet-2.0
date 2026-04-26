export const Transactionservices = {
    balance(){
        return useNuxtApp().$api.get("/wallet/me/")
    }
}