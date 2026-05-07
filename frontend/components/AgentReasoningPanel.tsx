"use client";

export function AgentReasoningPanel({ trace }: { trace?: any[] }) {
  if (!trace?.length) {
    return (
      <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-600">Agent Reasoning</h2>
        <p className="text-sm text-slate-600">Agent trace will appear after the first successful plan.</p>
      </section>
    );
  }
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-600">Agent Reasoning</h2>
      <div className="space-y-3">
        {(trace ?? []).map((item, index) => (
          <article key={`${item.agent}-${index}`} className="rounded-md border border-slate-200 p-3">
            <div className="mb-2 flex items-start justify-between gap-3">
              <div>
                <h3 className="font-semibold text-ink">{item.agent}</h3>
                <p className="text-sm text-slate-600">{item.summary}</p>
              </div>
              <span className="rounded bg-slate-100 px-2 py-1 text-xs font-medium text-slate-700">{item.data_source}</span>
            </div>
            <pre className="max-h-52 overflow-auto rounded bg-slate-950 p-3 text-xs text-slate-100">{JSON.stringify(item.output, null, 2)}</pre>
          </article>
        ))}
      </div>
    </section>
  );
}
