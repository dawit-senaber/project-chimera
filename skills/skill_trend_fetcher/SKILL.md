# Skill: Trend Fetcher
**Description**: Scrapes and analyzes high-velocity social trends within the Ethiopian digital niche.
**Input Contract**:
- `niche` (string): The category to research (e.g., "fashion", "tech").
- `depth` (int): Number of sources to analyze.
**Output Contract**:
- `trends` (list): Array of objects containing `topic` and `score`.
- `timestamp` (string): ISO format of fetch time.