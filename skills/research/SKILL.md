---
name: research
description: "Conduct web research via Tavily API with citations. Use when: (1) user asks to research a topic, (2) needs current/real-time information with sources, (3) wants comprehensive analysis of trends/comparisons/market data, (4) requests structured research output. Keywords: research, investigate, find out about, what's the latest on, compare, analyze market"
---

# Research Skill

Run `scripts/research.sh` to conduct web research with automatic source gathering and citations.

## Usage

```bash
scripts/research.sh '{"input": "research topic", "model": "mini|pro|auto"}' [output_file]
```

Run `scripts/research.sh` without arguments for full help.

## Model Selection

- **mini** (~30s): Single-topic questions. "What is X?" "How does Y work?"
- **pro** (~60-120s): Comparisons, multi-angle analysis. "X vs Y" "Best practices for..."
- **auto**: Let API decide based on query complexity

## Structured Output

Add `output_schema` for predictable JSON structure. Every property needs `type` and `description`:

```bash
scripts/research.sh '{
  "input": "top AI startups 2025",
  "model": "pro",
  "output_schema": {
    "properties": {
      "summary": {"type": "string", "description": "Executive summary"},
      "companies": {"type": "array", "description": "Top companies", "items": {"type": "string"}}
    },
    "required": ["summary", "companies"]
  }
}' output.json
```

## Notes

- Takes 30-120 seconds; suggest running in background (Ctrl+B)
- Requires `TAVILY_API_KEY` environment variable
- For timeouts on complex queries: `MAX_WAIT=300 scripts/research.sh ...`
