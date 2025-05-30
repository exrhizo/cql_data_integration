from typing import Optional, List, Any, Iterable
from pydantic import BaseModel, Field

class AttributeFragment(BaseModel):
    """Partial description of an attribute in an ontology."""
    name: str
    dtype: Optional[str] = None
    description: Optional[str] = None

class EntityFragment(BaseModel):
    """Partial description of an entity consisting of attributes."""
    name: str
    attributes: List[AttributeFragment] = Field(default_factory=list)
    description: Optional[str] = None

class OntologicalFragment(BaseModel):
    """Collection of entity fragments capturing a portion of an ontology."""
    name: str
    entities: List[EntityFragment] = Field(default_factory=list)
    description: Optional[str] = None

class OntologicalDataFrame(BaseModel):
    """Associates a pandas DataFrame with an ontological fragment."""
    data: Any  # Expected to be a pandas.DataFrame
    fragment: OntologicalFragment

    class Config:
        arbitrary_types_allowed = True

def tag_dataframe(df: Any, fragment: OntologicalFragment) -> OntologicalDataFrame:
    """Wrap a DataFrame with ontological metadata."""
    return OntologicalDataFrame(data=df, fragment=fragment)

def assert_dataframe_has_columns(df: Any, fragment: OntologicalFragment) -> None:
    """Raise AssertionError if df is missing columns declared in fragment."""
    # try to obtain iterable of column names
    columns: Iterable[str] = getattr(df, "columns", [])
    missing = []
    for ent in fragment.entities:
        for attr in ent.attributes:
            if attr.name not in columns:
                missing.append(attr.name)
    if missing:
        raise AssertionError(f"DataFrame is missing expected columns: {missing}")
