import json
import lazydl as l
from lazydl.utils.log import Logger


logger = Logger(__name__)



class FaithDialProcessor(l.BaseProcessor):

    def preprocess_dataset(self, data_file):
        ori_data = l.load_in(data_file)
        new_data_list = []
        for item in ori_data:
            for uttr in item["utterances"]:
                history = uttr['history']
                ori_response = uttr['original_response']
                knowledge = uttr['knowledge']
                response = uttr['response']
                begin_label = uttr['BEGIN']
                vrm_label = uttr['VRM']
                prompt = l.load_class("modules.faith_dial.faithdial_prompt.Prompt")
                user_inputs = prompt.build_prompt(
                                history=history,
                                knowledge=knowledge)
                new_data_list.append({"user_inputs": user_inputs, "targets": response})
        return new_data_list

    def encode_data(self, batch):
        user_inputs = batch["user_inputs"]
        targets = batch["targets"]
        user_input_ids = self.tokenizer.batch_encode_plus(user_inputs, max_length=self.max_uer_input_length, truncation=True, add_special_tokens=True)["input_ids"]
        target_ids = self.tokenizer.batch_encode_plus(targets, max_length=self.max_target_length, truncation=True, add_special_tokens=False)["input_ids"]
        
        input_ids = [user_input_id + target_ids[idx] + [self.tokenizer.eos_token_id] for idx, user_input_id in enumerate(user_input_ids)]
        
        labels = [[self.tokenizer.pad_token_id] * len(user_input_ids[idx]) + target_id + [self.tokenizer.eos_token_id] for idx, target_id in enumerate(target_ids)]

        result = {
            'input_ids': input_ids,
            'labels': labels,
        }
        
        if self.used_for_eval:
            result["user_inputs"] = user_inputs
            result["references"] = targets

        return result





