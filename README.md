# White-Box Hallucination in Large Language Models

Understanding and reducing hallucinations in large language models through controlled experiments.

---

## Overview

Large Language Models (LLMs) often produce confident but incorrect information, commonly referred to as *hallucinations*.  
This project studies hallucinations using a **white-box, hyperparameter-driven approach**, systematically analyzing how controllable training-time and inference-time mechanisms affect model reliability.

Instead of treating the model as a black box, we evaluate and compare:

- Decoding strategies (temperature, top-k, top-p, repetition penalties)
- Retrieval grounding (context-supported generation)
- Parameter-efficient fine-tuning (PEFT / LoRA)
- Combined interventions and their trade-offs

The objective is to identify which interventions improve factual reliability and under what conditions.

---

## Research Questions

1. How do inference-time decoding parameters influence hallucination frequency and confidence?
2. When does fine-tuning reduce hallucinations and when does it not?
3. Which hallucinations originate from the model versus missing context?
4. What are the reliability vs compute trade-offs across mitigation strategies?

---

## Current Status

🚧 **Project initialization phase**

Current work:
- Designing the evaluation pipeline
- Finalizing dataset selection
- Implementing baseline generation and scoring

Experiments, results, and analysis will be added incrementally.

---

## Repository Structure

```

whitebox-hallucination-llms/
│
├── configs/          # experiment configurations
├── datasets/         # dataset loaders & preprocessing
├── src/
│   ├── generation/   # decoding strategies
│   ├── finetuning/   # PEFT / LoRA training
│   ├── evaluation/   # hallucination metrics
│   └── pipeline/     # experiment orchestration
│
├── notebooks/        # exploratory analysis
├── experiments/      # run logs
├── results/          # tables & plots
└── paper/            # research paper source

```

---

## Planned Methodology

We evaluate hallucinations through controlled experiments:

1. Generate baseline outputs
2. Vary decoding parameters
3. Apply fine-tuning interventions
4. Compare reliability metrics
5. Analyze cost vs performance trade-offs

All experiments will be reproducible via configuration files.

---

## Expected Contributions

- Hallucination behavior analysis
- Comparative evaluation of mitigation strategies
- Practical reliability guidelines for LLM deployment
- Reproducible research framework

---

## Authors

- [Sanskar Modi](https://github.com/sanskarmodi8)
- [Aryan Dhanuka](https://github.com/AryanDhanuka10)
- [Priyanshu Kumar Singh](https://github.com/Priyanshu1303d)

**Mentor:** Ashwani Kumar

---

## License

MIT License
