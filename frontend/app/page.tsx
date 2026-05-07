"use client";

import { useEffect, useMemo, useState } from "react";
import { RefreshCcw } from "lucide-react";
import { AgentReasoningPanel } from "@/components/AgentReasoningPanel";
import { ApiStatusPanel } from "@/components/ApiStatusPanel";
import dynamic from "next/dynamic";

const LeafletMap = dynamic(() => import("@/components/LeafletMap").then((mod) => mod.LeafletMap), {
  ssr: false,
});
import { OperatorDashboard } from "@/components/OperatorDashboard";
import { RecommendationCard } from "@/components/RecommendationCard";
import { ScenarioButtons } from "@/components/ScenarioButtons";
import { TripPanel } from "@/components/TripPanel";
import { AppMode, Preference, planTrip } from "@/lib/api";

export default function Home() {
  const [mode, setMode] = useState<AppMode>("hybrid");
  const [preference, setPreference] = useState<Preference>("rain_safe");
  const [scenario, setScenario] = useState("heavy_rain_bus_delay");
  const [result, setResult] = useState<any>();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [refreshNonce, setRefreshNonce] = useState(0);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);

  const tripInput = useMemo(
    () => ({
      origin: "Wangsa Maju",
      destination: "KL Sentral",
      arrival_deadline: "08:45",
      preference,
      scenario,
      mode
    }),
    [mode, preference, scenario]
  );

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    planTrip(tripInput)
      .then((data) => {
        if (!cancelled) {
          setResult(data);
          setLastUpdated(new Date().toLocaleTimeString());
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(`${err.message}. Check that the FastAPI backend is running; the app will keep showing the last successful plan if one exists.`);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [tripInput, refreshNonce]);

  return (
    <main className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-2 px-4 py-5 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold tracking-normal text-ink">RentasAI</h1>
              <p className="text-sm text-slate-600">Live-ready agentic mobility recovery for Malaysian commuters.</p>
            </div>
            <button
              type="button"
              onClick={() => {
                setResult(undefined);
                setRefreshNonce((value) => value + 1);
              }}
              className="inline-flex items-center gap-2 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-ink hover:border-rail"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden />
              Refresh
            </button>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-sm">
            {loading ? <span className="text-rail">Planning with deterministic agents...</span> : null}
            {lastUpdated ? <span className="text-slate-500">Last successful plan: {lastUpdated}</span> : null}
            {error ? <span className="rounded-md border border-red-200 bg-red-50 px-2 py-1 text-danger">{error}</span> : null}
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-4 px-4 py-5 sm:px-6 lg:grid-cols-[360px_1fr] lg:px-8">
        <aside className="space-y-4">
          <TripPanel mode={mode} preference={preference} onModeChange={setMode} onPreferenceChange={setPreference} />
          <ApiStatusPanel apiHealth={result?.api_health} mode={mode} effectiveMode={result?.effective_mode} persistence={result?.persistence} />
          <OperatorDashboard operatorImpact={result?.operator_impact} />
        </aside>
        <section className="space-y-4">
          <ScenarioButtons mode={mode} scenario={scenario} onScenarioChange={setScenario} />
          <LeafletMap
            geometry={result?.map_geometry}
            selectedRoute={result?.recommendation?.selected_route}
            mode={mode}
            scenario={scenario}
          />
          <RecommendationCard recommendation={result?.recommendation} loading={loading} />
          <AgentReasoningPanel trace={result?.agent_trace} />
        </section>
      </div>
    </main>
  );
}
