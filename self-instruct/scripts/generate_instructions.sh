batch_dir=${1:-"data/gpt3_generations/"}
num_instructions_to_generate=${2:-50000}

python self_instruct/bootstrap_instructions.py \
    --batch_dir ${batch_dir} \
    --num_instructions_to_generate ${num_instructions_to_generate} \
    --seed_tasks_path data/seed_tasks.jsonl