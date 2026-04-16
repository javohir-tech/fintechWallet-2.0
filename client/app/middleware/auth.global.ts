export default defineNuxtRouteMiddleware((to) => {

  if (import.meta.server) return

  const token = localStorage.getItem("access_token");
  const publicPage = ["/auth/login", "/auth/signup"];
  const isPublic = publicPage.includes(to.path);

  if (token && isPublic) {
    return navigateTo("/");
  }

  if(!token && !isPublic){
    return navigateTo("/auth/login")
  }
});
