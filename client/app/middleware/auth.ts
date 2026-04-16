export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie("access_token");
  const verifyToken = useCookie("verify_token");

  const publicPage = ["/auth/login", "/auth/signup" , "/auth/verify/"];
  const isPublic = publicPage.includes(to.path);

  const isLoggedIn = !!token.value;

  if (isLoggedIn && isPublic) {
    return navigateTo("/");
  }

  if (!isLoggedIn && !isPublic) {
    return navigateTo("/auth/login");
  }
});
