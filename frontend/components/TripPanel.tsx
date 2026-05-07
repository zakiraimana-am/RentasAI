"use client";

import { MapPin, Timer } from "lucide-react";
import type { AppMode, Preference } from "@/lib/api";
import { ModeSelector } from "./ModeSelector";

type Props = {
  mode: AppMode;
  preference: Preference;
  onModeChange: (mode: AppMode) => void;
  onPreferenceChange: (preference: Preference) => void;
};

export function TripPanel(props: Props) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-4 grid gap-3">
        <div className="flex items-center gap-3">
          <MapPin className="h-5 w-5 text-rail" aria-hidden />
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">Origin</p>
            <p className="font-semibold">Wangsa Maju</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <MapPin className="h-5 w-5 text-danger" aria-hidden />
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">Destination</p>
            <p className="font-semibold">KL Sentral</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Timer className="h-5 w-5 text-amberline" aria-hidden />
          <div>
            <p className="text-xs uppercase tracking-wide text-slate-500">Deadline</p>
            <p className="font-semibold">08:45</p>
          </div>
        </div>
      </div>
      <ModeSelector {...props} />
    </section>
  );
}
