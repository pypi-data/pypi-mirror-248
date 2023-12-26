import json
import lazydl as l
from lazydl.utils.log import Logger


logger = Logger(__name__)



class PsyProcessor(l.BaseProcessor):

    def preprocess_dataset(self, data_file):
        with open(data_file, 'r', encoding='utf8') as f:
            data_list = f.readlines()
        new_data_list = []
        for item in data_list:
            item = json.loads(item)
            input = item['input']
            targets = item['target']
            desc = item['desc']
            prompt = l.load_class("modules.prompt_templates.psy_prompt.Prompt")
            user_inputs = prompt.build_prompt(
                            id=1,
                            history=f"用户：{desc}", 
                            query=input)
            new_data_list.append({"user_inputs": user_inputs, "targets": targets})
        return new_data_list

    def encode_data(self, batch, tokenizer, max_uer_input_length, max_target_length, used_for_eval):
        user_inputs = batch["user_inputs"]
        targets = batch["targets"]
        user_input_ids = self.tokenizer.batch_encode_plus(user_inputs, max_length=self.max_uer_input_length, truncation=True, add_special_tokens=True)["input_ids"]
        target_ids = self.tokenizer.batch_encode_plus(targets, max_length=self.max_target_length, truncation=True, add_special_tokens=False)["input_ids"]
        
        input_ids = [user_input_id + target_ids[idx] + [self.tokenizer.eos_token_id] for idx, user_input_id in enumerate(user_input_ids)]
        
        labels = [[self.tokenizer.pad_token_id] * len(user_input_ids[idx]) + target_id + [self.tokenizer.eos_token_id] for idx, target_id in enumerate(target_ids)]
        
        # 找出batch中的最大长度
        lengths = [len(x) for x in input_ids + labels]
        # 取出batch中的最大长度，如果超过max_seq_length，则取max_seq_length
        batch_max_len = min(max(lengths), self.max_seq_length)
        
        
        for input_index, ids in enumerate(input_ids):
            pad_len = batch_max_len - len(ids)
            input_ids[input_index] = ids + [self.tokenizer.pad_token_id] * pad_len
            labels[input_index] = labels[input_index] + [self.tokenizer.pad_token_id] * pad_len
            
            labels[input_index] = [(l if l != self.tokenizer.pad_token_id else -100) for l in labels[input_index]]
    
        
        result = {
            'input_ids': input_ids,
            'labels': labels,
        }
        
        if self.used_for_eval:
            result["user_inputs"] = user_inputs
            result["references"] = targets

        return result





