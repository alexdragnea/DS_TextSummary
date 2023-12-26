# Project Overview

## BART-Large Model

### Introduction
[BART (Bidirectional and Auto-Regressive Transformers)](https://huggingface.co/facebook/bart-large-cnn) from *Facebook* is a *LLM* (Large Language Model), a transformer-based model designed for sequence-to-sequence tasks in NLP. The "BART-Large" variant refers to a larger version of the BART model with increased capacity and capabilities, making it well-suited for complex text generation tasks. The bidirectional nature of BART enables it to capture information from both directions, making it well-suited for tasks like summarization.

A critical component in NLP, the tokenizer is responsible for converting raw text into a format suitable for machine learning models. The tokenizer splits input text into tokens, such as words or subwords, and transforms them into numerical representations that the model can understand.

## Project Goal

This project aims to use *BART-Large-CNN* model for abstractive summarization.Abstractive summarization is a method that involves creating concise and coherent summaries that accurately summarize the key information from the input text.

### Achievements :
-   #### Build a dataset from scratch using public API's.

Dataset used for training can be found [here](https://huggingface.co/datasets/alexdg19/reddit_summaries). It has 10k rows that were used for training and 2k rows used for evaluation. The dataset was builded using [Cohere API](https://cohere.com) and Reddit API. Basically, we used Reddit API to fetch posts and comments from top 100 sub reddits and we used [Cohere API](https://cohere.com) to generate summaries. Code for generating dataset is hosted [here](https://github.com/alexdragnea/Ds_TextSummary/blob/main/dataset/dataset-generator.py). 

-   #### Fine tunining *BART-Large-CNN* on our own dataset and obtain decent ROGUE metrics.

Training occured on *Google Colab*. We used a batch size of 3 with 5 epochs. Training results are hosted on [HuggingFace](https://huggingface.co/alexdg19/bart-large-cnn-reddit-summary-v2) along with the results. To assess the quality of generated summaries, the *ROUGE* metric was employed. *ROUGE* evaluates the overlap between the model-generated summaries and reference summaries, providing insights into the summarization performance. The notebook used for training can be found [here](https://github.com/alexdragnea/Ds_TextSummary/blob/main/train/train.ipynb)

-   #### Serving the fine tuned model through a Flask web app.

The interaction with the model is done via a web app, where users can request summaries for their given input. The ratios that controls the max and min lenght of the summaries are defined in the app.py. 

-   #### Automate the process of dockerizing the app and publish it to *DockerHub* using *GiHub Actions*.

With this workflow, we assure that at every code changes the app is packed as a docker image and uploaded to *DockerHub* with the latest tag. 

-   #### Automate the deploy and the orchestration on *Google Kubernetes Engin* using *GitHub Actions*.

A *MLOps Pipeline* was used with GitHub Actions to deploy the app. The processes from the MLOps pipeline are: 
1. Building latest docker image and pushing it to DockerHub in order to have the latest version of the app (important for code changes).
2. Logging to Google Cloud Console and applying deployment, service and hpa files.
3. Separated workflows for applying or deleting kubernetes resources.
    
The model is served on a *GKE autopilot* cluster as a web server, using CPU workloads. We employed *Liveness*, *Readiness* probes and *Horizontal Pod Autoscaling*, making it a real production ready project.

 

Note: Currently, all *GitHub* workflows are triggered manually to avoid costs but with a single line of code, the workflows can be triggered automatically at a single push.

