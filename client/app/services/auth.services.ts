export const authService = {
    login(data : {user_input : string , password : string}){
        return useNuxtApp().$api.post("/auth/login/" , data)
    },

    register(data: {email_or_number : string}){
        return  useNuxtApp().$api.post("/auth/signup/" , data)
    }
}