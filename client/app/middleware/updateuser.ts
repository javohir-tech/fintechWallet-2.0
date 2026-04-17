export default defineNuxtRouteMiddleware((to) => {
  const update_token = useCookie("update_token");

  if (
    !update_token.value &&
    (to.path === "/auth/updateuser" || to.path === "/auth/updateuser/")
  ) {
    return "/auth/login";
  }
});
