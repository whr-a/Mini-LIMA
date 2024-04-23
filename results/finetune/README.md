---
license: other
base_model: /home/whr-a/llm/hw2/modelscope_hub/qwen/Qwen1___5-0___5B
tags:
- llama-factory
- full
- generated_from_trainer
model-index:
- name: qwen_sft
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# qwen_sft

This model is a fine-tuned version of [/home/whr-a/llm/hw2/modelscope_hub/qwen/Qwen1___5-0___5B](https://huggingface.co//home/whr-a/llm/hw2/modelscope_hub/qwen/Qwen1___5-0___5B) on the qwen_data dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 1e-05
- train_batch_size: 2
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 32
- total_train_batch_size: 64
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_steps: 100
- training_steps: 5000

### Training results



### Framework versions

- Transformers 4.39.3
- Pytorch 2.2.2+cu121
- Datasets 2.18.0
- Tokenizers 0.15.2
