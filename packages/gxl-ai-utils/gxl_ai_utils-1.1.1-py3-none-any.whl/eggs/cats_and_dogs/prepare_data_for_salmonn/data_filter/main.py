import torch

from gxl_ai_utils.utils import utils_file

if __name__ == "__main__":
    """"""
    # print('hello gxl')
    # from gxl_ai_utils.config.gxl_config import GxlNode
    # args = utils_file.load_dict_from_yaml('./args_data.yaml')
    # args = GxlNode(args)
    # configs = utils_file.load_dict_from_yaml('./configs_data.yaml')

    input_data = torch.randn(32, 1200)
    for i, data in enumerate(input_data):
        # data = tensor = torch.tensor([1.0, 2.0, float('inf'), float('-inf'), float('nan'), 3.0])
        print(data.shape, i)
        condition = torch.any(torch.isinf(data)) or torch.any(torch.isnan(data))
        print(condition)
        print(bool(condition))
        utils_file.write_list_to_file(['1', '2', '3'], '1.txt')
