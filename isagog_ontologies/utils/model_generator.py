
from isagog_kg.utils.ontology_to_module import generate_module

if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert ontology files to Python module"
    )
    parser.add_argument(
        "-o",
        "--ontologies",
        default=["isagog_ontologies/ontologies/top/isagog_ontology.ttl", "isagog_ontologies/ontologies/maxxi/v1/maxxi_ontology.ttl"],
        nargs="+",
        help="Path(s) to ontology file(s)",
    )
    parser.add_argument("-m", "--output", help="Path to output Python module file")
    parser.add_argument(
        "-f", "--format", default="pydantic", help="Output format (default: pydantic)"
    )

    args = parser.parse_args()

    try:
        generate_module(args.ontologies, args.output, args.format)
    except Exception as e:
        print(f"Error: {e}") # noqa: T201
