import datetime

from pont.flow import Flow


def test_create_flow(mocker):
    flow = Flow("http", id="1", path="/hello")
    assert flow.id == "1"
    assert flow.path == "/hello"
    assert flow.protocol == "http"
    assert flow.updated_at is not None

    # Test that the updated_at field is updated when a field is updated
    past_date = datetime.datetime(2023, 1, 1)
    flow.updated_at = past_date
    assert flow.updated_at == past_date
    flow.path = "/world"
    assert flow.updated_at != past_date
