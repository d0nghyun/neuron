# Quant Analyst Output Schema

```json
{
  "hypothesis": "...",
  "analysis_timestamp": "ISO 8601",
  "questions_and_judgments": [
    {
      "question": "Q1. Does this phenomenon exist in the data?",
      "operationalization": "How I made this measurable",
      "my_criterion": "The standard I defined and why",
      "measurement": {
        "method": "How measurement was conducted",
        "result": "...",
        "data_quality_notes": "..."
      },
      "judgment": "YES/NO/MARGINAL",
      "reasoning": "Why I judged this way (comparison of measurement to criterion)",
      "what_could_change_my_mind": ["..."]
    }
  ],
  "synthesis": {
    "overall_judgment": "PROCEED/MODIFY/REJECT",
    "key_insight": "Most important finding",
    "what_would_change_my_mind": ["..."],
    "recommended_next_steps": ["..."]
  }
}
```

## Success Criteria

| Criterion | Validation |
|-----------|------------|
| Questions are specific | Can be measured objectively |
| Criteria are self-defined | Not copied from external standards |
| Criteria are justified | Reasoning for threshold selection is clear |
| Measurements are rigorous | Using appropriate analytical methods |
| Judgments are explicit | YES/NO/MARGINAL with clear reasoning |
| Synthesis is actionable | Recommends clear next steps or decision |
