from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

import asyncpg

from app.config import get_settings


async def database_status() -> str:
    try:
        conn = await asyncpg.connect(get_settings().database_url, timeout=1.5)
        await conn.execute("select 1")
        await conn.close()
        return "ok"
    except Exception:
        return "error"


async def persist_trip_result(result: dict[str, Any]) -> str | None:
    try:
        conn = await asyncpg.connect(get_settings().database_url, timeout=1.5)
    except Exception:
        return None

    trip = result["trip"]
    trip_id = str(uuid4())
    try:
        async with conn.transaction():
            await conn.execute(
                """
                insert into trips (id, origin, destination, arrival_deadline, preference, scenario, mode)
                values ($1, $2, $3, $4, $5, $6, $7)
                """,
                trip_id,
                trip["origin"],
                trip["destination"],
                trip["arrival_deadline"],
                trip["preference"],
                trip["scenario"],
                result["mode"],
            )
            for trace in result.get("agent_trace", []):
                await conn.execute(
                    """
                    insert into agent_runs (id, trip_id, agent_name, input_data, output_data, data_source)
                    values ($1, $2, $3, $4::jsonb, $5::jsonb, $6)
                    """,
                    str(uuid4()),
                    trip_id,
                    trace.get("agent"),
                    "{}",
                    json.dumps(trace),
                    trace.get("data_source", "unknown"),
                )
            for route in result.get("route_options", []):
                await conn.execute(
                    """
                    insert into route_options
                    (id, trip_id, route_name, estimated_arrival, delay_saved_minutes, cost_level, walking_minutes,
                     risk_level, score, safety_status, route_geometry)
                    values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::jsonb)
                    """,
                    str(uuid4()),
                    trip_id,
                    route.get("name"),
                    route.get("estimated_arrival"),
                    route.get("delay_saved_minutes"),
                    route.get("cost_level"),
                    route.get("walking_minutes"),
                    route.get("risk_level"),
                    route.get("score"),
                    route.get("safety_status"),
                    json.dumps(route.get("geometry")),
                )
            rec = result.get("recommendation", {})
            await conn.execute(
                """
                insert into recommendations
                (id, trip_id, selected_route_name, user_message, reason, backup_option, confidence, data_note)
                values ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                str(uuid4()),
                trip_id,
                rec.get("selected_route", {}).get("name"),
                rec.get("explanation", {}).get("user_message"),
                rec.get("explanation", {}).get("reason"),
                rec.get("explanation", {}).get("backup_option"),
                rec.get("explanation", {}).get("confidence"),
                rec.get("explanation", {}).get("data_note"),
            )
            op = result.get("operator_impact", {})
            await conn.execute(
                """
                insert into operator_events
                (id, trip_id, affected_area, severity, affected_users_estimate, recommended_action, event_data)
                values ($1, $2, $3, $4, $5, $6, $7::jsonb)
                """,
                str(uuid4()),
                trip_id,
                op.get("affected_area"),
                op.get("severity"),
                op.get("affected_users_estimate"),
                op.get("recommended_action"),
                json.dumps(op),
            )
            for source, status in result.get("api_health", {}).items():
                if isinstance(status, dict):
                    await conn.execute(
                        """
                        insert into api_snapshots (id, source_name, status, api_response, error_message)
                        values ($1, $2, $3, $4::jsonb, $5)
                        """,
                        str(uuid4()),
                        source,
                        status.get("status"),
                        json.dumps(status),
                        status.get("message"),
                    )
    except Exception:
        return None
    finally:
        try:
            await conn.close()
        except Exception:
            pass
    return trip_id
