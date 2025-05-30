import pytest

from .. import (
    AttributeFragment,
    EntityFragment,
    OntologicalFragment,
    tag_dataframe,
    assert_dataframe_has_columns,
)

class FakeDataFrame:
    def __init__(self, rows):
        self._rows = rows
        if rows:
            self.columns = list(rows[0].keys())
        else:
            self.columns = []

    def __getitem__(self, item):
        return [row[item] for row in self._rows]


def fake_kusto(query: str) -> FakeDataFrame:
    """Return a FakeDataFrame mimicking a Kusto query result."""
    data = [
        {"Timestamp": "2024-01-01T00:00:00Z", "EventID": 1, "ComputerName": "host1"},
        {"Timestamp": "2024-01-01T00:01:00Z", "EventID": 2, "ComputerName": "host2"},
    ]
    return FakeDataFrame(data)


def windows_security_fragment() -> OntologicalFragment:
    return OntologicalFragment(
        name="WindowsSecurityLog",
        entities=[
            EntityFragment(
                name="LogEntry",
                attributes=[
                    AttributeFragment(name="Timestamp"),
                    AttributeFragment(name="EventID"),
                    AttributeFragment(name="ComputerName"),
                ],
            )
        ],
    )


def test_kusto_query_tagging():
    fragment = windows_security_fragment()
    df = fake_kusto("SecurityEvent | limit 2")
    assert_dataframe_has_columns(df, fragment)
    tagged = tag_dataframe(df, fragment)
    assert tagged.fragment.name == "WindowsSecurityLog"
    assert tagged.data.columns == ["Timestamp", "EventID", "ComputerName"]


def test_kusto_missing_column():
    fragment = windows_security_fragment()
    # Expect an additional column that isn't present
    fragment.entities[0].attributes.append(AttributeFragment(name="User"))
    df = fake_kusto("SecurityEvent | limit 2")
    with pytest.raises(AssertionError):
        assert_dataframe_has_columns(df, fragment)
