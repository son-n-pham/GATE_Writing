# GATE_Writing

**Creative writing:** Students use a provided image to write creative pieces following the pre-defined rubric.

**Goal:** To enhance creative writing skills over time by employing an AI-powered workflow, providing consistently educational grading and personalized feedback for writings based on image prompts.

**Tools (all are free):**

- VS Code
- Google Gemini API: Free with experimental LLMs that perform well to meet our requirements
- Several free LLMs in Cline provided by Github's Copilot (including amazing Claude Sonnet 3.5) or by Mistral or very low-cost LLMs provided by DeepSeek.

**Workflow:**

1.  **Input:**
    - A PNG image containing the image prompt for creative writing.
    - Student writing in markdown format with file names structured as `student_{student name}.md`.
2.  **Workflow:**
    1. The extension reads the `system_prompt.md` to obtain the workflow and grading rubric.
    2. _Only if_ there is no markdown file derived from the image prompt, the image is sent to Gemini API to generate a markdown file which will be used as the writing prompt.
    3. The extension then uses the writing prompt, grading rubric, and student writing to grade their work and provide feedback.
    4. Finally, the extension generates an AI model essay, grades this, and produces an output.
3.  **Output:** The output is a grade, a structured markdown report (`grading_{student_name}.md`) that includes scores based on the rubric, direct quotes from the student essay with feedback, and actionable improvement suggestions. This is in addition to an AI generated model essay, and the score for this model essay.

**Demonstration:**
https://youtu.be/KThUVPv7t0A
