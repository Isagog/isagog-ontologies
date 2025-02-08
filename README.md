# Isagog ontologies

This repo contains the top ontology of the Isagog platform, the domain specific ontologies for main ongoing projects, and a utility to generate pydantic modules out of the abovementioned ontologies


## Generating Python Models

The `ontology-to-module.py` script in the `isagog_ontologies/utils` directory can be used to generate Python model classes from an OWL ontology file like `mema_ontology.ttl`. 

To run the script and generate models from multiple ontology files:

```
python isagog_ontologies/utils/ontology-to-module.py -o mema/v7/mema_ontology.ttl top/isagog_ontology.ttl
```

This will generate a `mema_model.py` file in the `isagog_ontologies/models` directory containing Pydantic model classes. Each class corresponds to an entity or concept defined in the ontology, with properties representing the entity's attributes and relationships to other entities.

For example, you could use the generated `Artwork` model class like this:

```python
from isagog_ontologies.models.mema_model import Artwork

artwork = Artwork(
    label="The Starry Night",
    creator="Vincent Van Gogh",
    creation_date="1889"
)

print(artwork.json())
```

This will print a JSON representation of the Artwork instance with the specified label, creator and creation date properties.
