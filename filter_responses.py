import json
import os
import codecs
import re
import csv
import numpy as np


def merge_row(one_row):
    # print("b", one_row)
    max_val = np.max(one_row)
    max_val_idx = np.squeeze(np.where(one_row == max_val))
    if max_val_idx.size > 1:
        return one_row
    # print(max_val_idx)
    if one_row[max_val_idx - 1] > 0:
        target_val = one_row[max_val_idx - 1]
        one_row[max_val_idx - 1] = 0
        one_row[max_val_idx] += target_val

    if max_val_idx < len(one_row) - 1:
        target_val = one_row[max_val_idx + 1]
        one_row[max_val_idx + 1] = 0
        one_row[max_val_idx] += target_val
    # print("a", one_row)
    return one_row


def filter_disagree_one(answers_dict):
    pass


def load_response_jsons():
    answers_dict = dict()

    for sub_root, sub_dirs, sub_files in os.walk(responses_path):
        for one_sub_file in sub_files:
            file_path = os.path.join(sub_root, one_sub_file)

            re_result = filename_pattern.search(one_sub_file)
            context_idx = re_result.group(1)
            worker_id = re_result.group(2)

            with codecs.open(file_path, "r", "utf-8") as json_f:
                answers = json.load(json_f)

            try:
                target_context = answers_dict[context_idx]
            except KeyError:
                answers_dict[context_idx] = dict()
                target_context = answers_dict[context_idx]

            target_context[worker_id] = answers

    return answers_dict


def write_csv_json(answers_dict):
    workers_set = set()
    with codecs.open(output_path + "responses.json", "w", "utf-8") as json_f:
        json.dump(answers_dict, json_f, indent=4)

    with codecs.open(output_path + "responses.csv", "w", "utf-8") as csv_f:
        fieldnames = ["context", "worker",
                      "tfidf_o", "tfidf_t", "hred_o", "hred_t", "vhcr_o", "vhcr_t", "ground_o", "ground_t"]
        csv_writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        csv_writer.writeheader()
        for one_context, one_context_answers in sorted(answers_dict.items(), key=lambda x: int(x[0])):
            for one_worker, one_context_worker_answers in one_context_answers.items():
                workers_set.add(one_worker)
                csv_writer.writerow({"context": one_context, "worker": one_worker,
                                     "tfidf_o": one_context_worker_answers['tfidf']['overall'],
                                     "tfidf_t": one_context_worker_answers['tfidf']['topic'],
                                     "hred_o": one_context_worker_answers['hred']['overall'],
                                     "hred_t": one_context_worker_answers['hred']['topic'],
                                     "vhcr_o": one_context_worker_answers['vhcr']['overall'],
                                     "vhcr_t": one_context_worker_answers['vhcr']['topic'],
                                     "ground_o": one_context_worker_answers['human']['overall'],
                                     "ground_t": one_context_worker_answers['human']['topic']})

    with codecs.open(output_path + "workers.txt", "w", "utf-8") as txt_f:
        for one_worker in workers_set:
            print(one_worker, file=txt_f)


def print_response_json_filename():
    worker_id_set = set()

    for sub_root, sub_dirs, sub_files in os.walk(responses_path):
        for one_sub_file in sub_files:
            re_result = filename_pattern.search(one_sub_file)
            # context_idx = re_result.group(1)
            worker_id = re_result.group(2)
            worker_id_set.add(worker_id)

    for one_worker_id in worker_id_set:
        print(one_worker_id)


def main():
    answers_dict = load_response_jsons()
    write_csv_json(answers_dict)


if __name__ == "__main__":
    responses_path = "./output/response/"
    filename_pattern = re.compile(r'context_([0-9]+?)__res__(.+?)\.json')

    source_filename = os.path.splitext(os.path.basename(__file__))[0]
    output_path = "./{}/".format(source_filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    main()

    # print_response_json_filename()
