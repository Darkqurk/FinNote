import { useEffect, useState } from "react";
import { fetchHoldings, fetchSummary } from "../api";
import type { Holding } from "../api"; // 이렇게 분리해서 import

export default function HoldingsTable() {
  const [rows, setRows] = useState<Holding[]>([]);
  const [sum, setSum] = useState<{ total_market_value: number; total_pnl: number } | null>(null);

  useEffect(() => {
    fetchHoldings().then(setRows);
    fetchSummary().then(setSum);
  }, []);

  return (
    <div>
      <h1>Pinnote 대시보드</h1>
      {sum && (
        <div>
          <div>총 평가금액: {sum.total_market_value.toLocaleString()}</div>
          <div>총 손익: {sum.total_pnl.toLocaleString()}</div>
        </div>
      )}
      <table>
        <thead>
          <tr>
            <th>티커</th>
            <th>수량</th>
            <th>평단가</th>
            <th>현재가</th>
            <th>평가금액</th>
            <th>손익</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.stock.ticker}</td>
              <td>{r.quantity}</td>
              <td>{r.avg_cost}</td>
              <td>{r.last_close}</td>
              <td>{r.market_value}</td>
              <td>{r.pnl}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
