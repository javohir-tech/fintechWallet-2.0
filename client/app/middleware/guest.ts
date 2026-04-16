export default defineNuxtRouteMiddleware((to) => {
  const accessToken = useCookie("access_token");

  if (accessToken.value && to.path.startsWith("/auth")) {
    return navigateTo("/");
  }
});
