from typing import List, Optional, Any

from pydantic import BaseModel, Field

from isagog_kg.models.logic_model import Thing 


class Entity(Thing):
    """Thing localizable in space and / or time"""
    described_by: List['EntityDescriptor'] = Field(default_factory=list, description="described_by property", json_schema_extra={'kg_property': 'described_by', 'kg_type': 'relation', 'kg_related_class': 'EntityDescriptor'})
    mentioned_in: List['Document'] = Field(default_factory=list, description="mentioned_in property", json_schema_extra={'kg_property': 'mentioned_in', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class Continuant(Entity):
    """An entity that persists through time while maintaining its identity, existing as a whole at any given moment. Continuants are not characterized by temporal parts; instead, they endure as the same entity throughout change, distinct from processes or events, which unfold over time."""

class Information(Thing):
    """Non material thing that yields signs, which may be instantiated in many physical forms, e.g. documents, descriptors, classifiers such as tags or topics, word types (lexemes) and tokens."""

class Sign(Information):
    """Non-material entity underpinning the process of interpreting something as representing or standing for something else. Signs may yield other Signs (Peirce: unlimited semiosis)"""
    referent: List[Any] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Any'})
    source: List['Information'] = Field(default_factory=list, description="source property", json_schema_extra={'kg_property': 'source', 'kg_type': 'relation', 'kg_related_class': 'Information'})
    concept: Optional[str] = Field(default=None, description="concept property", json_schema_extra={'kg_property': 'concept', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    expression: Optional[str] = Field(default=None, description="expression property", json_schema_extra={'kg_property': 'expression', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Statement(Sign):
    """Proposition (i.e. sentence that may be true or false) about a state of affairs"""

class Description(Statement):
    """Statement about a specific aspect or feature of something"""

class Document(Information):
    """Textual document"""
    authored_by: List['Person'] = Field(default_factory=list, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Person'})
    yields: List['Sign'] = Field(default_factory=list, description="yields property", json_schema_extra={'kg_property': 'yields', 'kg_type': 'relation', 'kg_related_class': 'Sign'})

class EntityDescriptor(Description):
    referent: List['Entity'] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Entity'})

class Occurrent(Entity):
    """Entities that unfold or occur over time, such as events, processes,  or activities. These entities are not wholly present at any single moment but are extended in time, contrasting with 'Continuants', which persist while maintaining identity."""
    has_participant: List['Entity'] = Field(default_factory=list, description="has_participant property", json_schema_extra={'kg_property': 'has_participant', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    in_place: List['Location'] = Field(default_factory=list, description="in_place property", json_schema_extra={'kg_property': 'in_place', 'kg_type': 'relation', 'kg_related_class': 'Location'})
    time_coordinate: List[str] = Field(default_factory=list, description="time_coordinate property", json_schema_extra={'kg_property': 'time_coordinate', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Event(Occurrent):
    pass

class Location(Continuant):
    """Identified portion of space (place)"""
    geo_coordinate: List[str] = Field(default_factory=list, description="geo_coordinate property", json_schema_extra={'kg_property': 'geo_coordinate', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Material(Continuant):
    """A non-sortal continuant that exists as a mass or quantity without inherent boundaries or a distinct identity, persisting through time while undergoing potential changes in form or composition. Material is typically characterized by its divisibility and its capacity to constitute or combine with other entities to form objects or structures."""

class Mention(Sign):
    """Denotation of an entity (e.g. a name)"""
    referent: List['Entity'] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Entity'})

class Object(Continuant):
    """A sortal continuant characterized by having determinate boundaries and a unity criterion that defines its persistence as a distinct entity. Changes in morphology or composition may affect its identity within a given context."""

class Organization(Continuant):
    """Social group of people working together towards common goals, governed by defined rules and processes"""

class Person(Continuant):
    name: str = Field(..., description="name property", json_schema_extra={'kg_property': 'name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    surname: str = Field(..., description="surname property", json_schema_extra={'kg_property': 'surname', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Relationship(Statement):
    """A formal statement (assertion) that specifies how two entities are connected or associated within a given context, describing the nature, direction, and type of interaction or dependency between them."""
    subject: Any = Field(..., description="subject property", json_schema_extra={'kg_property': 'subject', 'kg_type': 'relation', 'kg_related_class': 'Any'})
    object: Optional[Any] = Field(default=None, description="object property", json_schema_extra={'kg_property': 'object', 'kg_type': 'relation', 'kg_related_class': 'Any'})

class State(Occurrent):
    pass


# Update forward references
Entity.model_rebuild()
Continuant.model_rebuild()
Information.model_rebuild()
Sign.model_rebuild()
Statement.model_rebuild()
Description.model_rebuild()
Document.model_rebuild()
EntityDescriptor.model_rebuild()
Occurrent.model_rebuild()
Event.model_rebuild()
Location.model_rebuild()
Material.model_rebuild()
Mention.model_rebuild()
Object.model_rebuild()
Organization.model_rebuild()
Person.model_rebuild()
Relationship.model_rebuild()
State.model_rebuild()