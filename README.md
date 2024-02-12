# Summarization with LLMs

This repository contains code for utilizing Large Language Models (LLMs) to summarize documents. It also includes a method for evaluating the quality of summarization, inspired by the concepts presented in this paper: [Link to the Paper](https://arxiv.org/pdf/2004.04228.pdf).

## Getting Started

### Build Docker Image

```bash
docker build -t summarization_app .
```

### Run the container:
```bash
docker run -it -p 8080:8080 summarization_app
```
### Make a POST Request:
```bash
curl -X POST "http://localhost:8080/summarize" -H "Content-Type: application/json" -d '{"text": "Falcon comes in two sizes — 7 billion parameters (called Falcon-7B) and 40 billion parameters (called Falcon 40B). Each of the two sizes has two versions: (i) base, which has been pre-trained on large corpuses of text and can be fine-tuned on downstream tasks and (ii) instruct, which has already been fine-tuned on instructions, making it, in our view favorable for out-of-the-box chatbot and Q&A applications."}'
```
### Expected Result:
```bash
{"summary":"Falcon is a language model available in two sizes, with two versions each. The instruct version, which is pre-trained on instructions, is recommended for chatbot and Q&A applications.","score":0.6}
```
