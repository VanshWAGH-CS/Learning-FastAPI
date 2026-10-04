from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

try:
    from ..db import contract_collection
    contract_collections = contract_collection
except ImportError:
    try:
        from ..db import db

        contract_collections = db["contracts"]
    except Exception:
        contract_collections = None

router = APIRouter(prefix="/analysis", tags=["analysis"])


def _normalize_status(value: Any) -> str:
    if value is None:
        return "unknown"
    return str(value).strip().lower()


def _safe_number(value: Any) -> float:
    try:
        if value in (None, "", " "):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


@router.get("/contracts")
async def analyze_contracts(
    status: str | None = Query(default=None, description="Filter by contract status"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
):
    if contract_collections is None:
        raise HTTPException(
            status_code=500,
            detail="Contract collection is not configured in app.db",
        )

    try:
        filters: Dict[str, Any] = {}
        if status:
            filters["status"] = {"$regex": f"^{status}$", "$options": "i"}

        total_contracts = contract_collections.count_documents(filters)
        contracts = list(
            contract_collections.find(filters)
            .skip((page - 1) * limit)
            .limit(limit)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while fetching contracts: {str(exc)}",
        )

    analyzed_contracts: List[Dict[str, Any]] = []
    total_value = 0.0
    status_breakdown: Dict[str, int] = {}
    active_contracts = 0
    expired_contracts = 0

    for contract in contracts:
        contract_id = str(contract.get("_id"))
        contract_status = _normalize_status(contract.get("status"))
        value = _safe_number(contract.get("value"))
        total_value += value

        if contract_status in {"active", "approved", "signed", "in_force", "valid"}:
            active_contracts += 1
        if contract_status in {"expired", "cancelled", "closed", "rejected"}:
            expired_contracts += 1

        status_breakdown[contract_status] = status_breakdown.get(contract_status, 0) + 1

        analyzed_contracts.append(
            {
                "id": contract_id,
                "title": contract.get("title") or contract.get("name") or "Untitled Contract",
                "status": contract.get("status") or "unknown",
                "value": value,
                "party": contract.get("party") or contract.get("client") or "N/A",
                "start_date": contract.get("start_date"),
                "end_date": contract.get("end_date"),
            }
        )

    return {
        "page": page,
        "limit": limit,
        "total_contracts": total_contracts,
        "total_value": round(total_value, 2),
        "active_contracts": active_contracts,
        "expired_contracts": expired_contracts,
        "status_breakdown": status_breakdown,
        "contracts": analyzed_contracts,
    }


@router.get("/contract/{contract_id}")
async def analyze_single_contract(contract_id: str):
    if contract_collections is None:
        raise HTTPException(
            status_code=500,
            detail="Contract collection is not configured in app.db",
        )

    try:
        contract = contract_collections.find_one({"_id": contract_id})
        if not contract:
            contract = contract_collections.find_one({"_id": contract_id})
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while fetching contract: {str(exc)}",
        )

    status_name = _normalize_status(contract.get("status"))
    value = _safe_number(contract.get("value"))

    return {
        "id": str(contract.get("_id")),
        "title": contract.get("title") or contract.get("name") or "Untitled Contract",
        "status": contract.get("status") or "unknown",
        "value": value,
        "party": contract.get("party") or contract.get("client") or "N/A",
        "summary": {
            "is_active": status_name in {"active", "approved", "signed", "in_force", "valid"},
            "is_expired": status_name in {"expired", "cancelled", "closed", "rejected"},
            "risk_level": "low" if status_name in {"active", "approved", "signed"} else "medium",
        },
        "raw": contract,
    }


@router.get("/summary")
async def analysis_summary():
    if contract_collections is None:
        raise HTTPException(
            status_code=500,
            detail="Contract collection is not configured in app.db",
        )

    try:
        contracts = list(contract_collections.find({}))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error while calculating summary: {str(exc)}",
        )

    if not contracts:
        return {
            "total_contracts": 0,
            "total_value": 0.0,
            "average_value": 0.0,
            "status_breakdown": {},
        }

    total_value = sum(_safe_number(contract.get("value")) for contract in contracts)
    status_breakdown: Dict[str, int] = {}

    for contract in contracts:
        status_name = _normalize_status(contract.get("status"))
        status_breakdown[status_name] = status_breakdown.get(status_name, 0) + 1

    return {
        "total_contracts": len(contracts),
        "total_value": round(total_value, 2),
        "average_value": round(total_value / len(contracts), 2),
        "status_breakdown": status_breakdown,
    }


__all__ = ["router"]
