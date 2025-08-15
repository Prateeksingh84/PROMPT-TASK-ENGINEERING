import json

def generate_text_based_knowledge_graph(extracted_json_data):
    """
    Generates a text-based knowledge graph from the extracted JSON content.
    This is a simplified representation focusing on hierarchical and explicit relationships.
    """
    graph_lines = []

    if "chapter_title" in extracted_json_data:
        graph_lines.append(f"Chapter: {extracted_json_data['chapter_title']}\n")

    def process_elements(elements, indent_level=0):
        indent_str = "  " * indent_level
        for element in elements:
            elem_type = element.get("type", "unknown")
            elem_name = element.get("name", "")
            elem_text = element.get("text", "")
            elem_desc = element.get("description", "")
            elem_caption = element.get("caption", "")

            if elem_type == "topic":
                graph_lines.append(f"{indent_str}- Topic: {elem_name}")
                if "elements" in element:
                    process_elements(element["elements"], indent_level + 1)
            elif elem_type == "sub_topic":
                graph_lines.append(f"{indent_str}- Sub-topic: {elem_name}")
                if "elements" in element:
                    process_elements(element["elements"], indent_level + 1)
            elif elem_type == "paragraph":
                pass 
            elif elem_type == "image":
                graph_lines.append(f"{indent_str}  - Image: {elem_caption if elem_caption else elem_desc}")
                if elem_caption and elem_desc:
                    graph_lines.append(f"{indent_str}    (Description: {elem_desc})")
            elif elem_type == "diagram":
                graph_lines.append(f"{indent_str}  - Diagram: {elem_caption if elem_caption else elem_desc}")
                if elem_caption and elem_desc:
                    graph_lines.append(f"{indent_str}    (Description: {elem_desc})")
            elif elem_type == "table":
                graph_lines.append(f"{indent_str}  - Table: {elem_caption}")
            elif elem_type == "example":
                graph_lines.append(f"{indent_str}  - Example: {elem_text.splitlines()[0]}...") 
            elif elem_type == "activity":
                graph_lines.append(f"{indent_str}  - Activity: {elem_desc}")
            elif elem_type == "question":
                graph_lines.append(f"{indent_str}  - Question: {elem_text.strip()}")
            elif elem_type == "external_source":
                graph_lines.append(f"{indent_str}  - Boxed Info/Source: {elem_text.strip().splitlines()[0]}...")

    if "content" in extracted_json_data and isinstance(extracted_json_data["content"], list):
        process_elements(extracted_json_data["content"])

    return "\n".join(graph_lines)

if __name__ == '__main__':
    
    dummy_json_data = {
        "chapter_title": "Sample Chapter on Photosynthesis",
        "content": [
            {
                "type": "topic",
                "name": "What is Photosynthesis?",
                "elements": [
                    {
                        "type": "paragraph",
                        "text": "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with chlorophyll. This process uses carbon dioxide and water as reactants."
                    },
                    {
                        "type": "image",
                        "description": "Diagram of a plant leaf showing stomata.",
                        "caption": "Fig. 1.1: Cross-section of a leaf."
                    },
                    {
                        "type": "sub_topic",
                        "name": "Requirements for Photosynthesis",
                        "elements": [
                            {
                                "type": "paragraph",
                                "text": "For photosynthesis to occur, plants need sunlight, chlorophyll, water, and carbon dioxide."
                            },
                            {
                                "type": "table",
                                "caption": "Table 1.1: Key Components of Photosynthesis",
                                "rows": [
                                    ["Component", "Source"],
                                    ["Sunlight", "Sun"],
                                    ["Water", "Soil"],
                                    ["Carbon Dioxide", "Air"]
                                ]
                            }
                        ]
                    },
                    {
                        "type": "activity",
                        "description": "To demonstrate that sunlight is essential for photosynthesis.",
                        "steps": [
                            "Take a potted plant and keep it in the dark for three days.",
                            "Cover one of its leaves with black paper.",
                            "Keep the plant in sunlight for a few hours.",
                            "Perform starch test on both leaves."
                        ]
                    },
                    {
                        "type": "question",
                        "text": "Why is chlorophyll important for plants?"
                    }
                ]
            }
        ]
    }
    knowledge_graph = generate_text_based_knowledge_graph(dummy_json_data)
    print("Generated Knowledge Graph:\n", knowledge_graph)

    output_dir = "../data/output_kg/"
    os.makedirs(output_dir, exist_ok=True)
    output_kg_path = os.path.join(output_dir, "sample_chapter_kg.txt")
    with open(output_kg_path, "w", encoding="utf-8") as f:
        f.write(knowledge_graph)
    print(f"Knowledge Graph saved to: {output_kg_path}")