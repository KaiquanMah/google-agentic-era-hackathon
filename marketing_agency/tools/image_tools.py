
import io
import json
import os
import re

from google.adk.tools import ToolContext
from google.genai import Client, types
from PIL import Image

# Correctly initialize the client based on working examples
client = Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
)

async def find_and_extract_elements(
    image_artifact_name: str, elements_to_find: list[str], tool_context: "ToolContext"
) -> dict[str, list[str]]:
    """Finds and extracts multiple elements from an image.

    This tool first uses a multimodal model to find the bounding boxes of
    requested elements, then crops and saves each element as a new artifact.

    Args:
        image_artifact_name: The name of the image artifact to process.
        elements_to_find: A list of strings describing the elements to find.
        tool_context: The context for the tool.

    Returns:
        A dictionary containing a list of the filenames of the extracted images.
    """
    # --- Part 0: Load the initial image artifact ---
    image_artifact = await tool_context.load_artifact(image_artifact_name)
    if not image_artifact:
        return {"error": f"Artifact '{image_artifact_name}' not found.".replace('"', '\"')}

    image_bytes = image_artifact.part.to_bytes()
    img = Image.open(io.BytesIO(image_bytes))

    # --- Part 1: Use the model to find bounding boxes ---
    prompt = f"""Analyze the attached image. Identify the following elements: 
    - {", ".join(elements_to_find)}

    For each element, provide its name and its bounding box as a list of four integer coordinates [x1, y1, x2, y2].
    Return the output as a single JSON array where each object has a "label" and a "box_2d" key.
    """
    response = client.models.generate_content([prompt, img], model="gemini-2.5-pro")

    try:
        cleaned_text = re.sub(r"^```json\n?|\n?```$", "", response.text, flags=re.MULTILINE)
        found_elements = json.loads(cleaned_text)
    except (json.JSONDecodeError, IndexError):
        return {"error": f"Failed to parse model response: {response.text}".replace('"', '\"')}

    # --- Part 2: Loop and extract each element ---
    extracted_files = []
    for i, element in enumerate(found_elements):
        label = element.get("label", f"element_{i}").replace(" ", "_").replace("'", "")
        box = element.get("box_2d")
        if not box or len(box) != 4:
            continue

        try:
            box_ints = [int(c) for c in box]
            cropped_image = img.crop(box_ints)
            
            output_buffer = io.BytesIO()
            cropped_image.save(output_buffer, format="PNG")
            output_bytes = output_buffer.getvalue()

            new_artifact_name = f"extracted_{label}.png"
            await tool_context.save_artifact(
                new_artifact_name,
                types.Part.from_bytes(data=output_bytes, mime_type="image/png"),
            )
            extracted_files.append(new_artifact_name)
        except Exception:
            # Ignore errors on individual crops
            continue

    return {"extracted_filenames": extracted_files}
