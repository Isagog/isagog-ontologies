from typing import List, Optional, Any

from pydantic import BaseModel, Field

from isagog_kg.models.logic_model import Thing 


class Information(Thing):
    """Non material thing that conveys semantic information, realizable in many physical forms, e.g. a newspaper article (written or spoken), signs such as tags or topics, word types (lexemes)."""
    yields: List['Sign'] = Field(default_factory=list, description="yields property", json_schema_extra={'kg_property': 'yields', 'kg_type': 'relation', 'kg_related_class': 'Sign'})

class Sign(Information):
    """Non-material entity underpinning the process of interpreting one thing as representing or standing for another"""
    source: List['Information'] = Field(default_factory=list, description="source property", json_schema_extra={'kg_property': 'source', 'kg_type': 'relation', 'kg_related_class': 'Information'})
    expression: str = Field(..., description="expression property", json_schema_extra={'kg_property': 'expression', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    concept: Optional[str] = Field(default=None, description="concept property", json_schema_extra={'kg_property': 'concept', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    status: Optional[str] = Field(default=None, description="status property", json_schema_extra={'kg_property': 'status', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Descriptor(Sign):
    """An information item that qualifies a specific aspect or feature of something"""
    describes: List['Thing'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Thing'})

class EntityDescriptor(Descriptor):
    pass

class AIDescriptior(EntityDescriptor):
    pass

class Document(Information):
    """Textual document"""
    described_by: List['Metadata'] = Field(default_factory=list, description="described_by property", json_schema_extra={'kg_property': 'described_by', 'kg_type': 'relation', 'kg_related_class': 'Metadata'})
    body: Optional[str] = Field(default=None, description="body property", json_schema_extra={'kg_property': 'body', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Article(Document):
    """Newspaper article"""
    authored_by: List['Author'] = Field(default_factory=list, description="authored_by property", json_schema_extra={'kg_property': 'authored_by', 'kg_type': 'relation', 'kg_related_class': 'Author'})
    title: Optional[str] = Field(default=None, description="title property", json_schema_extra={'kg_property': 'title', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    published_day: str = Field(..., description="published_day property", json_schema_extra={'kg_property': 'published_day', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    edition_date: Optional[str] = Field(default=None, description="edition_date property", json_schema_extra={'kg_property': 'edition_date', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    kicker: Optional[str] = Field(default=None, description="kicker property", json_schema_extra={'kg_property': 'kicker', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Entity(Thing):
    """Entità localizzabile nello spazio e / o nel tempo"""
    described_by: List['EntityDescriptor'] = Field(default_factory=list, description="described_by property", json_schema_extra={'kg_property': 'described_by', 'kg_type': 'relation', 'kg_related_class': 'EntityDescriptor'})
    mentioned_in: List['Document'] = Field(default_factory=list, description="mentioned_in property", json_schema_extra={'kg_property': 'mentioned_in', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class Person(Entity):
    name: List[str] = Field(default_factory=list, description="name property", json_schema_extra={'kg_property': 'name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    surname: str = Field(..., description="surname property", json_schema_extra={'kg_property': 'surname', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Author(Person):
    """Autorship information, realized (but not necessarily) by some agent"""
    author_of: List['Document'] = Field(default_factory=list, description="author_of property", json_schema_extra={'kg_property': 'author_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})
    author_str: str = Field(..., description="author_str property", json_schema_extra={'kg_property': 'author_str', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Metadata(Descriptor):
    """Document's metadata"""
    describes: List['Document'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Document'})
    text: Optional[str] = Field(default=None, description="text property", json_schema_extra={'kg_property': 'text', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Category(Metadata):
    """Categoria di classificazione di oggetti informativi"""
    category_of: List['Document'] = Field(default_factory=list, description="category_of property", json_schema_extra={'kg_property': 'category_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class DBPediaDescriptor(EntityDescriptor):
    describes: List['Entity'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    dbpedia_ref: str = Field(..., description="dbpedia_ref property", json_schema_extra={'kg_property': 'dbpedia_ref', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Event(Entity):
    """Temporal entity, either stative or dynamic"""
    has_participant: List['Entity'] = Field(default_factory=list, description="has_participant property", json_schema_extra={'kg_property': 'has_participant', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    in_place: List['Location'] = Field(default_factory=list, description="in_place property", json_schema_extra={'kg_property': 'in_place', 'kg_type': 'relation', 'kg_related_class': 'Location'})

class GeonamesDescriptor(EntityDescriptor):
    describes: List['Entity'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    geoinfo_bbox: List[str] = Field(default_factory=list, description="geoinfo_bbox property", json_schema_extra={'kg_property': 'geoinfo_bbox', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_country_name: List[str] = Field(default_factory=list, description="geoinfo_country_name property", json_schema_extra={'kg_property': 'geoinfo_country_name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_name: List[str] = Field(default_factory=list, description="geoinfo_name property", json_schema_extra={'kg_property': 'geoinfo_name', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_feature_class: Optional[str] = Field(default=None, description="geoinfo_feature_class property", json_schema_extra={'kg_property': 'geoinfo_feature_class', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_feature_code: Optional[str] = Field(default=None, description="geoinfo_feature_code property", json_schema_extra={'kg_property': 'geoinfo_feature_code', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    geoinfo_id: Optional[int] = Field(default=None, description="geoinfo_id property", json_schema_extra={'kg_property': 'geoinfo_id', 'kg_type': 'attribute', 'kg_data_type': 'int'})
    geoinfo_lat: Optional[float] = Field(default=None, description="geoinfo_lat property", json_schema_extra={'kg_property': 'geoinfo_lat', 'kg_type': 'attribute', 'kg_data_type': 'float'})
    geoinfo_lng: Optional[float] = Field(default=None, description="geoinfo_lng property", json_schema_extra={'kg_property': 'geoinfo_lng', 'kg_type': 'attribute', 'kg_data_type': 'float'})

class Highlight(Metadata):
    pass

class HumanDescriptor(EntityDescriptor):
    userid: Optional[str] = Field(default=None, description="userid property", json_schema_extra={'kg_property': 'userid', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Location(Entity):
    """Identified portion of space (place)"""

class Mention(Sign):
    """Reference to an Entity in a Document"""
    referent: Optional['Entity'] = Field(default=None, description="referent property", json_schema_extra={'kg_property': 'referent', 'kg_type': 'relation', 'kg_related_class': 'Entity'})

class Organization(Entity):
    """Social group of people working together towards common goals, governed by defined rules and processes"""

class Picture(Information):
    """Immagine fotografica o grafica a corredo di articolo o numero"""
    picture_of: List['Article'] = Field(default_factory=list, description="picture_of property", json_schema_extra={'kg_property': 'picture_of', 'kg_type': 'relation', 'kg_related_class': 'Article'})
    imgcaption: List[str] = Field(default_factory=list, description="imgcaption property", json_schema_extra={'kg_property': 'imgcaption', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    copyright: Optional[str] = Field(default=None, description="copyright property", json_schema_extra={'kg_property': 'copyright', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    imgurl: Optional[str] = Field(default=None, description="imgurl property", json_schema_extra={'kg_property': 'imgurl', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Relationship(Sign):
    """Reference to a relationship"""
    subject: 'Mention' = Field(..., description="subject property", json_schema_extra={'kg_property': 'subject', 'kg_type': 'relation', 'kg_related_class': 'Mention'})
    object: Optional['Mention'] = Field(default=None, description="object property", json_schema_extra={'kg_property': 'object', 'kg_type': 'relation', 'kg_related_class': 'Mention'})

class Summary(Metadata):
    summarizes: 'Document' = Field(..., description="summarizes property", json_schema_extra={'kg_property': 'summarizes', 'kg_type': 'relation', 'kg_related_class': 'Document'})
    text: str = Field(..., description="text property", json_schema_extra={'kg_property': 'text', 'kg_type': 'attribute', 'kg_data_type': 'str'})

class Tag(Metadata):
    tag_of: List['Document'] = Field(default_factory=list, description="tag_of property", json_schema_extra={'kg_property': 'tag_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class Topic(Metadata):
    """Argomento rilevante di articolo identificato dalle funzioni redazionali o dall'IA"""
    topic_of: List['Document'] = Field(default_factory=list, description="topic_of property", json_schema_extra={'kg_property': 'topic_of', 'kg_type': 'relation', 'kg_related_class': 'Document'})

class WikipediaDescriptor(EntityDescriptor):
    """Wikipedia summary"""
    describes: List['Entity'] = Field(default_factory=list, description="describes property", json_schema_extra={'kg_property': 'describes', 'kg_type': 'relation', 'kg_related_class': 'Entity'})
    wiki_timestamp: Optional[str] = Field(default=None, description="wiki_timestamp property", json_schema_extra={'kg_property': 'wiki_timestamp', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    wiki_title: Optional[str] = Field(default=None, description="wiki_title property", json_schema_extra={'kg_property': 'wiki_title', 'kg_type': 'attribute', 'kg_data_type': 'str'})
    wiki_url: Optional[str] = Field(default=None, description="wiki_url property", json_schema_extra={'kg_property': 'wiki_url', 'kg_type': 'attribute', 'kg_data_type': 'str'})


# Update forward references
Information.model_rebuild()
Sign.model_rebuild()
Descriptor.model_rebuild()
EntityDescriptor.model_rebuild()
AIDescriptior.model_rebuild()
Document.model_rebuild()
Article.model_rebuild()
Entity.model_rebuild()
Person.model_rebuild()
Author.model_rebuild()
Metadata.model_rebuild()
Category.model_rebuild()
DBPediaDescriptor.model_rebuild()
Event.model_rebuild()
GeonamesDescriptor.model_rebuild()
Highlight.model_rebuild()
HumanDescriptor.model_rebuild()
Location.model_rebuild()
Mention.model_rebuild()
Organization.model_rebuild()
Picture.model_rebuild()
Relationship.model_rebuild()
Summary.model_rebuild()
Tag.model_rebuild()
Topic.model_rebuild()
WikipediaDescriptor.model_rebuild()