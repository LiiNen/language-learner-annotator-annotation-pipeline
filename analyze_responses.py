import json
import codecs
import numpy as np
import os


def clean_row(one_row):
    original_sum_values = np.sum(one_row)

    # Merge max point
    # print("b", one_row)
    max_val = np.max(one_row)
    max_val_idx = np.squeeze(np.where(one_row == max_val))
    if max_val_idx.size > 1:
        return one_row, max_val_idx[0]
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

    # Remove only one
    non_zero_idxs = np.squeeze(np.where(one_row > 0))
    if 2 == non_zero_idxs.size:
        non_zero_idxs = list(non_zero_idxs)
        non_zero_idxs.remove(max_val_idx)
        non_zero_idx = non_zero_idxs[0]
        one_row[non_zero_idx] = 0

    # Remove answers when the max is over 50%
    target_point = original_sum_values / 2.
    non_zero_idxs = np.squeeze(np.where(one_row > 0))
    if non_zero_idxs.size > 1 and one_row[max_val_idx] > target_point:
        non_zero_idxs = list(non_zero_idxs)
        non_zero_idxs.remove(max_val_idx)
        for non_zero_idx in non_zero_idxs:
            one_row[non_zero_idx] = 0

    return one_row, max_val_idx


def compute_kappa(answers_dict):
    p_value_list = list()
    one_row_list = list()
    output_list = list()

    for one_context_idx, one_context_answers in answers_dict.items():
        if len(one_context_answers) < 2:
            continue

        for one_response_type in response_type_list:
            one_row = np.zeros(6, dtype=np.int32)
            for one_context_worker, one_context_worker_answers in one_context_answers.items():
                one_score = one_context_worker_answers[one_response_type]['overall']
                if one_score < 3:
                    one_score_three_type = 0
                elif one_score > 3:
                    one_score_three_type = 2
                else:
                    one_score_three_type = 1
                # one_row[one_score_three_type] += 1
                one_row[one_score] += 1

            # if np.sum(one_row > 0) > 2:
            #     continue
            one_row, max_val_idx = clean_row(one_row)

            output_list.append("{},{},{}".format(one_context_idx, one_response_type, max_val_idx))
            # print(one_context_idx, one_response_type, max_val_idx)
            one_row_list.append(one_row)

            sum_one_row = np.sum(one_row)
            p_value = (np.sum(one_row * one_row) - sum_one_row) / (sum_one_row * (sum_one_row - 1))
            p_value_list.append(p_value)

    one_mat = np.stack(one_row_list, axis=0)[:, 1:]
    sum_all_answers = np.sum(one_mat, axis=0)
    np.savetxt(output_path + "qwer2.csv", one_mat, fmt="%d", delimiter=",")

    p_bar = sum(p_value_list) / len(p_value_list)
    p_value_vec = sum_all_answers / np.sum(sum_all_answers)
    p_e_bar = np.sum(p_value_vec * p_value_vec)

    kappa_value = (p_bar - p_e_bar) / (1. - p_e_bar)
    print(len(p_value_list))

    with codecs.open(output_path + "context_res_amtscore.csv", "w", "utf-8") as csv_f:
        for one_ele in output_list:
            print(one_ele, file=csv_f)

    return kappa_value, output_list


def main():
    with codecs.open(responses_file_path, "r", "utf-8") as json_f:
        answers_dict = json.load(json_f)

    kappa_value, output_list = compute_kappa(answers_dict)
    print(kappa_value)

    output_dict = dict()
    for one_ele in output_list:
        one_ele_arr = one_ele.split(",")
        with codecs.open(context_files_path_template.format(one_ele_arr[0]), "r", "utf-8") as json_f:
            context = json.load(json_f)
        context_part = context['dialog']
        response_part = context['candidates'][one_ele_arr[1]]
        context_part_list = context_part.split('"')
        # print(len(context_part_list))

        try:
            target_dict = output_dict[one_ele_arr[0]]
        except KeyError:
            output_dict[one_ele_arr[0]] = dict()
            target_dict = output_dict[one_ele_arr[0]]

        target_dict['context1'] = context_part_list[1]
        target_dict['context2'] = context_part_list[3]
        target_dict['context3'] = context_part_list[5]
        target_dict[one_ele_arr[1]] = [response_part, one_ele_arr[2]]

    with codecs.open(output_path + "context_res_amtscore.json", "w", "utf-8") as json_f:
        json.dump(output_dict, json_f, indent=4)


if __name__ == "__main__":
    responses_file_path = "./filter_responses/responses.json"
    response_type_list = ['tfidf', 'hred', 'vhcr', 'human']
    context_files_path_template = "./data/contexts/context_{}.json"

    source_filename = os.path.splitext(os.path.basename(__file__))[0]
    output_path = "./{}/".format(source_filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    main()
