from pathlib import Path

from typing import Dict, List, Optional, Tuple


from rdflib import BNode, Graph, URIRef

from rdflib.namespace import OWL, RDF, RDFS, XSD


xsd_types = {

    str(XSD.string): "str",

    str(XSD.integer): "int",

    str(XSD.float): "float",

    str(XSD.double): "float",

    str(XSD.boolean): "bool",

    str(XSD.dateTime): "datetime",
    
    str(XSD.long): "int",

}



def _make_pydantic_field_definition(prop_name: str,

                           field_type: str,

                           value_type: str,

                           annotations: Optional[Dict[str, str]] = None) -> str:

    if "Optional" in field_type:

        default_value = "default=None"

    elif "List" in field_type:

        default_value = "default_factory=list"

    else:

        default_value = "..."

    extras = {

        'kg_property': prop_name,

    }

    if value_type in xsd_types.values():

        extras['kg_type'] = 'attribute'

        extras['kg_data_type'] = value_type

    else:

        extras['kg_type'] = 'relation'

        extras['kg_related_class'] = value_type

    if annotations:

        extras.update(annotations)

    field_def = f"    {prop_name}: {field_type}"

    field_def += f' = Field({default_value}, description="{prop_name} property", json_schema_extra={extras})'
    return field_def



class OntologyConverter:

    """Converts a Turtle ontology to Pydantic model classes."""


    def __init__(self) -> None:

        self.graph = Graph()

        self.namespace: Optional[str] = None

        # Using list to maintain order of classes as they appear

        self.class_order: List[str] = []

        self.class_hierarchy: Dict[str, List[str]] = {}

        self.class_restrictions: Dict[str, List[Tuple[str, str, str, int | None]]] = {}

        self.class_comments: Dict[str, str] = {}

        # Memorizziamo le annotazioni degli axiomi, indicizzate per (classe, proprietà)

        self.axiom_annotations: Dict[Tuple[str, str], Dict[str, str]] = {}


    def load_ontology(self, turtle_content: str) -> None:

        """Load ontology from Turtle content string."""

        self.graph.parse(data=turtle_content, format="turtle")


        # Extract base namespace

        for s, _p, _o in self.graph.triples((None, None, OWL.Ontology)):

            self.namespace = str(s).rstrip("#")

            break


    def extract_class_info(self) -> None:

        """Extract class hierarchy and restrictions from the ontology."""

        # Reset storage

        self.class_hierarchy.clear()
        self.class_restrictions.clear()
        self.class_comments.clear()

        self.axiom_annotations.clear()


        # Get all classes

        for class_uri in self.graph.subjects(RDF.type, OWL.Class):

            class_name = self._get_class_name(URIRef(str(class_uri))) if not isinstance(class_uri, BNode) else None

            if not class_name:
                continue


            # Add to ordered list if not already present

            if class_name not in self.class_order:
                self.class_order.append(class_name)


            # Get superclasses

            superclasses = []

            for superclass in self.graph.objects(class_uri, RDFS.subClassOf):

                if isinstance(superclass, (URIRef, BNode)):

                    if isinstance(superclass, URIRef):

                        superclass_name = self._get_class_name(superclass)

                        if superclass_name:
                            superclasses.append(superclass_name)

                    else:  # BNode - represents a restriction

                        self._process_restriction(class_name, superclass)


            self.class_hierarchy[class_name] = superclasses


            # Get class comment

            for comment in self.graph.objects(class_uri, RDFS.comment):

                self.class_comments[class_name] = str(comment)

                break


        # Process axioms annotations after aver raccolto le restrizioni

        self._extract_axiom_annotations()


    def _process_restriction(self, class_name: str, restriction_node: BNode) -> None:

        """Process an OWL restriction and store the property information."""

        restriction_type = None

        property_uri = None

        value_type = None

        cardinality = None


        for p, o in self.graph.predicate_objects(restriction_node):

            if p == OWL.onProperty:

                property_uri = o

            elif p == OWL.someValuesFrom:

                restriction_type = "some"

                value_type = o

            elif p == OWL.allValuesFrom:

                restriction_type = "all"

                value_type = o

            elif p in [

                OWL.qualifiedCardinality,

                OWL.maxQualifiedCardinality,

                OWL.minQualifiedCardinality,

            ]:

                restriction_type = str(p).split("#")[-1]

                cardinality = int(str(o))

            elif p in [OWL.onDataRange, OWL.onClass]:

                value_type = o


        if property_uri and restriction_type:

            if class_name not in self.class_restrictions:

                self.class_restrictions[class_name] = []


            property_name = self._get_property_name(URIRef(str(property_uri)))

            if isinstance(value_type, BNode):

                value_type_name = "Any"

            else:

                value_type_name = self._get_value_type_name(URIRef(str(value_type)))


            self.class_restrictions[class_name].append(

                (property_name, restriction_type, value_type_name, cardinality),
            )


    def _extract_axiom_annotations(self) -> None:
        """

        Process OWL axioms to extract annotations on restrictions.

        Queste annotazioni verranno integrate nel parametro json_schema_extra.
        """

        for axiom in self.graph.subjects(RDF.type, OWL.Axiom):

            source = self.graph.value(subject=axiom, predicate=OWL.annotatedSource)

            target = self.graph.value(subject=axiom, predicate=OWL.annotatedTarget)

            if source is None or target is None:
                continue

            class_name = self._get_class_name(URIRef(str(source)))

            if not class_name:
                continue

            # Verifichiamo che il target sia una restrizione contenente owl:onProperty

            property_uri = self.graph.value(subject=target, predicate=OWL.onProperty)

            if property_uri is None:
                continue

            property_name = self._get_property_name(URIRef(str(property_uri)))

            # Raccolta delle annotazioni (escludendo i predicati standard)

            annotations = {}

            for p, o in self.graph.predicate_objects(axiom):

                if p in {RDF.type, OWL.annotatedSource, OWL.annotatedProperty, OWL.annotatedTarget}:
                    continue

                key = self._get_property_name(URIRef(str(p)))

                annotations[key] = str(o)

            self.axiom_annotations[(class_name, property_name)] = annotations


    def _sort_classes_by_inheritance(self) -> List[str]:

        """Sort classes so that superclasses come before their subclasses."""

        # Create dependency graph

        dependencies = {

            cls: set(supers) - {"Thing"} for cls, supers in self.class_hierarchy.items()

        }


        # Topological sort

        sorted_classes = []

        visited = set()

        temp_visited = set()


        def visit(class_name: str) -> None:

            if class_name in temp_visited:

                msg = f"Circular inheritance detected involving {class_name}"

                raise ValueError(msg)

            if class_name not in visited:

                temp_visited.add(class_name)

                for superclass in dependencies.get(class_name, set()):

                    visit(superclass)

                temp_visited.remove(class_name)

                visited.add(class_name)
                sorted_classes.append(class_name)


        # Visit all classes in their original order

        for class_name in self.class_order:

            if class_name not in visited:

                visit(class_name)

        return sorted_classes


    def generate_model(self, format: str = "pydantic") -> str:

        """Generate model classes from the extracted ontology information."""

        match format.lower():

            case "pydantic":

                return self._generate_pydantic_model()

            case _:

                raise ValueError(f"Unsupported format: {format}")


    def _generate_pydantic_model(self) -> str:

        """Generate Pydantic model classes from the extracted ontology information."""

        imports = [

            "from typing import List, Optional, Any",

            "from pydantic import BaseModel, Field",

            "from isagog_kg.models.logic_model import Thing \n",

        ]


        classes = []

        forward_refs = set()


        # Sort classes by inheritance dependencies

        sorted_classes = self._sort_classes_by_inheritance()


        # Generate classes in dependency order

        for class_name in sorted_classes:

            superclasses = self.class_hierarchy.get(class_name, [])

            if not superclasses:

                superclasses = ["Thing"]


            class_def = [f"class {class_name}({', '.join(superclasses)}):"]


            # Add docstring if available

            if class_name in self.class_comments:

                class_def.append(f'    """{self.class_comments[class_name]}"""')


            # Add property fields

            if class_name in self.class_restrictions:
                for (

                    prop_name,

                    rest_type,

                    value_type,

                    cardinality,

                ) in self.class_restrictions[class_name]:

                    field_type = self._get_field_type(

                        rest_type,

                        value_type,

                        cardinality,
                    )


                    # Track forward references

                    if any(cls in field_type for cls in self.class_hierarchy):

                        forward_refs.add(class_name)


                    # Verifica se esistono annotazioni axiom per la coppia (classe, proprietà)

                    annotations = self.axiom_annotations.get((class_name, prop_name))

                    field_def = _make_pydantic_field_definition(prop_name, field_type, value_type, annotations)
                    class_def.append(field_def)

            if len(class_def) == 1:  # Only class definition, no fields
                class_def.append("    pass")


            classes.append("\n".join(class_def))


        # Add forward reference updates for all classes that have custom type fields

        updates = [f"{cls}.model_rebuild()" for cls in sorted_classes]

        classes.append("\n# Update forward references\n" + "\n".join(updates))


        return "\n\n".join(imports + classes)


    def _get_class_name(self, uri: URIRef) -> Optional[str]:

        """Extract class name from URI."""

        if not isinstance(uri, URIRef):

            return None

        return str(uri).split("#")[-1]


    def _get_property_name(self, uri: URIRef) -> str:

        """Extract property name from URI."""

        return str(uri).split("#")[-1]


    def _get_value_type_name(self, uri: URIRef) -> str:

        """Convert URI to Python type name."""

        if not uri:

            return "Any"


        # Handle XML Schema types

        uri_str = str(uri)

        if uri_str in xsd_types:

            return xsd_types[uri_str]


        # Handle custom classes

        class_name = self._get_class_name(uri)

        return class_name if class_name else "Any"


    def _get_field_type(

        self,

        restriction_type: str,

        value_type: str,

        cardinality: Optional[int],

    ) -> str:

        """Convert OWL restriction to Python type annotation."""

        # Se value_type è una classe custom (non built-in) la racchiudiamo tra virgolette

        if value_type not in {"str", "int", "float", "bool", "datetime", "Any"}:

            value_type = f"'{value_type}'"


        if restriction_type in ("some", "all"):

            return f"List[{value_type}]"

        if restriction_type == "maxQualifiedCardinality" and cardinality == 1:

            return f"Optional[{value_type}]"

        if restriction_type == "qualifiedCardinality" and cardinality == 1:

            return value_type


        return f"Optional[{value_type}]"



