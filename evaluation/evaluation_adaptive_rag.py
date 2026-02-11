from langchain_core.documents import Document
from agent_adaptive_rag.adaptive_rag_graph_builder import build_adaptive_rag_graph
from evaluation.question_reference import evaluation_set
from langchain_core.messages import HumanMessage
from ragas import SingleTurnSample, RunConfig, evaluate, EvaluationDataset
from ragas.metrics._answer_correctness import answer_correctness
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.metrics._context_precision import context_precision
from ragas.metrics._context_recall import context_recall
from ragas.metrics._faithfulness import faithfulness
from models.models import evaluator_llm, qwen3_embedding_model
from utils.log_utils import log

# ====== set up the naive rag graph and the relevant data lists ======
graph = build_adaptive_rag_graph()
id_category_doctype = []
samples = []

# test
# conv_config = {"configurable":{"thread_id":f"evaluation"}}
# state_1 = graph.invoke({"messages": [HumanMessage(content="")]}, config=conv_config) # trigger the greetings
# state_2 = graph.invoke({"messages": [HumanMessage(content="What is liquidity?")]}, config=conv_config) # get the real reply
# print(state_2["logs"][-1]["generation"])

# ====== let the agent answer prepared questions one by one ======
for item in evaluation_set:
    # ------ get the info from one evaluation item ------
    eval_id = item["id"]
    eval_category = item["category"]
    eval_question = item["question"]
    eval_reference= item["reference"]
    print(f"Start to answer question {eval_id} - {eval_question}")

    # ------ set tup config, each item has its own thread_id ------
    conv_config = {"configurable":{"thread_id":f"evaluation_{eval_id}"}}

    # ------ use the graph to answer the question in the item ------
    state_1 = graph.invoke({"messages": [HumanMessage(content="")]}, config=conv_config) # trigger the greetings
    state_2 = graph.invoke({"messages": [HumanMessage(content=eval_question)]}, config=conv_config) # get the real reply
    last_log = state_2["logs"][-1]
    for log in state_2["logs"]:
        print(log)

    # ------ get retrieved context, a bit complicated for adaptive rag ------
    try:
        retrieved_contexts = []
        info_types = []
        retrieved_documents = last_log.get("retrieved_documents", [])
        for r_d in retrieved_documents:# could be a list of Documents, or dicts that contain Documents
            if isinstance(r_d, Document):
                info_types.append(r_d.metadata.get("info_type"))
                retrieved_contexts.append(r_d.page_content)
            elif isinstance(r_d, dict):
                info_types.append(r_d.get("info_type"))
                documents = r_d.get("documents", [])
                for d in documents:
                    if isinstance(d, Document):
                        retrieved_contexts.append(d.page_content)

        # decide the doctype
        if ("web_search" in info_types) and ("retrieval" not in info_types):
            doctype = "web_search"
        elif ("retrieval" in info_types) and ("web_search" not in info_types):
            doctype = "retrieval"
        elif ("retrieval" in info_types) and ("web_search" in info_types):
            doctype = "retrieval_&_web_search"
        else:
            doctype = "NA"

        generation = last_log.get("generation", "")
        info_type = last_log.get("info_type", "")

        # ------ add the organized info to the lists ------
        id_category_doctype.append(
            {
                "id": eval_id,
                "category": eval_category,
                "doctype":doctype
            }
        )
        samples.append(
            SingleTurnSample(
                user_input=eval_question,
                retrieved_contexts=retrieved_contexts,
                response=generation,
                reference=eval_reference,
            )
        )
    except Exception as e:
        log.error(f"Error when formulating retrieved context for question: {eval_question}: {e}")

# ====== evaluate the results ======
# Configure for stability over speed
run_config = RunConfig(
    timeout=300,      # Increase timeout to 300 seconds (default is 180)
    max_workers=2,    # Reduce parallel jobs (default is 16) to avoid API congestion
    max_retries=3     # Give it more chances to succeed
)
results = evaluate(
    dataset=EvaluationDataset(samples=samples),
    metrics=[context_precision, context_recall, answer_relevancy, faithfulness, answer_correctness],
    llm=evaluator_llm,
    embeddings=qwen3_embedding_model,
    run_config=run_config
)

# ====== Organize and output the results ======
df_results = results.to_pandas()
try:
    df_results["id"] = [item["id"] for item in id_category_doctype]
    df_results["category"] = [item["category"] for item in id_category_doctype]
    df_results["document_type"] = [item["doctype"] for item in id_category_doctype]
    df_results.to_csv("eval_results_adaptive_rag.csv", index=False, encoding="utf-8")
except Exception as e:
    log.error(f"Error when organizing the final results: {e}")
    df_results.to_csv("eval_results_adaptive_rag.csv", index=False, encoding="utf-8")