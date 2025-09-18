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

from google.adk import Agent

from . import prompt

img_element_extractor_agent = Agent(
    model=MODEL,
    name="img_element_extractor_agent",
    description="An agent that extracts text or objects from an image based on user instructions.",
    instruction=prompt.IMG_ELEMENT_EXTRACTOR_PROMPT,
    output_key="img_element_extractor_output",
)
