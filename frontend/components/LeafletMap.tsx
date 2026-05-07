"use client";

import { useEffect, useMemo } from "react";
import { MapContainer, TileLayer, Polyline, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

type Props = {
  geometry?: GeoJSON.LineString;
  selectedRoute?: any;
  mode: string;
  scenario: string;
};

const origin: [number, number] = [3.2058, 101.7317];
const destination: [number, number] = [3.1342, 101.6861];
const disruption: [number, number] = [3.2101, 101.7296];

const originIcon = L.divIcon({
  className: "custom-marker",
  html: '<div style="width: 16px; height: 16px; border-radius: 999px; background: #245f73; border: 2px solid white; box-shadow: 0 1px 6px rgba(0,0,0,.25);"></div>',
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

const destinationIcon = L.divIcon({
  className: "custom-marker",
  html: '<div style="width: 16px; height: 16px; border-radius: 999px; background: #c94c4c; border: 2px solid white; box-shadow: 0 1px 6px rgba(0,0,0,.25);"></div>',
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

const disruptionIcon = L.divIcon({
  className: "custom-marker",
  html: '<div style="width: 16px; height: 16px; border-radius: 999px; background: #e0a73f; border: 2px solid white; box-shadow: 0 1px 6px rgba(0,0,0,.25);"></div>',
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

function MapUpdater({ geometry, mode, scenario }: { geometry?: GeoJSON.LineString; mode: string; scenario: string }) {
  const map = useMap();

  useEffect(() => {
    if (geometry && geometry.coordinates.length > 0) {
      const latLngs: [number, number][] = geometry.coordinates.map(
        (coord) => [coord[1], coord[0]] as [number, number]
      );
      const bounds = L.latLngBounds(latLngs);
      map.fitBounds(bounds, { padding: [64, 64], duration: 0.6 });
    }
  }, [geometry, map]);

  return null;
}

function RiskOverlay({ mode, scenario }: { mode: string; scenario: string }) {
  const shouldShow = mode !== "live" && ["heavy_rain_bus_delay", "flash_flood_risk"].includes(scenario);

  if (!shouldShow) return null;

  const riskArea: [number, number][] = [
    [3.214, 101.724],
    [3.206, 101.740],
    [3.192, 101.734],
    [3.198, 101.716],
    [3.214, 101.724],
  ];

  return <Polyline positions={riskArea} pathOptions={{ color: "#e0a73f", fillColor: "#e0a73f", fillOpacity: 0.22, weight: 0 }} />;
}

export function LeafletMap({ geometry, selectedRoute, mode, scenario }: Props) {
  const routeCoordinates = useMemo(() => {
    if (!geometry || !geometry.coordinates) return [];
    return geometry.coordinates.map((coord) => [coord[1], coord[0]] as [number, number]);
  }, [geometry]);

  return (
    <section className="overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
        <div>
          <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-600">Klang Valley Recovery Map</h2>
          <p className="text-sm text-slate-600">{selectedRoute?.name ?? "Recommended route"}</p>
        </div>
        <span className="rounded bg-mint px-2 py-1 text-xs font-semibold text-ink">{mode}</span>
      </div>
      <div className="h-[440px] w-full">
        <MapContainer
          center={[3.171, 101.707]}
          zoom={12}
          style={{ height: "100%", width: "100%" }}
          zoomControl={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {routeCoordinates.length > 0 && (
            <Polyline
              positions={routeCoordinates}
              pathOptions={{ color: "#245f73", weight: 6, opacity: 0.9 }}
            />
          )}

          <Marker position={origin} icon={originIcon}>
            <Popup>Origin: Wangsa Maju</Popup>
          </Marker>

          <Marker position={destination} icon={destinationIcon}>
            <Popup>Destination: KL Sentral</Popup>
          </Marker>

          <Marker position={disruption} icon={disruptionIcon}>
            <Popup>Disruption: feeder delay / rain risk</Popup>
          </Marker>

          <RiskOverlay mode={mode} scenario={scenario} />

          <MapUpdater geometry={geometry} mode={mode} scenario={scenario} />
        </MapContainer>
      </div>
    </section>
  );
}