def ontology_to_pydantic(turtle_content: str) -> str:

    """Convert Turtle ontology content to Pydantic models."""

    converter = OntologyConverter()

    converter.load_ontology(turtle_content)

    converter.extract_class_info()

    return converter._generate_pydantic_model()



def generate_module(ontology_files: list[str], output_file: str | None = None, format: str = "pydantic") -> None:
    """

    Generate a Python module with Pydantic models from an ontology file.


    Args:

        ontology_files (str): Path to the ontology files (e.g. "resources/ontology/mema_ontology.ttl").

        output_file (str): Path to the output Python module file (e.g. "src/isagog_kg/models/mema_model.py").
    """

    converter = OntologyConverter()


    if output_file is None:

        output_file = ontology_files[-1].replace(".ttl", "_model.py")


    for ontology_file in ontology_files:

        with open(ontology_file, "r") as file:

            turtle_content = file.read()        

        converter.load_ontology(turtle_content)
        

    converter.extract_class_info()

    ontology_model = converter.generate_model(format)


    out_path = Path(output_file)

    if out_path.exists():

        response = input(f"File {out_path} already exists. Do you want to overwrite it? (y/n): ").lower()

        if response != "y":

            print("Operation cancelled")
            return


    with out_path.open("w") as file:

        file.write(ontology_model)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert ontology files to Python module")
    parser.add_argument("-o", "--ontologies", default=["top/isagog_ontology.ttl"], nargs="+", help="Path(s) to ontology file(s)")
    parser.add_argument("-m", "--output", help="Path to output Python module file")
    parser.add_argument("-f", "--format", default="pydantic", help="Output format (default: pydantic)")

    args = parser.parse_args()

    try:
        generate_module(args.ontologies, args.output, args.format)
    except Exception as e:
        print(f"Error: {e}")
