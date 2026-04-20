import type { IUser } from "~/types";

export function normalizeUser(data: any): IUser {
  return {
    id: data.id ?? "",
    username: data.username ?? "",
    email: data.email ?? "",
    phone_number: data.phone_number ?? "",
    avatar: data.avatar ?? "",
    auth_status: data.auth_status ?? "new",
    auth_type: data.auth_type ?? "via_email",
  };
}
