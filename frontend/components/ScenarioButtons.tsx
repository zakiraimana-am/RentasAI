"use client";

import type { AppMode } from "@/lib/api";

const scenarios = [
  ["normal_route", "Normal Route"],
  ["heavy_rain_bus_delay", "Heavy Rain + Bus Delay"],
  ["flash_flood_risk", "Flash Flood Risk"],
  ["feeder_bus_delay", "Feeder Bus Delay"],
  ["road_congestion", "Road Congestion"]
] as const;

export function ScenarioButtons({
  mode,
  scenario,
  onScenarioChange
}: {
  mode: AppMode;
  scenario: string;
  onScenarioChange: (scenario: string) => void;
}) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-600">Scenario</h2>
        {mode === "live" ? <span className="text-xs text-slate-500">Live mode uses current API data. Simulation trigger is disabled or treated as test overlay.</span> : null}
      </div>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 xl:grid-cols-5">
        {scenarios.map(([id, label]) => (
          <button
            key={id}
            type="button"
            disabled={mode === "live"}
            onClick={() => onScenarioChange(id)}
            className={`rounded-md border px-3 py-2 text-left text-sm transition ${
              scenario === id ? "border-rail bg-mint font-semibold text-ink" : "border-slate-200 bg-white text-slate-700 hover:border-rail"
            } disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-400`}
          >
            {label}
          </button>
        ))}
      </div>
    </section>
  );
}
