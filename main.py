from flask import Flask, render_template, request, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io


app = Flask(__name__, static_folder= "static")

@app.route("/", methods = ["GET", "POST"])
def index():
    func = {}
    if request.method == "POST":
        func[request.form["function"]] = True
        funcV = request.form["function"]
        amp  = request.form["amplitude"]
        freq = request.form["frequency"]
        return render_template("index.html", func = func, amp = amp, freq = freq, funcV = funcV)
    else:
        func["cos"] = True
        funcV = "cos"
        amp  = 1
        freq = 1
        return render_template("index.html", func = func, amp = amp, freq = freq, funcV = funcV)

x = np.linspace(0, 2, 1000)
fig, ax = plt.subplots(1, figsize=(10, 4))
@app.route("/image-<string:funcV>,<int:amp>,<int:freq>.png")
def plot_png(funcV = "sin", amp = 1, freq = 1, phase = 0):
    """ renders the plot on the fly.
    """
    plt.suptitle(f'{funcV} Wave')
    ax.clear()
    units = 'amp = {} $(psi)$ \nfreq = {} $(Hz)$'
    if funcV == "sin":
        y = amp * np.sin(freq * 2 * np.pi * x + phase * 2 * np.pi)
    elif funcV == "cos":
        y = amp * np.cos(freq * 2 * np.pi * x + phase * 2 * np.pi)
    elif funcV == "tan":
        y = amp * np.tan(freq * 2 * np.pi * x + phase * 2 * np.pi)
    
    ax.plot(x, y, label=units.format(amp, freq))
    ax.set_xlim(x[0], x[-1])
    ax.legend(loc=1)
    ax.set_xlabel('$(s)$')
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)