from flask import Flask, render_template,request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import orderstrat
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = int(request.form.get('n'))
        mean=int(request.form.get('mean'))
        deviation_percent = float(request.form.get('deviation_percent'))
        std = int(mean * (deviation_percent / 100))
        replenishment = int(request.form.get('replenishment'))
        l1 = float(request.form.get('l1'))
        l2 = float(request.form.get('l2'))
        a1 = float(request.form.get('a1'))/100
        a2 = float(request.form.get('a2'))/100
        alpha=[a1,a2]
        L=[l1,l2]
        results,c1,c2,c3,c4,Demand=orderstrat.calculate(n,mean,std,replenishment,L,alpha)
        plt.hist(Demand[0],bins=n)
        plt.title("Demand Distribution")
        plt.xlabel('Demand')
        plt.ylabel('Frequency')
        plt.savefig('distribution.png')
        plot_img = BytesIO()
        plt.savefig(plot_img, format='png')
        plot_img.seek(0)
        plot_url = base64.b64encode(plot_img.getvalue()).decode()

        plt.close() 

        # Render the DataFrame as an HTML table
        table = results.to_html(index=False)
        case1=c1.to_html(index=False)
        case2=c2.to_html(index=False)
        case3=c3.to_html(index=False)
        case4=c4.to_html(index=False)
        return render_template('index.html', table=table, case1=case1, case2=case2, case3=case3, case4=case4,plot_url=plot_url)
    
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
