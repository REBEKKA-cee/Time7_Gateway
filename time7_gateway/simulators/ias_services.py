from typing import Optional, Tuple


# IAS simulation
MOCK_IAS_DB = {
    "90127838712": "Nike Air Max 90",
    "76834512904": "Adidas Ultraboost 22",
    "55201983746": "Puma Suede Classic",
    "83467021955": "New Balance 990v6",
    "19628403751": "Converse Chuck 70",
}


def mock_ias_lookup(tag_id: str) -> Tuple[bool, Optional[str]]:

    if tag_id in MOCK_IAS_DB:
        return True, MOCK_IAS_DB[tag_id]
    return False, "Invalid tag"


