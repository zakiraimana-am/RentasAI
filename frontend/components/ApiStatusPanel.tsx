"use client";

function statusClass(status: string) {
  if (status === "ok") return "bg-emerald-100 text-emerald-800";
  if (status === "fallback") return "bg-amber-100 text-amber-800";
  if (status === "error") return "bg-red-100 text-red-800";
  return "bg-slate-100 text-slate-700";
}

export function ApiStatusPanel({ apiHealth, mode, effectiveMode, persistence }: { apiHealth?: any; mode: string; effectiveMode?: string; persistence?: any }) {
  const entries = [
    ["GTFS Static", apiHealth?.gtfs_static],
    ["GTFS Realtime", apiHealth?.gtfs_realtime],
    ["Weather API", apiHealth?.weather],
    ["Database", persistence ? { status: persistence.database, message: persistence.message } : undefined],
    ["Data mode", { status: effectiveMode ?? mode, message: `Requested mode: ${mode}${effectiveMode && effectiveMode !== mode ? `; recovered with ${effectiveMode}` : ""}` }],
    ["Overall", { status: apiHealth?.overall_status ?? "not_checked", message: apiHealth?.fallback_used ? "At least one optional live dependency used fallback." : "No fallback reported." }]
  ];
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-600">API Status</h2>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-1">
        {entries.map(([label, detail]) => {
          const status = detail?.status ?? "not_checked";
          return (
          <div key={label} className="rounded-md border border-slate-100 p-3">
            <p className="text-xs text-slate-500">{label}</p>
            <span className={`mt-2 inline-flex rounded px-2 py-1 text-xs font-semibold ${statusClass(status)}`}>{status}</span>
            {detail?.message ? <p className="mt-2 text-xs leading-5 text-slate-600">{detail.message}</p> : null}
          </div>
          );
        })}
      </div>
    </section>
  );
}
