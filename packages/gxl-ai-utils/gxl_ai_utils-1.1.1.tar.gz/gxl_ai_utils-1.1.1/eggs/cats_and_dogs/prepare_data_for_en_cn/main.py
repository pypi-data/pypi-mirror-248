import glob
import os
import random
import sys

import tqdm

sys.path.append('/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils')
from gxl_ai_utils.utils import utils_file


def do_get_all_shard_list_for_data4w():
    """"""
    input_dir = '/home/41_data/data4w/shard_1'
    output_dir = '/home/work_nfs6/xlgeng/data/asr_data_shard_list'
    utils_file.makedir_sil(output_dir)
    # 得到一级子目录
    all_child_dir = os.listdir(input_dir)
    print(all_child_dir)
    for child_dir in tqdm.tqdm(all_child_dir, total=len(all_child_dir)):
        now_dir = utils_file.join_path(input_dir, child_dir)
        tar_list = glob.glob(os.path.join(now_dir, '*.tar'))
        output_path = utils_file.join_path(output_dir, child_dir, 'shard_list.txt')
        utils_file.write_list_to_file(tar_list, output_path)


def do_get_all_raw_list_for_data4w():
    """"""
    input_dir = '/home/work_nfs5_ssd/hfxue/data/data4w/source_1'
    output_dir = '/home/work_nfs6/xlgeng/data/asr_data_raw_list'
    utils_file.makedir_sil(output_dir)
    # 得到一级子目录
    all_child_dir = os.listdir(input_dir)
    print(all_child_dir)
    for child_dir in tqdm.tqdm(all_child_dir, total=len(all_child_dir)):
        now_dir = utils_file.join_path(input_dir, child_dir)
        print(now_dir)
        wav_scp_path = os.path.join(now_dir, 'wav.scp')
        text_path = os.path.join(now_dir, 'text')
        if os.path.exists(wav_scp_path) and os.path.exists(text_path):
            output_path = utils_file.join_path(output_dir, child_dir, 'data.list')
            utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_path, text_path, output_path)
        else:
            print(f'{wav_scp_path} or {text_path} do not exist')


def cut_train_test():
    input_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/data/asr_data_shard/shard.list"
    all_list = utils_file.load_list_file_clean(input_path)
    train_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/data/asr_data_shard/train.list"
    test_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/data/asr_data_shard/test.list"
    dev_path = "/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/data/asr_data_shard/dev.list"
    train_list = all_list[:int(len(all_list) * 0.8)]
    test_list = all_list[int(len(all_list) * 0.8):int(len(all_list) * 0.9)]
    dev_list = all_list[int(len(all_list) * 0.9):]
    utils_file.write_list_to_file(train_list, train_path)
    utils_file.write_list_to_file(test_list, test_path)
    utils_file.write_list_to_file(dev_list, dev_path)


def train_aslp_data():
    aslp_data = utils_file.AslpDataset()
    aslp_data.print_all_keys()
    info_1 = aslp_data.get_path_info_by_key_or_id(65)  # asru
    print(info_1)
    info_2 = aslp_data.get_path_info_by_key_or_id(27)  # librispeech
    print(info_2)
    info_3 = aslp_data.get_path_info_by_key_or_id(38)  # aishell2
    print(info_3)
    list_path_1 = info_1['shard_list']
    list_path_2 = info_2['shard_list']
    list_path_3 = info_3['shard_list']
    # output_dir = '/home/work_nfs7/yhliang/wenet-main/examples/aishell/s0/data/asr_data_shard'
    # utils_file.makedir_sil(output_dir)
    # list_1 = utils_file.load_list_file_clean(list_path_1)
    # list_2 = utils_file.load_list_file_clean(list_path_2)
    # list_3 = utils_file.load_list_file_clean(list_path_3)
    # list_1.extend(list_2)
    # list_1.extend(list_3)
    # random.shuffle(list_1)
    # utils_file.write_list_to_file(list_1, os.path.join(output_dir, 'shard.list'))
    utils_file.print_list(utils_file.load_list_file_clean(list_path_1))
    utils_file.print_list(utils_file.load_list_file_clean(list_path_2))
    # utils_file.print_list(utils_file.load_list_file_clean(list_path_3))


def get_text_for_test():
    input_path = "/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/kd_model/data/AISHELL-2"
    test_list = utils_file.load_dict_list_from_jsonl(os.path.join(input_path, 'test.list'))
    text_dict = {}
    for item in test_list:
        key = item['key']
        text = item['txt']
        text_dict[key] = text
    utils_file.write_dict_to_scp(text_dict, os.path.join(input_path, 'test.text'))


def get_test_files_for_asru():
    aslp_data = utils_file.AslpDataset()
    info_1 = aslp_data.get_path_info_by_key_or_id(65)
    wav_scp_file = info_1['wav_scp']
    text_file = info_1['text']
    data_list = utils_file.do_convert_wav_text_scp_to_jsonl(wav_scp_file, text_file)
    random.shuffle(data_list)
    test_list = data_list[:int(len(data_list) * 0.1)]
    utils_file.write_dict_list_to_jsonl(test_list, '/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/data/asru_test.list')
    text_dict = {}
    for item in test_list:
        key = item['key']
        text = item['txt']
        text_dict[key] = text
    utils_file.write_dict_to_scp(text_dict, '/home/work_nfs7/xlgeng/workspace/wenet-sanm/examples/aishell/en_cn/data/asru_test_text')


if __name__ == '__main__':
    """"""
    # do_get_all_shard_list_for_data4w()
    # do_get_all_raw_list_for_data4w()
    # cut_train_test()
    # get_text_for_test()
    # train_aslp_data()
    get_test_files_for_asru()