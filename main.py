import json

from api_methods import FAIAPIMethods


def scanSKU() -> str:
    """Simulate scanning a SKU and returning its code."""
    # In a real application, this would interface with a scanner or input device.
    return "SKU12345"


def doingSomething(location_index, location_code) -> None:
    """Simulate doing something with the scanned SKU."""
    print(f"Doing something with SKU at location {location_index} ({location_code})...")


def processingLoop(api: FAIAPIMethods, location_code: str):
    """Example processing loop for a sorting session."""
    # Get sorting session info
    session_info = api.getSortingSessionInfo(location_code)
    if not session_info:
        print("Failed to retrieve sorting session info.")
        return
    print(f"Sorting Session Info: {session_info}\n")

    location_id = session_info.get("locationId")
    pick_list_id = session_info.get("pickListId")
    number_of_trans = session_info.get("numberOfTrans")

    if not location_id or location_id == 0:
        print("Invalid location ID in session info.")
        return

    tote_info = api.getLocationInfo("T080")
    if not tote_info:
        print("Failed to retrieve tote info.")
        return
    print(f"Tote Info: {tote_info}\n")

    session_start = api.createSortingSession(
        {
            "userCode": "phung",
            "warehouseCode": "WRN",
            "pickupLocationId": location_id,  # Check this, I dont't know if it is correct
            "sortingLocations": [
                "T080",
                "T081",
                "T082",
            ],  # Check this, I dont't know if it is correct
        }
    )
    if not session_start:
        print("Failed to create sorting session.")
        return
    print(f"Session Start: {session_start}\n")

    sorting_session_id = session_start.get("sortingSessionId")
    list_products = session_start.get("products", [])
    list_items = session_start.get("items", [])

    while True:
        sku = scanSKU()
        product_id = None
        # item_found = False
        list_of_items_matched = []
        final_item = None
        for product in list_products:
            if product.get("sku") == sku:
                product_id = product.get("productId")
                break
        if not product_id:
            print(f"SKU {sku} not found in product list.")
            continue
        for item in list_items:
            if item.get("productId") == product_id:
                list_of_items_matched.append(item)
        if len(list_of_items_matched) == 0:
            print(f"No items found for product ID {product_id}.")
            continue
        if len(list_of_items_matched) > 1:
            print(
                f"Multiple items found for product ID {product_id}. Please specify further."
            )  # This is a placeholder for further logic to handle multiple items
            final_item = list_of_items_matched[0]  # Default to the first item
            continue
        if len(list_of_items_matched) == 1:
            final_item = list_of_items_matched[0]

        body = {
            "userCode": "phung",
            "warehouseCode": "WRN",
            "productId": final_item.get("productId"),
            "unitId": final_item.get("unitId"),
            "conditionTypeId": final_item.get("conditionTypeId"),
            "productType": 1,
            "expiredDate": final_item.get("expiredDate"),
            "storageCode": final_item.get("storageCode"),
            "isSingleItem": True,
        }

        process_item = api.processItem(sorting_session_id=sorting_session_id, body=body)
        if not process_item:
            print("Failed to process item.")
            continue
        sorting_location_code = process_item.get("locationCode")
        sorting_location_index = process_item.get("locationIndex")
        doingSomething(
            location_index=sorting_location_index, location_code=sorting_location_code
        )


if __name__ == "__main__":
    api = FAIAPIMethods()

    processingLoop(api, "T074")
