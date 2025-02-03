# mema_ontology
Ontology of MeMa Knowledge Base

## License
This work is licensed under a Creative Commons Attribution 4.0 International License.

## Credits
* Il Nuovo Manifesto Soc. Coop. Editrice, Via Angelo Bargoni 8, 00153 Roma, Italy
* Isagog Srl, Via Faà di Bruno 52, 00195 Roma, Italy

## Generating Python Models

The `ontology-to-module.py` script in the `src/utils` directory can be used to generate Python model classes from the mema_ontology.ttl file. To run the script:

```
python src/utils/ontology-to-module.py
```

This will generate a `mema_model.py` file in the `src/models` directory containing Pydantic model classes representing the entities and relationships defined in the ontology.

The generated models can then be used in your Python code to work with data conforming to the mema_ontology schema.
