# Skill: Media Generator
**Description**: Transforms raw trend data into persona-aligned social media posts and image prompts.
**Input Contract**:
- `trend_data` (dict): The output from the Trend Fetcher.
- `persona_ref` (string): Path to the SOUL.md file.
**Output Contract**:
- `content` (string): The final social media caption.
- `image_prompt` (string): Descriptive prompt for GenAI image tools.