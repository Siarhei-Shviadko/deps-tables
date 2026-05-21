class TestHealthcheck:
    endpoint = "/api/tables"

    def test_healthcheck(self, client):
        response = client.get(f"{self.endpoint}/healthcheck")

        assert response.status_code == 200
