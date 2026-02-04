import gradio as gr
from langchain_core.messages import HumanMessage
from agent_naive_rag.naive_rag_graph_builder import build_naive_rag_graph

# ========== Set up config and initialize the graph ==========
conv_config = {"configurable":{
    "thread_id":"agent_gui",
    "terminated":False
}}

graph = build_naive_rag_graph()

# ========== Create GUI functions ==========
def do_graph(user_input, chat_bot):
    """
    function to execute after input is submitted
    """
    if user_input:
        chat_bot.append({'role':'user', 'content': user_input})
    return '', chat_bot

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            c.get("text", "")
            for c in content
            if isinstance(c, dict) and c.get("type") == "text"
        )
    return ""

def init_chatbot():
    """
    Trigger the graph once with an empty message to get the greeting
    """
    state = graph.invoke(
        {"messages": [HumanMessage(content="")]},
        config=conv_config
    )
    chat_bot = []
    messages = state.get("messages", [])
    if messages and isinstance(messages, list):
        last_msg = messages[-1]
        if last_msg.__class__.__name__ == "AIMessage" and last_msg.content:
            chat_bot.append({
                "role": "assistant",
                "content": last_msg.content
            })
    return chat_bot

def execute_graph(chat_bot: list[dict]) -> list[dict]:
    """
    function to execute the workflow
    """
    # Skip execution if terminated
    if conv_config["configurable"].get("terminated"):
        return chat_bot

    raw_content = chat_bot[-1]["content"]
    user_input = extract_text(raw_content)

    result = '' #AI assistant last message
    events = graph.stream({"messages": ("user", user_input)}, conv_config, stream_mode = "values")

    for event in events:
        messages = event.get("messages")
        if messages:
            if isinstance(messages, list):
                message = messages[-1]
            if message.__class__.__name__ == "AIMessage":
                if message.content:
                    result = message.content #messages that needs to display in web UI
            msg_repr = message.pretty_repr(html = True)
            if len(msg_repr) > 1500:
                msg_repr = msg_repr[:1500] + "... and more."
            print(msg_repr)
    chat_bot.append({'role': 'assistant', 'content': result})
    return chat_bot

# Build a GUI with gradio
theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="emerald",
    neutral_hue="slate",
    radius_size="md",
    font=["Inter", "sans-serif"]
).set(
    body_background_fill="#f5f7fa",
    block_background_fill="#ffffff",
    block_border_width="1px",
    block_shadow="0 4px 12px rgba(0,0,0,0.08)",
    button_primary_background_fill="#22c55e",
    button_primary_background_fill_hover="#16a34a",
    button_primary_text_color="white",
)

with (gr.Blocks(title='Quantitative Finance Assistant (Naive RAG)', theme=theme) as instance): #set up the page title with css, we have an HTML page
    gr.Label('Quantitative Finance Assistant (Naive RAG)', container=False) #header of the page

    chatbot = gr.Chatbot(height=350, label = 'Assistant') #chatbot widget

    input_textbox = gr.Textbox(label='Please input your question here.📝', value='') #input box

    instance.load(init_chatbot, inputs=None, outputs=chatbot) # Run greeting once on page load

    input_textbox.submit(do_graph,
                         [input_textbox, chatbot],
                         [input_textbox, chatbot]
                         ).then(execute_graph, chatbot, chatbot)

    with gr.Row():
        gr.Column(scale=1)  # empty spacer column
        with gr.Column(scale=0):  # button column, won't stretch
            quit_button = gr.Button("End the chat", elem_id="quit-btn")
    def quit_chat(chat_bot):
        conv_config["configurable"]["terminated"] = True
        chat_bot.append({
            'role': 'user',
            'content': 'End the chat'
        })
        chat_bot.append({
            'role': 'assistant',
            'content':"Thank you for using the Quantitative Finance Assistant. Wish you have a good day!"
        })
        return chat_bot

    quit_button.click(quit_chat, chatbot, chatbot)

if __name__=='__main__':
    #launch the gradio app
    instance.launch(debug=True)