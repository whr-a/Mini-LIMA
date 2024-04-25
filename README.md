# Mini-LIMA Assignment

In this assignment, we complete:

1. instruction dataset construction
2. model alignment via supervised fine-tuning(sft)
3. model evaluation

## instruction dataset construction

Corresponding self_structure in the depository.

The generated data is placed in the dataset directory.

## model alignment via supervised fine-tuning(sft)

Add dataset to LLaMA-Factory and run run.sh. See the result in results/finetune.

## model evaluation

```
# use HF mirror endpoint so that you can access the datasets properly on DSW notebook.
export HF_ENDPOINT=https://hf-mirror.com

# copy your model config into alpaca folder
cp -r mini_lima/ alpaca_eval/src/alpaca_eval/models_configs/

alpaca_eval evaluate_from_model \
  --model_configs 'mini_lima' \
  --annotators_config 'chatgpt'
```

See the result in results/evaluate.

