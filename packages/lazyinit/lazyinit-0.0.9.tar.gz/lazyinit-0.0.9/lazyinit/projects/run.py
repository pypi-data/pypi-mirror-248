import lazydl as l
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from omegaconf import DictConfig
import hydra
import datetime


l.hi()
log = l.Logger(__name__)
current_dir = os.path.dirname(os.path.abspath (__file__))


@hydra.main(version_base="1.2", config_path="configs/", config_name="default_config.yaml")
def main(config: DictConfig) -> float:
    try:
        exp_start = datetime.datetime.now()
        config, experiment = l.init_env(config, current_dir)
        
        # ---------------------------------------------------------------------------- #
        #                         加载模型                                     
        # ---------------------------------------------------------------------------- #
        model, tokenizer = l.load_model_and_tokenizer(config.model_name_or_path, use_qlora=config.use_qlora)
        

        if config.stage != "test":
            # ---------------------------------------------------------------------------- #
            #                            初始化Trainer                                  
            # ---------------------------------------------------------------------------- #
            if config.trainer_type == 'hf':
                trainer = l.HFTrainer(
                    model=model,
                    args=config.hf_args,
                    train_dataset=l.load_data(config, tokenizer, stage="train", return_dataloader=False),
                    compute_loss=config.loss_func_file
                )
                
            elif config.trainer_type == 'lit':
                trainer = l.LitTrainer(config,
                                        model=l.load_class(config.lit_model_file)(config, tokenizer, model=model), 
                                        tokenizer=tokenizer,
                                        train_dataloader=l.load_data(config, tokenizer, stage="train"),
                                        val_dataloader=l.load_data(config, tokenizer, stage="val"),
                                        experiment=experiment,)

                
            else:
                raise ValueError("Unknown trainer type: %s" % config.trainer_type)
            
            pre_end = datetime.datetime.now()
            
            trainer.train()


            # ---------------------------------------------------------------------------- #
            #                         结果保存                                     
            # ---------------------------------------------------------------------------- #
            if config.use_qlora:
                final_save_path = os.path.join(config.output_dir, 'lora_weights')
            else:
                final_save_path = os.path.join(config.output_dir, 'best')
            trainer.save_model(final_save_path)

            if config.use_qlora and config.merge_lora:
                log.info("Merge lora weights to base model!")
                model = l.merge_lora_to_base_model(config.model_name_or_path, final_save_path, config.output_dir + "/best")
            else:
                model = trainer.model.backbone
        
        
        eval_result_str = ""
        
        if config.test_data_file is not None and config.test_data_file != "":
            # ---------------------------------------------------------------------------- #
            #                         测试模型                                     
            # ---------------------------------------------------------------------------- #
            test_dataset = l.load_data(config, tokenizer, stage="test", return_dataloader=False)
            eval_pipline = l.Pipeline(model, tokenizer)
            test_dataset = test_dataset.map(
                    lambda batch: {
                        "model_responses": eval_pipline.generate(**batch)   
                    },
                    batched=True,
                    batch_size=config.test_batch_size,
                    desc="生成中...",
                )
            result= l.get_eval_metrics(test_dataset, config.eval_metrics)
            eval_result_str = result.flatten_to_print()
            
            l.save_as(result, config.output_dir + "/test_result.json")
            
            if experiment:
                log.info("上传测评结果至 Comet.ml ！")
                experiment.log_others(result)
        
        train_or_test_end = datetime.datetime.now()
        
        pre_time_day = (train_or_test_end - exp_start).total_seconds() // 60 // 60 // 24
        pre_time_hour = (train_or_test_end - exp_start).total_seconds() // 60 // 60
        pre_time_minute = (train_or_test_end - exp_start).total_seconds() // 60
        
        run_time_day = (train_or_test_end - exp_start).total_seconds() // 60 // 60 // 24
        run_time_hour = (train_or_test_end - exp_start).total_seconds() // 60 // 60
        run_time_minute = (train_or_test_end - exp_start).total_seconds() // 60
        
        if config.dingding_access_token and config.dingding_secret:
            end_notice = (
                f"{config.task_id} 任务已完成\n"
                f"实验名称：{config.comet_exp_name}\n"
                f"实验备注：{config.memo}\n"
                f"实验准备总耗时：{pre_time_day} 天 {pre_time_hour} 小时 {pre_time_minute} 分钟\n"
                f"实验运行总耗时：{run_time_day} 天 {run_time_hour} 小时 {run_time_minute} 分钟\n"
                f"{eval_result_str}"
            )
            l.notice(end_notice)
    
    except Exception as e:
        error_notice = (
            f"{config.task_id} 任务失败\n"
            f"实验名称：{config.comet_exp_name}\n"
            f"实验备注：{config.memo}\n"
            f"错误信息：{e}"
        )
        l.notice(error_notice)
    
if __name__ == "__main__":
    main()