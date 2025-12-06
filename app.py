import gradio as gr
#sets up the rang of available numbers 1-100, and sets up the the state data for values of binary search
numbers = range(1, 101)
state_data = gr.State({"low": 1, "high": 100, "mid": 50, "targ": None})
#function for starting new binary search, activated when place order button hit
def place_order(state_data, target):
    state_data["low"] = 1
    state_data["high"] = 100
    state_data["mid"] = 50
    state_data["targ"] = target
    return graph(state_data), state_data["mid"]
#function that checks if you hit the correct button (less, more, yes) advances the binary search by a step if correct and updates the graph. also congratulates user when reaching "yes"
def steps(button, state_data, target):
    if state_data["targ"] == None:
        state_data["targ"] = target
    if button == "LESS":
        if state_data["mid"] < state_data["targ"] or state_data["mid"] == state_data["targ"]:
            raise gr.Error("INCORRECT", print_exception=False)
        binary_search(state_data)
    elif button == "MORE":
        if state_data["mid"] > state_data["targ"] or state_data["mid"] == state_data["targ"]:
            raise gr.Error("INCORRECT", print_exception=False)
        binary_search(state_data)
    else:
        if not state_data["mid"] == state_data["targ"]:
            raise gr.Error("INCORRECT", print_exception=False)
        gr.Info("The chef has found the correct amount of burgs to make you! Try placing a new order.")
    return state_data["mid"], graph(state_data)
#function for advancing the steps of binary search
def binary_search(state_data):
    middle = (state_data["low"] + state_data["high"]) // 2
    target = state_data["targ"]
    if middle < target:
        state_data["low"] = middle + 1
    elif middle > target:
        state_data["high"] = middle - 1
    else:
        pass
    middle = (state_data["low"] + state_data["high"]) // 2
    state_data["mid"] = middle
#function for updating graph based on new high, low, and mid values
def graph(state_data, empty=False):
    cells = []
    if empty:
        for n in numbers:
            cells.append(f"<div style='color:white;'>{n}</div>")
        grid = (
        "<div style='display:grid;"
        "grid-template-columns: repeat(10, 1fr);"
        "gap:5px;font-size:20px'>"
        + "".join(cells)
        + "</div>"
        )
        return grid
    
    lower=state_data["low"]
    higher=state_data["high"]
    target=state_data["targ"]
    middle=state_data["mid"]
    
    for n in numbers:
        
        if n == target: 
                cells.append(f"<div style='color:lime;font-weight:bold'>{n}</div>")
        elif n == middle: 
                cells.append(f"<div style='color:yellow;font-weight:bold'>{n}</div>")
        elif n == lower: 
                cells.append(f"<div style='color:red;font-weight:bold'>{n}</div>")
        elif n == higher: 
                cells.append(f"<div style='color:red;font-weight:bold'>{n}</div>")
        else:
            cells.append(f"<div style='color:white;'>{n}</div>")

    grid = (
        "<div style='display:grid;"
        "grid-template-columns: repeat(10, 1fr);"
        "gap:5px;font-size:20px'>"
        + "".join(cells)
        + "</div>"
    )
    return grid
#gradio stuff
with gr.Blocks() as demo:
    
    state_data = gr.State({"low": 1, "high": 100, "mid": 50, "targ": None})
    gr.HTML("<h1 style='color: white'>Welcome to Fishburger how many burger you want?</h1>")
    graph_image = gr.HTML(graph(state_data, True))
    with gr.Row():
        request = gr.Slider(minimum=1, step=1, precision=0, label="I want this many burgs")
        order = gr.Button("Place Order")
        response = gr.Textbox(label="SO_THIS_MANY_BURGS?")
        order.click(place_order, inputs=[state_data, request], outputs=[graph_image, response])
    with gr.Row():
        fish = gr.Image("fish.png", show_label=False, container=False, buttons=[""])
        with gr.Column():
            less = gr.Button("LESS").click(lambda n, x: steps("LESS", n, x), inputs=[state_data, request], outputs=[response, graph_image])
            yes = gr.Button("YES").click(lambda n, x: steps("YES", n, x), inputs=[state_data, request], outputs=[response, graph_image])
            more = gr.Button("MORE").click(lambda n, x: steps("MORE", n, x), inputs=[state_data, request], outputs=[response, graph_image])
        rob = gr.Image("robot.png", show_label=False, container=False, buttons=[""])
    gr.Button("RESET").click(None, None, None, js="() => location.reload()")

demo.launch(css=".gradio-container {background-color: #00188F}")