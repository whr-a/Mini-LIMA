# Mini-LIMA Assignment

In this assignment, we complete:

1. instruction dataset construction
2. model alignment via supervised fine-tuning(sft)
3. model evaluation

## instruction dataset construction

To generate Self-Instruct data using our own seed tasks, we can run the follow scripts for the entire pipeline. Our code can be tested on the GPT-3.5-turbo model accessible via the [OpenAI API]

Here are the scripts for generating the data:
```bash
# 1. Generate instructions from the seed tasks
# If you want to generate instructions of classification only,add "--use_clf_seed_tasks_only" in the script
./scripts/generate_instructions.sh

# 2. Identify whether the instruction represents a classification task or not
./scripts/is_clf_or_not.sh

# 3. Generate instances for each instruction
./scripts/generate_instances.sh

# 4. Filtering, processing, and reformatting
./scripts/prepare_for_finetuning.sh
```

The final generated data is placed in the dataset directory.
The detailed data generation can be seen in the [`self-instruct/data/README.md`](self-instruct/data/README.md)

## model alignment via supervised fine-tuning(sft)

Fine-tuning process: Move the dataset to the data directory under the LLaMA-Factory directory, then add an entry about this dataset in the dataset_info.json file (if the format is "instruction", "input", "output", you only need to provide the filename corresponding to the dataset name). The provided run.sh script defines the batch size and the steps to run, and running run.sh will start the fine-tuning process.

See the result in results/finetune.

## model evaluation
The evaluation is divided into two steps. The first step is to use the model to generate a model_outputs.json file from the default given instruction. The second step involves calling the gpt-api to use ChatGPT to evaluate the model outputs. To run the evaluation, we need to place our fine-tuned model into the models_configs directory and add the configs.yaml and prompt.txt provided in the job release repository. After modifying the paths in these files, run the last item of the evaluation script from the job release repository to start the evaluation. The evaluation will default to splitting the instruction into chunks of size 64 to generate model outputs group by group. To modify this, we can change the chunksize in the main.py file.

Equivalent to the following script:
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
Specially,the model output predictions is in [`results/evaluate/model_outputs.json`](results/evaluate/model_outputs.json)