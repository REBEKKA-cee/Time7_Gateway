from __future__ import annotations

from typing import Dict, Tuple


MOCK_IAS_DB: Dict[str, str] = {
    "90127838712": "Nike Air Max 90",
    "76834512904": "Adidas Ultraboost 22",
    "55201983746": "Puma Suede Classic",
    "83467021955": "New Balance 990v6",
    "19628403751": "Converse Chuck 70",
}


def mock_ias_lookup(tag_id: str) -> Tuple[bool, str]:

    key = str(tag_id).strip()
    if not key:
        return False, "Invalid tag"

    info = MOCK_IAS_DB.get(key)
    if info is not None:
        return True, info

    return False, "Invalid tag"