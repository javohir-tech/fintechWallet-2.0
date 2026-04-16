export default defineNuxtRouteMiddleware((to) => {
  const verifyToken = useCookie("verify_token")

  if (!verifyToken.value && to.path === "/auth/verify") {
    return navigateTo("/")
  }
})