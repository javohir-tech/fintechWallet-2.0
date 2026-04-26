export interface IBalance {
  id: string;
  balance: string;
  currency: string;
  is_active: boolean;
  updated_time: string;
  card: {
    card_number: string;
    card_holder_name: string;
    card_type: string;
    expiry_month: number;
    expiry_year: number;
  };
}
