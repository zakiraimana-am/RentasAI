export type AppMode = "simulation" | "live" | "hybrid";
export type Preference = "balanced" | "fastest" | "cheapest" | "least_walking" | "rain_safe";

export type TripPlanInput = {
  origin: string;
  destination: string;
  arrival_deadline: string;
  preference: Preference;
  scenario: string;
  mode: AppMode;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export async function planTrip(input: TripPlanInput) {
  const response = await fetch(`${API_URL}/trip/plan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(`Trip planning failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchScenarios() {
  const response = await fetch(`${API_URL}/scenarios`, { cache: "no-store" });
  if (!response.ok) return { scenarios: [] };
  return response.json();
}
