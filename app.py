from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def parse_reference_string(ref_string):
    if not ref_string:
        return []
    tokens = [t for t in ref_string.replace(",", " ").split() if t.strip()]
    try:
        return [int(t) for t in tokens]
    except ValueError:
        return tokens


def simulate_fifo(refs, frame_count):
    frames = [-1] * frame_count
    timeline = []
    faults = []
    index = 0

    for page in refs:
        if page in frames:
            faults.append(False)
        else:
            frames[index] = page
            index = (index + 1) % frame_count
            faults.append(True)
        timeline.append(frames.copy())

    return timeline, faults


def simulate_lru(refs, frame_count):
    recency = []
    timeline = []
    faults = []

    for page in refs:
        if page in recency:
            recency.remove(page)
            recency.append(page)
            faults.append(False)
        else:
            faults.append(True)
            if len(recency) < frame_count:
                recency.append(page)
            else:
                recency.pop(0)
                recency.append(page)

        snapshot = ([-1] * (frame_count - len(recency))) + recency.copy()
        timeline.append(snapshot)

    return timeline, faults


def simulate_optimal(refs, frame_count):
    frames = []
    timeline = []
    faults = []

    for i, page in enumerate(refs):
        if page in frames:
            faults.append(False)
        else:
            faults.append(True)
            if len(frames) < frame_count:
                frames.append(page)
            else:
                farthest = -1
                victim = None

                for f in frames:
                    try:
                        nxt = refs.index(f, i + 1)
                    except ValueError:
                        nxt = float('inf')

                    if nxt > farthest:
                        farthest = nxt
                        victim = f

                frames[frames.index(victim)] = page

        snapshot = ([-1] * (frame_count - len(frames))) + frames.copy()
        timeline.append(snapshot)

    return timeline, faults


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json(force=True)

    refs = parse_reference_string(data.get("refs", ""))
    frames = int(data.get("frames", 3))
    alg = data.get("algorithm", "FIFO")

    if not refs or frames < 1:
        return jsonify({"error": "Invalid input"}), 400

    if alg == "FIFO":
        timeline, faults = simulate_fifo(refs, frames)
    elif alg == "LRU":
        timeline, faults = simulate_lru(refs, frames)
    elif alg == "Optimal":
        timeline, faults = simulate_optimal(refs, frames)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({
        "refs": refs,
        "frames": frames,
        "algorithm": alg,
        "timeline": timeline,
        "faults": faults,
        "total_faults": sum(faults)
    })


if __name__ == "__main__":
    app.run(debug=True)
