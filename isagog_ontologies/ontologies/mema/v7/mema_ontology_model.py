from typing import List, Optional, Any

from pydantic import BaseModel, Field

from isagog_kg.models.logic_model import Thing 


class Entity(Thing):
    """Thing localizable in space and / or time"""
    described_by: List['EntityDescriptor'] = Field(default_factory=list, description="described_by property", json_schema_extra={'kg_property': 'described_by', 'kg_type': 'relation', 'kg_related_class': 'EntityDescriptor'})
    mentioned_in: List['Document'] = Field(default_factory=list, description="mentioned_in property", json_schema_extra={'kg_property': 'mentioned_in', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class Continuant(Entity):
    """An entity that persists through time while maintaining its identity, existing as a whole at any given moment. Continuants are not characterized by temporal parts; instead, they endure as the same entity throughout change, distinct from processes or events, which unfold over time."""

class Sign(Thing):
    """A non-material entity that underlies the process of interpreting something as representing or standing for something else. Signs existentially depend on the information source that generates them, as each sign is a particular, individuated instance originating from a singular source of information."""
    referent: List[Any] = Field(default_factory=list, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Any'})
    source: Optional['Information'] = Field(default=None, description="source property", json_schema_extra={'kg_property': 'source', 'kg_type': 'relation', 'kg_related_class': 'Information'})
    concept: Optional[str] = Field(default=None, description="concept property", json_schema_extra={'kg_property': 'concept', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    expression: Optional[str] = Field(default=None, description="expression property", json_schema_extra={'kg_property': 'expression', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Statement(Sign):
    """Proposition (i.e. sentence that may be true or false) about a state of affairs"""

class Description(Statement):
    """Statement about a specific aspect or feature of something"""

class Information(Thing):
    """Non material thing that yields signs, which may be instantiated in many physical forms, e.g. documents, descriptors, classifiers such as tags or topics, word types (lexemes) and tokens."""
    yields: List['Sign'] = Field(default_factory=list, description="yields property", json_schema_extra={'kg_property': 'yields', 'kg_type': 'relation', 'kg_related_class': 'Sign'})

class Document(Information):
    """Textual document"""
    authored_by: List['Person'] = Field(default_factory=list, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Person', 'we_filter': 'true', 'we_search': 'true', 'we_tok': 'FIELD'})
    yields: List['Sign'] = Field(default_factory=list, description="yields property", json_schema_extra={'kg_property': 'yields', 'kg_type': 'relation', 'kg_related_class': 'Sign'})
    body: Optional[str] = Field(default=None, description="body property", json_schema_extra={'kg_property': 'body', 'kg_type': 'attribute', 'kg_data_type': 'str'})

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

class AIDescriptior(EntityDescriptor):
    pass

class Article(Document):
    """Newspaper article"""
    directus_id: str = Field(..., description="directus_id property", json_schema_extra={'kg_property': 'directus_id', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    published_day: str = Field(..., description="published_day property", json_schema_extra={'kg_property': 'published_day', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    title: str = Field(..., description="title property", json_schema_extra={'kg_property': 'title', 'kg_type': 'attribute', 'kg_data_type': 'str', 'we_search': 'false', 'we_tok': 'FIELD'})
    athena_id: Optional[str] = Field(default=None, description="athena_id property", json_schema_extra={'kg_property': 'athena_id', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    kicker: Optional[str] = Field(default=None, description="kicker property", json_schema_extra={'kg_property': 'kicker', 'kg_type': 'attribute', 'kg_data_type': 'str', 'we_search': 'false', 'we_tok': 'FIELD'})
    wp_id: Optional[str] = Field(default=None, description="wp_id property", json_schema_extra={'kg_property': 'wp_id', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    wp_slug: Optional[str] = Field(default=None, description="wp_slug property", json_schema_extra={'kg_property': 'wp_slug', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Author(Person):
    """Autorship information, realized (but not necessarily) by some agent"""
    author_of: List['Document'] = Field(default_factory=list, description="author_of property", json_schema_extra={'kg_property': 'author_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class Metadata(Description):
    """Document's metadata"""
    describes: List['Document'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Document'})
    text: Optional[str] = Field(default=None, description="text property", json_schema_extra={'kg_property': 'text', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Category(Metadata):
    """Categoria di classificazione di oggetti informativi"""
    category_of: List['Document'] = Field(default_factory=list, description="category_of property", json_schema_extra={'kg_property': 'category_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class DBPediaDescriptor(EntityDescriptor):
    dbpedia_ref: str = Field(..., description="dbpedia_ref property", json_schema_extra={'kg_property': 'dbpedia_ref', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class GeonamesDescriptor(EntityDescriptor):
    geoinfo_bbox: List[str] = Field(default_factory=list, description="geoinfo_bbox property", json_schema_extra={'kg_property': 'geoinfo_bbox', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_country_name: List[str] = Field(default_factory=list, description="geoinfo_country_name property", json_schema_extra={'kg_property': 'geoinfo_country_name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_name: List[str] = Field(default_factory=list, description="geoinfo_name property", json_schema_extra={'kg_property': 'geoinfo_name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_id: int = Field(..., description="geoinfo_id property", json_schema_extra={'kg_property': 'geoinfo_id', 'kg_type': 'attribute', 'kg_data_type': 'int'})
    geoinfo_feature_class: Optional[str] = Field(default=None, description="geoinfo_feature_class property", json_schema_extra={'kg_property': 'geoinfo_feature_class', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_feature_code: Optional[str] = Field(default=None, description="geoinfo_feature_code property", json_schema_extra={'kg_property': 'geoinfo_feature_code', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_lat: Optional[float] = Field(default=None, description="geoinfo_lat property", json_schema_extra={'kg_property': 'geoinfo_lat', 'kg_type': 'attribute', 'kg_data_type': 'float'})
    geoinfo_lng: Optional[float] = Field(default=None, description="geoinfo_lng property", json_schema_extra={'kg_property': 'geoinfo_lng', 'kg_type': 'attribute', 'kg_data_type': 'float'})
    geoinfo_population: Optional[int] = Field(default=None, description="geoinfo_population property", json_schema_extra={'kg_property': 'geoinfo_population', 'kg_type': 'attribute', 'kg_data_type': 'int'})

class Highlight(Metadata):
    pass

class HumanDescriptor(EntityDescriptor):
    userid: Optional[str] = Field(default=None, description="userid property", json_schema_extra={'kg_property': 'userid', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Picture(Information):
    """Immagine fotografica o grafica a corredo di articolo o numero"""
    picture_of: List['Article'] = Field(default_factory=list, description="picture_of property", json_schema_extra={'kg_property': 'picture_of', 'kg_type': 'relation', 'kg_related_class': 'Article'})
    imgcaption: List[str] = Field(default_factory=list, description="imgcaption property", json_schema_extra={'kg_property': 'imgcaption', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    copyright: Optional[str] = Field(default=None, description="copyright property", json_schema_extra={'kg_property': 'copyright', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    imgurl: Optional[str] = Field(default=None, description="imgurl property", json_schema_extra={'kg_property': 'imgurl', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Summary(Metadata):
    text: str = Field(..., description="text property", json_schema_extra={'kg_property': 'text', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Tag(Metadata):
    tag_of: List['Article'] = Field(default_factory=list, description="tag_of property", json_schema_extra={'kg_property': 'tag_of', 'kg_type': 'relation', 'kg_related_class': 'Article'})

class Topic(Metadata):
    """Argomento rilevante di articolo identificato dalle funzioni redazionali o dall'IA"""
    topic_of: List['Article'] = Field(default_factory=list, description="topic_of property", json_schema_extra={'kg_property': 'topic_of', 'kg_type': 'relation', 'kg_related_class': 'Article'})

class WikipediaDescriptor(EntityDescriptor):
    """Wikipedia summary"""
    wiki_timestamp: Optional[str] = Field(default=None, description="wiki_timestamp property", json_schema_extra={'kg_property': 'wiki_timestamp', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    wiki_title: Optional[str] = Field(default=None, description="wiki_title property", json_schema_extra={'kg_property': 'wiki_title', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    wiki_url: Optional[str] = Field(default=None, description="wiki_url property", json_schema_extra={'kg_property': 'wiki_url', 'kg_type': 'attribute', 'kg_data_type': 'str'})


# Update forward references
Entity.model_rebuild()
Continuant.model_rebuild()
Sign.model_rebuild()
Statement.model_rebuild()
Description.model_rebuild()
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
AIDescriptior.model_rebuild()
Article.model_rebuild()
Author.model_rebuild()
Metadata.model_rebuild()
Category.model_rebuild()
DBPediaDescriptor.model_rebuild()
GeonamesDescriptor.model_rebuild()
Highlight.model_rebuild()
HumanDescriptor.model_rebuild()
Picture.model_rebuild()
Summary.model_rebuild()
Tag.model_rebuild()
Topic.model_rebuild()
WikipediaDescriptor.model_rebuild()