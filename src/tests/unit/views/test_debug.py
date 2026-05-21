import pytest


def test_get__debug_page_for_sentry__return_ValueError(client):
    with pytest.raises(ValueError):
        client.get("/api/tables/debug/500")
