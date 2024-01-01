from datasets import load_dataset, concatenate_datasets

def multiarith_dataset():
    try:
        dataset = load_dataset("ChilleD/MultiArith")

        # データセットのサイズをカウント
        train_data_count = len(dataset['train'])
        test_data_count = len(dataset['test'])
        data_types = ['train','test']
        data_count = [train_data_count, test_data_count]
        return data_types, data_count, dataset

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def multiarith_split(dataset, data_type):
    if data_type == 'train':
        all_dataset = dataset['train']
        num_data = len(all_dataset)
    elif data_type == 'test':
        all_dataset = dataset['test']
        num_data = len(all_dataset)
    else:
        train_dataset = dataset['train']
        test_dataset = dataset['test']
        all_dataset = concatenate_datasets([train_dataset, test_dataset])
        num_data = len(all_dataset)

    data_list = [[example['question'], example['final_ans']] for example in all_dataset]

    return data_list, num_data
