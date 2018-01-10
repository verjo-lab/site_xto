from flask import Flask, render_template
import pandas as pd
app = Flask(__name__)

df = pd.read_excel('/home/lucas/PycharmProjects/untitled2/static/data/S2_Table Genomic location of lncRNAs.xlsx')
df.insert(0, 'GeneID', df['geneID'])
del (df['geneID'])



@app.route('/')


def lncrba_xto():

        col = df.columns.values
        for n, name in enumerate(col):
            if name == "blockCount" :
                    col[n]= 'Number of exons'



        dados = df.values
        tamanho_total =  df.shape[0]
        add_per_loading = float(100.0/df.shape[0])
        updates_in = range(0, df.shape[0], df.shape[0]/10 )
        print add_per_loading
        url_gb = "http://schistosoma.usp.br/cgi-bin/hgTracks?hgS_doOtherUser=submit&hgS_otherUserName=localadmin&hgS_otherUserSessionName=PLOSPathogensSubmitted&position="

        return render_template('lncrna_xto.html', col=col,
                               dados=dados,
                               per_iteration = add_per_loading,
                               up=updates_in,
                               tamanho_total=tamanho_total,
                               url_gb=url_gb)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
