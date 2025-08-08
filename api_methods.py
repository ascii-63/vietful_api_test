from client import FAIAPIClient


class FAIAPIMethods:
    """Specific API methods for FAI OpenAPI endpoints."""

    def __init__(self):
        self.client = FAIAPIClient()

    def getSortingSessionInfo(self, location_code):
        return self.client.makeRequest(
            "GET", path=f"/api/v1/sorting-sessions/info/{location_code}"
        )

    def getLocationInfo(self, location_code):
        return self.client.makeRequest(
            method="GET", path=f"/api/v1/sorting-sessions/location/{location_code}"
        )

    def createSortingSession(self, body):
        return self.client.makeRequest(
            method="POST", path="/api/v1/sorting-sessions", body=body
        )

    def processItem(self, sorting_session_id, body):
        return self.client.makeRequest(
            method="POST",
            path=f"/api/v1/sorting-sessions/{sorting_session_id}/process",
            body=body,
        )

    def finishSortingSession(self, sorting_session_id):
        return self.client.makeRequest(
            method="POST", path=f"/api/v1/sorting-sessions/{sorting_session_id}/finish"
        )

    def pendingSortingSession(self, sorting_session_id):
        return self.client.makeRequest(
            method="POST", path=f"/api/v1/sorting-sessions/{sorting_session_id}/pending"
        )

    def restoreSortingSession(self, sorting_session_id):
        return self.client.makeRequest(
            method="POST", path=f"/api/v1/sorting-sessions/{sorting_session_id}/restore"
        )

    def getAllPartners(self):
        return self.client.makeRequest(method="GET", path="/api/v1/partners")
