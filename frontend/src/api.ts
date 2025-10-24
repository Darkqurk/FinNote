import axios from "axios";

export const api = axios.create({ baseURL: "http://localhost:8000/api" });

export type Holding = {
  id: number;
  stock: { id: number; ticker: string; name: string };
  quantity: string;
  avg_cost: string;
  last_close: string;
  market_value: string;
  pnl: string;
};

export async function fetchHoldings() {
  const { data } = await api.get("/holdings/");
  return data as Holding[];
}

export async function fetchSummary() {
  const { data } = await api.get("/holdings/summary/");
  return data as { total_market_value: number; total_pnl: number };
}
