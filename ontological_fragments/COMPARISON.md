# Comparing Ontological Fragments with Existing CQL Models

The `ontological_fragments` module introduces small Pydantic models for describing
partial ontologies. Each `AttributeFragment`, `EntityFragment`, and
`OntologicalFragment` simply stores names and optional type information that can
later be attached to a DataFrame via `OntologicalDataFrame`.

```python
class AttributeFragment(BaseModel):
    name: str
    dtype: Optional[str] = None
    description: Optional[str] = None
```

This minimal approach contrasts with the more expressive style used in the rest
of the repository. For example, `cdi/science_example/inputs/catalysis.py`
constructs rich CQL models using helper constructors like `Entity`, `Attr`, and
`FK`:

```python
job = Entity(
    name = 'job',
    desc = 'DFT job',
    attrs= [Attr('stordir',  Varchar, desc = 'Directory containing log file', id=True),
            Attr('job_name', Varchar, desc = 'Name of job - arbitrary'),
            Attr('user',     Varchar, desc = 'Owner of job'),
            Attr('energy',   Double,  desc = 'Energy result of job')],
    fks = [FK('struct'), FK('calc')]
)
```

These CQL constructs not only define schema elements but also encode
constraints, path equations, and relationships between entities. The example
further sets up path equations to express domain knowledge:

```python
rich_pe = [
    PathEQ(Path(atom['number']),
           Path(atom['element'], elem['atomic_number'])),
    PathEQ(Path(b0['struct'], struct['system_type']),
           Path(JLit('bulk', String))),
]
```

To move `OntologicalFragment` toward this style, we could:

1. **Expand attribute and entity definitions.** Introduce richer field types and
   support for foreign keys similar to `FK` relationships. This would allow the
   fragment models to describe connections between fragments instead of just
   listing attributes.
2. **Capture constraints.** CQL schemas often specify invariants using
   `PathEQ` or `EQ`. Extending the fragment models with optional constraint
   objects would let us represent partial business logic along with schema
   descriptions.
3. **Provide builder utilities.** Functions that convert fragment definitions
   into CQL `Entity` and `Schema` objects would bridge the gap between the
   lightweight gradual typing approach and the full expressiveness of CQL.
4. **Annotate DataFrames with provenance.** Much like the CQL examples connect
   different entities through paths, fragments could track how DataFrame columns
   correspond to ontology attributes and how they were derived.

By following these directions, the fragment system can remain flexible while
getting closer to the powerful modeling capabilities showcased in the CQL
`catalysis` example.
