from .dataset.gsm8k import gsm8k_dataset, gsm8k_split
from .dataset.multiarith import multiarith_dataset, multiarith_split
import random


class LLMdataset:
    def __init__(
        self,
        dataset_name = None
        ):
        self.dataset_name = dataset_name
        if self.dataset_name:
            data_types, data_count, self.dataset = self._select_dataset()
            print(f"Data types:{data_types}")
            print(f"Number of data:{data_count}")

    def _select_dataset(self):
        if self.dataset_name == 'gsm8k':
            data_types, data_count, dataset = gsm8k_dataset()
            return data_types, data_count, dataset
        elif self.dataset_name == 'multiarith':
            data_types, data_count, dataset = multiarith_dataset()
            return data_types, data_count, dataset


    def _split_dataset(self, data_type):
        if self.dataset_name == 'gsm8k':
            data_list = gsm8k_split(self.dataset, data_type)
            return data_list
        elif self.dataset_name == 'multiarith':
            data_list = multiarith_split(self.dataset, data_type)
            return data_list


    def dataloader(self, data_type = None, batch_size=1, seed=None, max_data=5):
        self.data_list, self.num_data = self._split_dataset(data_type)

        if seed is not None:
            random.seed(seed)

        # 現在のデータセットのサイズと max_data を比較
        if max_data is not None and max_data > self.num_data:
            raise ValueError(f"max_data ({max_data}) cannot be greater than the size of the dataset ({self.num_data}).")

        if max_data is not None:
            data_list = random.sample(self.data_list, max_data)
        else:
            data_list = self.dataset[:max_data]

        # バッチサイズでデータセットを分割し、ジェネレータとして提供
        for i in range(0, len(data_list), batch_size):
            yield data_list[i:i + batch_size]


