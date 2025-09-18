# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""img_element_extractor_agent: for extracting elements from images"""

import io
from PIL import Image
from google.adk import Agent
from google.adk.tools import ToolContext
from google.genai import types

from . import prompt

MODEL = "gemini-2.5-pro"
MODEL_IMAGE = "imagen-3.0-generate-002"


async def extract_image_region(
    image_artifact_name: str, box_2d: list[int], tool_context: "ToolContext"
) -> dict[str, str]:
    """Extracts a region from an image based on a bounding box.

    Args:
        image_artifact_name: The name of the image artifact to load.
        box_2d: A list of 4 integers representing the bounding box [x1, y1, x2, y2].
        tool_context: The context for the tool.

    Returns:
        A dictionary containing the status and the filename of the extracted image.
    """
    image_artifact = await tool_context.load_artifact(image_artifact_name)
    if not image_artifact:
        return {"status": "error", "detail": f"Artifact '{image_artifact_name}' not found."}

    image_bytes = image_artifact.part.to_bytes()
    image = Image.open(io.BytesIO(image_bytes))

    # The box_2d coordinates are often normalized, but let's assume they are pixel values for now.
    # The format is [x1, y1, x2, y2].
    cropped_image = image.crop(box_2d)

    # Save the cropped image to a new artifact
    output_buffer = io.BytesIO()
    cropped_image.save(output_buffer, format="PNG")
    output_bytes = output_buffer.getvalue()

    new_artifact_name = f"extracted_{image_artifact_name}"
    await tool_context.save_artifact(
        new_artifact_name,
        types.Part.from_bytes(data=output_bytes, mime_type="image/png"),
    )

    return {
        "status": "success",
        "detail": f"Extracted image saved as artifact '{new_artifact_name}'.",
        "filename": new_artifact_name,
    }



img_element_extractor_agent = Agent(
    model=MODEL,
    name="img_element_extractor_agent",
    description="An agent that extracts text or objects from an image based on user instructions.",
    instruction=prompt.IMG_ELEMENT_EXTRACTOR_PROMPT,
    output_key="img_element_extractor_output",
    tools=[extract_image_region],
)
