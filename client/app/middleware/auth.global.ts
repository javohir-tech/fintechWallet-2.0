export default defineNuxtRouteMiddleware( (to) => {

  if (import.meta.server) return

  const token = useCookie("access_token")
  const publicPage = ["/auth/login", "/auth/signup"];
  const isPublic = publicPage.includes(to.path);

  const isLoggedIn = !!token.value

  if (isLoggedIn && isPublic) {
    return navigateTo("/");
  }

  if(!isLoggedIn && !isPublic){
    return navigateTo("/auth/login")
  }
});
