MODEL_TYPE_CHOICES = ['huggingface', 'replicate', 'octo']
MODEL_NAMES_MAPPING = {
    'huggingface': ['gpt2', 'bigscience/bloom-560m', 'other'],
    'replicate': ['replicate/llama-7b', 'replicate/llama-13b-lora', 'other'],
    'octo': ['llama-2-7b-chat', 'other'],
}
PROBES_CHOICES = ['Security', 'Toxicity', 'Hallucination', 'Ethics']
PROBES_DIMENSIONS_MAPPING = {
    'Security': 'dan,encoding,gcg,glitch,knownbadsignatures,leakerplay,malwaregen,packagehallucination,promptinject,xss',
    'Toxicity': 'atkgen,continuation,realtoxicityprompts',
    'Hallucination': 'goodside,snowball,misleading,packagehallucination',
    'Ethics': 'lmrc',
}