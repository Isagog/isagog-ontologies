from typing import List, Optional, Any

from pydantic import BaseModel, Field

from isagog_kg.models.logic_model import Thing 


class Entity(Thing):
    """Thing localizable in space and / or time"""
    mentioned_in: List['Document'] = Field(default_factory=list, description="mentioned_in property", json_schema_extra={'kg_property': 'mentioned_in', 'kg_type': 'relation', 'kg_related_class': 'Document'})
    referred_by: List['EntityDescriptor'] = Field(default_factory=list, description="referred_by property", json_schema_extra={'kg_property': 'referred_by', 'kg_type': 'relation', 'kg_related_class': 'EntityDescriptor'})

class Continuant(Entity):
    """An entity that persists through time while maintaining its identity, existing as a whole at any given moment. Continuants are not characterized by temporal parts; instead, they endure as the same entity throughout change, distinct from processes or events, which unfold over time."""

class Sign(Thing):
    """A non-material entity that underlies the process of interpreting something as representing or standing for something else. Signs existentially depend on the source that generates them, as each sign is a particular instance (token)."""
    referent: List['Thing'] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Thing'})
    source: Optional[Any] = Field(default=None, description="source property", json_schema_extra={'kg_property': 'source', 'kg_type': 'relation', 'kg_related_class': 'Any'})
    concept: Optional[str] = Field(default=None, description="concept property", json_schema_extra={'kg_property': 'concept', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Statement(Sign):
    """Linguistic proposition (i.e. sentence that may be true or false) about a state of affairs"""
    expression: Optional[str] = Field(default=None, description="expression property", json_schema_extra={'kg_property': 'expression', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Description(Statement):
    """Statement that brings information about a specific aspect or feature of something"""

class SocialObject(Thing):
    """Non-material entity that is socially instituted and identified, such as: informative objects (e.g. documents), political movements, promises, committments, etc. It doesn't have direct temporal-spatial attributes"""

class Information(SocialObject):
    """Social object that yields signs, which may be instantiated in many physical forms, e.g. documents, descriptors, classifiers such as tags or topics, word types (lexemes) and tokens."""
    yields: List['Sign'] = Field(default_factory=list, description="yields property", json_schema_extra={'kg_property': 'yields', 'kg_type': 'relation', 'kg_related_class': 'Sign'})

class Document(Information):
    """Textual document"""
    authored_by: List['Person'] = Field(default_factory=list, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Person', 'we_filter': 'true', 'we_search': 'true', 'we_tok': 'FIELD'})
    body: Optional[str] = Field(default=None, description="body property", json_schema_extra={'kg_property': 'body', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class EntityDescriptor(Description):
    """Descriptions referring to entities"""
    referent: List[Any] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Any'})

class Occurrent(Entity):
    """Entities that unfold or occur over time, such as events, processes,  or activities. These entities are not wholly present at any single moment but are extended in time, contrasting with 'Continuants', which persist while maintaining identity."""
    has_participant: List['Entity'] = Field(default_factory=list, description="has_participant property", json_schema_extra={'kg_property': 'has_participant', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    in_place: List['Location'] = Field(default_factory=list, description="in_place property", json_schema_extra={'kg_property': 'in_place', 'kg_type': 'relation', 'kg_related_class': 'Location'})
    time_coordinate: List[str] = Field(default_factory=list, description="time_coordinate property", json_schema_extra={'kg_property': 'time_coordinate', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Event(Occurrent):
    pass

class Location(Continuant):
    """Identified portion of space not necessarily continuous"""

class Material(Continuant):
    """A non-sortal continuant that exists as a mass or quantity without inherent boundaries or a distinct identity, persisting through time while undergoing potential changes in form or composition. Material is typically characterized by its divisibility and its capacity to constitute or combine with other entities to form objects or structures."""

class Mention(Statement):
    """A textual or verbal occurrence that denotes an entity (e.g., a name). Mentions may sometimes be erroneous, either by referring to a non-existent entity or by misidentifying the intended referent."""
    referred_by: List['EntityDescriptor'] = Field(default_factory=list, description="referred_by property", json_schema_extra={'kg_property': 'referred_by', 'kg_type': 'relation', 'kg_related_class': 'EntityDescriptor'})
    referent: List['Entity'] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Entity'})

class Object(Continuant):
    """A sortal continuant characterized by having determinate boundaries and a unity criterion that defines its persistence as a distinct entity. Changes in morphology or composition may affect its identity within a given context."""

class Organization(Continuant):
    """Social group of people working together towards common goals, governed by defined rules and processes"""

class Person(Continuant):
    anthroponym: str = Field(..., description="anthroponym property", json_schema_extra={'kg_property': 'anthroponym', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Relationship(Statement):
    """A formal statement (assertion) that specifies how two entities are connected or associated within a given context, describing the nature, direction, and type of interaction or dependency between them."""
    subject: Any = Field(..., description="subject property", json_schema_extra={'kg_property': 'subject', 'kg_type': 'relation', 'kg_related_class': 'Any'})
    object: Optional[Any] = Field(default=None, description="object property", json_schema_extra={'kg_property': 'object', 'kg_type': 'relation', 'kg_related_class': 'Any'})

class State(Occurrent):
    pass

class ArtMovement(SocialObject):
    pass

class ArtWork(Object):
    authored_by: List['Person'] = Field(default_factory=list, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Person'})

class Author(Person):
    """Autorship information, realized (but not necessarily) by some agent"""

class Building(Location):
    has_part: List['BuldingPart'] = Field(default_factory=list, description="has_part property", json_schema_extra={'kg_property': 'has_part', 'kg_type': 'relation', 'kg_related_class': 'BuldingPart'})

class BuldingPart(Building):
    part_of: 'Building' = Field(..., description="part_of property", json_schema_extra={'kg_property': 'part_of', 'kg_type': 'relation', 'kg_related_class': 'Building'})

class Curator(Person):
    pass

class CuratorialRecord(Document):
    authored_by: Optional['Curator'] = Field(default=None, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Curator'})
    inheres_to: Optional['ArtWork'] = Field(default=None, description="inheres_to property", json_schema_extra={'kg_property': 'inheres_to', 'kg_type': 'relation', 'kg_related_class': 'ArtWork'})

class Exibition(Event):
    features: List['ArtWork'] = Field(default_factory=list, description="features property", json_schema_extra={'kg_property': 'features', 'kg_type': 'relation', 'kg_related_class': 'ArtWork'})

class ExibitionLocation(Location):
    pass

class Hall(BuldingPart):
    pass

class Museum(Location):
    pass

class Visit(Event):
    has_participant: List['Person'] = Field(default_factory=list, description="has_participant property", json_schema_extra={'kg_property': 'has_participant', 'kg_type': 'relation', 'kg_related_class': 'Person'})

class Visitor(Person):
    pass


# Update forward references
Entity.model_rebuild()
Continuant.model_rebuild()
Sign.model_rebuild()
Statement.model_rebuild()
Description.model_rebuild()
SocialObject.model_rebuild()
Information.model_rebuild()
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
ArtMovement.model_rebuild()
ArtWork.model_rebuild()
Author.model_rebuild()
Building.model_rebuild()
BuldingPart.model_rebuild()
Curator.model_rebuild()
CuratorialRecord.model_rebuild()
Exibition.model_rebuild()
ExibitionLocation.model_rebuild()
Hall.model_rebuild()
Museum.model_rebuild()
Visit.model_rebuild()
Visitor.model_rebuild()