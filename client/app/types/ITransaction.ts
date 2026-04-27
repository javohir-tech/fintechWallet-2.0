export interface ITransactionUser {
  username: string;
  masked_number: string;
}

export interface ITransaction {
  id: string;
  amount: string;
  status: "PENDING" | "SUCCESS" | "FAILED" | "REVERSED";
  txtype: "TOPUP" | "TRANSFER" | "WITHDRAW";
  fee: string;
  idempotency_key: string;
  description: string;
  metadata: Record<string, unknown>;
  debit_amount: string | null;
  credit_amount: string | null;
  from_user: ITransactionUser | null;
  to_user: ITransactionUser | null;
  direction?: boolean; // true = received, false = sent
}
