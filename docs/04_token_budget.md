# Tokenbudget (design)

## Princip
- Default: ingen cloud-LLM
- Local LLM (Ollama) når det giver værdi
- Cloud LLM først senere og kun med budget-guards

## Logging (når vi får AI-lag)
- timestamp
- feature
- model
- input_tokens
- output_tokens

## Budget-guards
- Soft cap: forkort prompts, mindre output, cache
- Hard cap: fald tilbage til rules/heuristics
