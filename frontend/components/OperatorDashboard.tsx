"use client";

export function OperatorDashboard({ operatorImpact }: { operatorImpact?: any }) {
  const op = operatorImpact ?? {};
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-600">Operator Dashboard</h2>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <Metric label="Affected area" value={op.affected_area} wide />
        <Metric label="Severity" value={op.severity} />
        <Metric label="Affected users" value={op.affected_users_estimate?.toLocaleString?.() ?? op.affected_users_estimate} />
        <Metric label="Live data used" value={String(Boolean(op.live_data_used))} />
        <Metric label="Fallback used" value={String(Boolean(op.fallback_used))} />
      </div>
      <p className="mt-3 rounded-md bg-slate-50 p-3 text-sm text-slate-700">{op.recommended_action}</p>
    </section>
  );
}

function Metric({ label, value, wide }: { label: string; value?: string; wide?: boolean }) {
  return (
    <div className={`rounded-md border border-slate-100 p-3 ${wide ? "col-span-2" : ""}`}>
      <p className="text-xs text-slate-500">{label}</p>
      <p className="font-semibold text-ink">{value ?? "-"}</p>
    </div>
  );
}
