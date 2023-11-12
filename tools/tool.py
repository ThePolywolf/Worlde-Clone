import json

# draw history
def draw_history():
    # get history
    with open("stats.json", "r") as json_file:
        history = json.load(json_file)
    
    # lengths
    h_lengths = []
    max_length = 0

    for key in history:
        h_lengths.append(int(history[key]))
        if int(history[key]) > max_length:
            max_length = int(history[key])

    # draw bars
    for i in range(11):
        l = str(i + 1)
        if l == "11":
            l = "X"
        
        if len(l) < 2:
            l = l + " "

        w = 1
        if h_lengths[i] > 0:
            w = 1 + (18 * 2 - 4) * 20 * h_length[i] / max_length
        
        # print results
        print(l + " " + str(h_lengths[i]) + " " + str(w))

draw_history()