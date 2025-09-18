# Revised Workflow Plan

1.  **Step 1: Analyze the Blueprint (`logo_create` sub-agent)**
    *   **Action:** I will analyze the structure and content of the `logo_create` sub-agent to use as a blueprint.
    *   **Review:** I will present my findings to you. Since this step involves no code changes, there will be no commit.

2.  **Step 2: Create the New Sub-Agent's File Structure**
    *   **Action:** I will create the `marketing_agency/sub_agents/img_element_extractor` directory and the initial empty files: `__init__.py` and `img_element_extractor.py`.
    *   **Review:** I will then pause for your review of the new file structure.
    *   **Commit:** Upon your approval, I will commit the changes with the message: `feat: Initial structure for img_element_extractor agent`.

3.  **Step 3: Implement the `img_element_extractor_agent`**
    *   **Action:** I will write the code in `img_element_extractor.py` to define and instantiate the `google.adk.Agent` named `img_element_extractor_agent`, including its system prompt and parameters.
    *   **Review:** I will then show you the implemented code for your review.
    *   **Commit:** Upon your approval, I will commit the changes with the message: `feat: Implement img_element_extractor_agent`.

4.  **Step 4: Integrate the New Sub-Agent**
    *   **Action:** I will modify the main agent engine file (e.g., `agent_engine_app.py`) to import and register the new `img_element_extractor_agent`.
    *   **Review:** I will show you the modifications for your final review.
    *   **Commit:** Upon your approval, I will commit the integration with the message: `feat: Integrate img_element_extractor_agent into engine`.
