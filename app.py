from flask import Flask, render_template, request
from algorithms import simulate_fifo, simulate_lru, simulate_optimal

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            refs_raw = request.form.get('refs','').strip()
            refs = [int(x.strip()) for x in refs_raw.replace(';',',').split(',') if x.strip()!='']
            frames = int(request.form.get('frames', '3'))
            algo = request.form.get('algorithm','FIFO')
            if algo == 'FIFO':
                timeline, metrics = simulate_fifo(refs, frames)
            elif algo == 'LRU':
                timeline, metrics = simulate_lru(refs, frames)
            elif algo == 'Optimal':
                timeline, metrics = simulate_optimal(refs, frames)
            else:
                timeline, metrics = [], {}
            result = {'timeline': timeline, 'metrics': metrics, 'algorithm': algo}
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
