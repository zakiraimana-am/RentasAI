create extension if not exists "uuid-ossp";

create table if not exists trips (
    id uuid primary key,
    origin text not null,
    destination text not null,
    arrival_deadline text not null,
    preference text not null,
    scenario text not null,
    mode text not null,
    created_at timestamptz not null default now()
);

create table if not exists agent_runs (
    id uuid primary key,
    trip_id uuid references trips(id) on delete cascade,
    agent_name text not null,
    input_data jsonb not null default '{}'::jsonb,
    output_data jsonb not null default '{}'::jsonb,
    data_source text,
    created_at timestamptz not null default now()
);

create table if not exists route_options (
    id uuid primary key,
    trip_id uuid references trips(id) on delete cascade,
    route_name text not null,
    estimated_arrival text,
    delay_saved_minutes integer,
    cost_level text,
    walking_minutes integer,
    risk_level text,
    score numeric,
    safety_status text,
    route_geometry jsonb,
    created_at timestamptz not null default now()
);

create table if not exists recommendations (
    id uuid primary key,
    trip_id uuid references trips(id) on delete cascade,
    selected_route_name text,
    user_message text,
    reason text,
    backup_option text,
    confidence text,
    data_note text,
    created_at timestamptz not null default now()
);

create table if not exists operator_events (
    id uuid primary key,
    trip_id uuid references trips(id) on delete cascade,
    affected_area text,
    severity text,
    affected_users_estimate integer,
    recommended_action text,
    event_data jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists api_snapshots (
    id uuid primary key,
    source_name text not null,
    status text not null,
    api_response jsonb not null default '{}'::jsonb,
    error_message text,
    created_at timestamptz not null default now()
);

create table if not exists cached_gtfs_stops (
    id uuid primary key,
    stop_id text,
    stop_name text,
    lat numeric,
    lon numeric,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);

create table if not exists cached_gtfs_routes (
    id uuid primary key,
    route_id text,
    route_name text,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now()
);
