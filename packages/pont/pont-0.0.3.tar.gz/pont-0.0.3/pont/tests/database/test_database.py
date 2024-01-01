import datetime

from pont.database.database import Database
from pont.flow import Flow


def test_flows_add():
    db = Database()
    flow = Flow("http")
    db.flows().add(flow)
    assert len(db.flows().find()) == 1


def test_get_flow():
    db = Database()
    flow = Flow("http", id="1")
    db.flows().add(flow)
    assert db.flows().get("1") == flow


def test_empty_flows():
    db = Database()
    assert len(db.flows().find()) == 0


def test_flows():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find()
    assert len(flows) == 2
    assert flows[0] == flow1
    assert flows[1] == flow2


def test_flows_with_filter_exact_match():
    db = Database()
    flow1 = Flow("http", id="1", status="200")
    flow2 = Flow("https", id="2", status="200")
    flow3 = Flow("http", id="3", status="404")
    flow4 = Flow("http", id="4", status="200")
    db.flows().add(flow1)
    db.flows().add(flow2)
    db.flows().add(flow3)
    db.flows().add(flow4)
    flows = db.flows().find("status=200 AND protocol=http")
    assert len(flows) == 2
    assert flows[0] == flow1
    assert flows[1] == flow4


def test_sort_alpha():
    db = Database()
    flow1 = Flow("http", id="1", host="b.org")
    flow2 = Flow("http", id="2", host="a.com")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(sort="host")
    assert len(flows) == 2
    assert flows[0].id == flow2.id


def test_sort_numeric():
    db = Database()
    flow1 = Flow("http", id="1", port=443)
    flow2 = Flow("http", id="2", port=80)
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(sort="port")
    assert len(flows) == 2
    assert flows[0].id == flow2.id


def test_sort_datetime():
    db = Database()
    flow1 = Flow("http", id="1", updated_at=datetime.datetime(2021, 1, 1))
    flow2 = Flow("http", id="2", updated_at=datetime.datetime(2020, 1, 1))
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(sort="updated_at")
    assert len(flows) == 2
    assert flows[0].id == flow2.id


def test_limit_without_sort():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(limit=1)
    assert len(flows) == 1
    assert flows[0].id == flow1.id


def test_limit_with_sort():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(limit=1, sort="id")
    assert len(flows) == 1
    assert flows[0].id == flow1.id


def test_limit_reverse():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(limit=1, sort="id", reverse=True)
    assert len(flows) == 1
    assert flows[0].id == flow2.id


def test_reverse_without_sort_with_query():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(query="protocol=http", reverse=True)
    assert len(flows) == 2
    assert flows[0].id == flow2.id
    assert flows[1].id == flow1.id


def test_reverse_without_sort_with_query_with_limit():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("mysql", id="2")
    flow3 = Flow("http", id="3")
    db.flows().add(flow1)
    db.flows().add(flow2)
    db.flows().add(flow3)
    flows = db.flows().find(
        query="protocol=http",
        limit=2,
        reverse=True,
    )
    assert len(flows) == 2
    assert flows[0].id == flow3.id


def test_reverse_without_sort_without_query():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    db.flows().add(flow1)
    db.flows().add(flow2)
    flows = db.flows().find(reverse=True)
    assert len(flows) == 2
    assert flows[0].id == flow2.id
    assert flows[1].id == flow1.id


def test_reverse_without_sort_without_query_with_limit():
    db = Database()
    flow1 = Flow("http", id="1")
    flow2 = Flow("http", id="2")
    flow3 = Flow("http", id="3")
    db.flows().add(flow1)
    db.flows().add(flow2)
    db.flows().add(flow3)
    flows = db.flows().find(query="", limit=2, reverse=True)
    assert len(flows) == 2
    assert flows[0].id == flow3.id


def test_clear():
    db = Database()
    flow = Flow("http")
    db.flows().add(flow)
    assert len(db.flows().find()) == 1
    db.flows().clear()
    assert len(db.flows().find()) == 0
