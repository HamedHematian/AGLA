import os
import json
import argparse
from tqdm import tqdm
import numpy as np
parser = argparse.ArgumentParser()
parser.add_argument("--gt_files", type=str, default="../data/POPE/coco/coco_pope_popular.json")
parser.add_argument("--gen_files", type=str, default="../output/llava_coco_pope_adversarial_answers_agla_seed1.jsonl")
args = parser.parse_args()

# open ground truth answers
gt_files = [json.loads(q) for q in open(os.path.expanduser(args.gt_files), "r")]

# open generated answers
gen_files = [json.loads(q) for q in open(os.path.expanduser(args.gen_files), "r")]

# calculate precision, recall, f1, accuracy, and the proportion of 'yes' answers
true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0
unknown = 0
total_questions = len(gt_files)
yes_answers = 0
id_list_hal = []
id_list_nohal = []
id_list_all = []
# compare answers
for index, line in enumerate(gt_files):
    idx = line["question_id"]
    gt_answer = line["label"]
    image_id = line['image']
    id_list_all.append(image_id)
    assert idx == gen_files[index]["question_id"]
    gen_answer = gen_files[index]["text"]
    # convert to lowercase
    gt_answer = gt_answer.lower()
    gen_answer = gen_answer.lower()
    # strip
    gt_answer = gt_answer.strip()
    gen_answer = gen_answer.strip()
    # pos = 'yes', neg = 'no'
    if gt_answer == 'yes':
        if 'yes' in gen_answer:
            true_pos += 1
            yes_answers += 1
        else:
            false_neg += 1

    elif gt_answer == 'no':
        if 'no' in gen_answer:
            true_neg += 1
            id_list_nohal.append(image_id)
        else:
            yes_answers += 1
            false_pos += 1
            id_list_hal.append(image_id)
    else:
        print(f'Warning: unknown gt_answer: {gt_answer}')
        unknown += 1
np.savez('image_id.npz', id_list_all = id_list_all, id_list_hal = id_list_hal, id_list_nohal = id_list_nohal)
# calculate precision, recall, f1, accuracy, and the proportion of 'yes' answers
precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1 = 2 * precision * recall / (precision + recall)
accuracy = (true_pos + true_neg) / total_questions
yes_proportion = yes_answers / total_questions
unknown_prop = unknown / total_questions
# report results
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print(f'F1: {f1}')
print(f'Accuracy: {accuracy}')
print(f'yes: {yes_proportion}')
print(f'true_pos: {true_pos}, false_neg: {false_neg}, true_neg: {true_neg}, false_pos: {false_pos}')
print(f'unknow: {unknown_prop}')
