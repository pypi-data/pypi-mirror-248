from datasets import load_dataset

def gsm8k_dataset(data_type='train'):
    try:
        # GSM8Kデータセットのロード
        dataset = load_dataset("gsm8k", "main", split=data_type)

        # データセットのサイズをカウント
        count = len(dataset)
        data_list = [[example['question'], example['answer'].split('#### ')[1]] for example in dataset]
        return count, data_list

    except Exception as e:
        print(f"Error occurred: {e}")
        return None
