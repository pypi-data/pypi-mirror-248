import lazydl as l

    
test_pip = l.Pipeline(model_name_or_path="THUDM/chatglm2-6b-32k", use_qlora=False)
resp = test_pip.generate(["Round[0]\n\n问：你好\n\n答：", "Round[0]\n\n问：我很开心遇到你\n\n答："])

eval_input = l.Result(
    model_responses=resp.model_responses,
    references=["你好", "你好"],
    bert_score_references=["你好", "你好"],
    meteor_references=["你好", "你好"],
)

eval_metrics = ["meteor", "sent_bleu", "dist"]

result= l.get_eval_metrics(eval_input, eval_metrics)

print(resp.model_responses)

