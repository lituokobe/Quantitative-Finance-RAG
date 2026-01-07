from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.metrics._answer_correctness import answer_correctness
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.metrics._context_precision import context_precision
from ragas.metrics._context_recall import context_recall
from ragas.metrics._faithfulness import faithfulness
from ragas.run_config import RunConfig
from models.models import evaluator_llm, qwen3_embedding_model

# TODO: Prepare data
user_input1 = "湖人队三连冠的关键因素是什么？"
retrieved_contexts1 = ["湖人队有奥尼尔和科比两大巨星能够通力合作，尽管略有间隙，但是在比赛的关键时刻，还是能够拥有十分高超的默契。"]
response_lines1 = [
    "内线霸主沙奎尔·奥尼尔的存在，他在三连冠期间三次获得总决赛MVP",
    "科比·布莱恩特的成长和关键时刻的表现",
    "主教练菲尔·杰克逊非常出色",
    "当时的NBA联盟希望打造王朝球队，裁判判罚有时对湖人有利",
]
response1 = "\n".join(response_lines1)  # 正确连接
reference1 = "湖人阵中有奥尼尔和科比两位天才球星，主教练菲尔杰克逊也十分优秀。此外，联盟需要树立一个榜样，裁判对湖人一直很照顾。"

sample1 = SingleTurnSample(
    user_input=user_input1, # 用户问题
    retrieved_contexts=retrieved_contexts1, # 检索到的上下文
    response=response1, # AI生成的响应
    reference=reference1, # 参考答案
)

user_input2 = "2000年以来历届奥运会在哪里举办？"
retrieved_contexts2= ["奥运会每四年一届，1992年以来，先后在巴塞罗那、亚特兰大、悉尼、雅典、北京、伦敦等城市举办。其中北京奥运会的开幕式被誉为最佳开幕式。"]
response2 = "2000年在悉尼举办，2004年在雅典举办。2008年在北京举办，2012年在伦敦举办，2016年在里约热内卢举办，2020年在东京举办，2024年在巴黎举办。"

reference2 = "奥运会每四年一届，2000年在悉尼举办，2004年在雅典举办。2008年在北京举办，2012年在伦敦举办，2016年在里约热内卢举办，2020年在东京举办，但延迟到了2021年， 2024年在巴黎举办， 2028年将在洛杉矶举办。"

sample2 = SingleTurnSample(
    user_input=user_input2,
    retrieved_contexts=retrieved_contexts2,
    response=response2,
    reference=reference2,
)

dataset = EvaluationDataset(samples=[sample1, sample2])

# TODO: Evaluate


# Configure for stability over speed
run_config = RunConfig(
    timeout=300,      # Increase timeout to 300 seconds (default is 180)
    max_workers=2,    # Reduce parallel jobs (default is 16) to avoid API congestion
    max_retries=3     # Give it more chances to succeed
)

results = evaluate(
    dataset=dataset,
    metrics=[context_precision, context_recall, answer_relevancy, faithfulness, answer_correctness],
    llm=evaluator_llm,
    embeddings=qwen3_embedding_model,
    run_config=run_config
)

df = results.to_pandas()
df["question"] = [s.user_input for s in dataset.samples]
print(df[[
    "question",
    "context_precision",
    "context_recall",
    "answer_relevancy",
    "faithfulness",
    "answer_correctness"
]].round(3))

cp_score0 = results["context_precision"][0]
cr_score0 = results["context_recall"][0]
ar_score0 = results["answer_relevancy"][0]
af_score0 = results["faithfulness"][0]
ac_score0 = results["answer_correctness"][0]

cp_score1 = results["context_precision"][1]
cr_score1 = results["context_recall"][1]
ar_score1 = results["answer_relevancy"][1]
af_score1 = results["faithfulness"][1]
ac_score1 = results["answer_correctness"][1]

print(f"全部结果：{results}")
print(f"第一条结果")
print(f"上下文精度: {cp_score0:.3f}")
print(f"上下文召回率: {cr_score0:.3f}")
print(f"答案相关性: {ar_score0:.3f}")
print(f"答案忠诚度: {af_score0:.3f}")
print(f"答案正确性: {ac_score0:.3f}")
print(f"第二条结果")
print(f"上下文精度: {cp_score1:.3f}")
print(f"上下文召回率: {cr_score1:.3f}")
print(f"答案相关性: {ar_score1:.3f}")
print(f"答案忠诚度: {af_score1:.3f}")
print(f"答案正确性: {ac_score1:.3f}")