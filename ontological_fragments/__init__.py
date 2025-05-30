from typing import Optional, List, Any
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
