import lazydl as l
import torch
import importlib


class LitModel(l.BaseLitModel):
    def __init__(self, config, tokenizer, as_pipeline=False, model=None):
        super(LitModel, self).__init__(config, tokenizer)
        if model is not None:
            self.backbone = model
        else:
            if ':' in self.config.pretrain_model:
                model_processor_name = self.config.pretrain_model.split(':')[0]
                module_path = config.logger_project + '.modules.' + model_processor_name
                try:
                    module = importlib.import_module(module_path)
                except ModuleNotFoundError as r:
                    raise ValueError(f"Please add a processor for this model: {model_processor_name}\n"
                                    f"Error module path：{module_path}")
                processor_name = 'CustomModel'
                processor_class = getattr(module, processor_name)
                pretrain_model = self.config.pretrain_model.split(':')[-1]
                self.backbone = processor_class.from_pretrained(pretrain_model,
                                                                cache_dir=self.config.cache_dir,
                                                                hyparam=config,
                                                                tokenizer=tokenizer,)
                self.backbone.resize_token_embeddings(self.tokenizer.vocab_size)
                self.backbone = self.backbone.train()
            else:
                self.model_type = self.model_mode[config.hf_model_type if not as_pipeline else config.pipline_model_type]
                self.backbone = self.init_pretrained_model(self.model_type)  # 实例化对象
        
            if self.config.get("use_param_noise", False):
                for name, para in self.backbone.named_parameters():
                    self.backbone.state_dict()[name][:] += (torch.rand(para.size()) - 0.5) * config.noise_lambda * torch.std(para)

    def forward(self,
                # batch, seq_len
                input_ids,
                # batch, seq_len
                labels=None,
                # 其他参数或特征
                past_result=None,  # 生成的时候借用此可以省去每次编码
                **other_features  # 如果有其他特征参数，建议加decoder前缀，保持框架一致性
                ):
        result = l.Result()
        # other_features['decoder_stage'] = self.stage
        outputs = self.backbone(input_ids=input_ids,
                                output_hidden_states=True,
                                output_attentions=True,
                                 labels=torch.where(labels == self.tokenizer.pad_token_id, -100, labels) if labels is not None else None,
                                return_dict=True,
                                use_cache=True,
                                # **other_features,
                                )
        if self.stage == 'train':
            loss = outputs[0]
            result.add(loss=loss)
            result.add(labels=labels)
            if isinstance(outputs[-1], l.Result):
                model_result = outputs[-1]
                result.merge_or_update(model_result)
        return result
