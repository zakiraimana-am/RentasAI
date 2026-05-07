"use client";

import { ShieldCheck } from "lucide-react";

export function RecommendationCard({ recommendation, loading }: { recommendation?: any; loading?: boolean }) {
  const route = recommendation?.selected_route;
  const explanation = recommendation?.explanation;
  if (!route) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <p className="font-semibold text-ink">{loading ? "Planning recommendation..." : "No recommendation loaded yet."}</p>
        <p className="mt-1 text-sm text-slate-600">Simulation and hybrid modes are designed to return a full recommendation even when optional services fail.</p>
      </section>
    );
  }
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-start gap-3">
        <ShieldCheck className="mt-1 h-5 w-5 text-emerald-700" aria-hidden />
        <div>
          <h2 className="text-lg font-bold text-ink">{route.name}</h2>
          <p className="text-sm text-slate-600">{explanation?.user_message}</p>
          {loading ? <p className="mt-1 text-xs font-medium text-rail">Refreshing recommendation...</p> : null}
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm sm:grid-cols-3">
        <Metric label="Arrival" value={route.estimated_arrival} />
        <Metric label="Delay saved" value={`${route.delay_saved_minutes} min`} />
        <Metric label="Walking" value={`${route.walking_minutes} min`} />
        <Metric label="Cost" value={route.cost_level} />
        <Metric label="Risk" value={route.risk_level} />
        <Metric label="Safety" value={route.safety_status} />
      </div>
      <div className="mt-4 space-y-2 text-sm text-slate-700">
        <p><strong>Reason:</strong> {explanation?.reason}</p>
        <p><strong>Backup:</strong> {explanation?.backup_option}</p>
        <p><strong>Confidence:</strong> {explanation?.confidence}</p>
        <p><strong>Data note:</strong> {explanation?.data_note}</p>
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value?: string }) {
  return (
    <div className="rounded-md bg-slate-50 p-3">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="font-semibold text-ink">{value ?? "-"}</p>
    </div>
  );
}
