export interface IUser {
  id: string;
  auth_status: "new" | "verifed" | "done" | "photo_done" | "logout";
  username: string;
  avatar: string;
  email: string;
  phone_number: string;
  auth_type: "via_email" | "via_phone";
}
