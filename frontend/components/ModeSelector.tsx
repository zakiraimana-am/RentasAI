"use client";

import type { AppMode, Preference } from "@/lib/api";

type Props = {
  mode: AppMode;
  preference: Preference;
  onModeChange: (mode: AppMode) => void;
  onPreferenceChange: (preference: Preference) => void;
};

export function ModeSelector({ mode, preference, onModeChange, onPreferenceChange }: Props) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      <label className="text-sm font-medium text-ink">
        Mode
        <select
          className="mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm"
          value={mode}
          onChange={(event) => onModeChange(event.target.value as AppMode)}
        >
          <option value="simulation">simulation</option>
          <option value="live">live</option>
          <option value="hybrid">hybrid</option>
        </select>
      </label>
      <label className="text-sm font-medium text-ink">
        Preference
        <select
          className="mt-1 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm"
          value={preference}
          onChange={(event) => onPreferenceChange(event.target.value as Preference)}
        >
          <option value="balanced">balanced</option>
          <option value="fastest">fastest</option>
          <option value="cheapest">cheapest</option>
          <option value="least_walking">least_walking</option>
          <option value="rain_safe">rain_safe</option>
        </select>
      </label>
    </div>
  );
}
