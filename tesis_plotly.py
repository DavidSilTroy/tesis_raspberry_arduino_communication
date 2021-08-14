import plotly.graph_objects as grob
import numpy as np
import plotly.express as px
from tesis_sqlite import DB_sensors_sql

db_sql = DB_sensors_sql()
doc_name="fsr402_10kg_flat"
data_from_sql = db_sql.get_data_from_column(doc_name,"*")
yi=[]
xi=[]

a=0
for data in data_from_sql:
    a+=1
    xi.append(str(data[0]))
    yi.append(data[1])
    if a>=1000:
        break

dict_of_fig = dict({
    "data": [{"type": "bar",
              "x": xi,
              "y": yi }],
    "marker": {"color":"LightSeaGreen"},
    "layout": {"title": {"text": "A Figure from David Silva xd"}}
})

#fig = grob.Figure(dict_of_fig)
#fig.write_html('first_figure.html', auto_open=True)



#x = np.arange(5)

#figi = grob.Figure(data=grob.Scatter(x=x, y=x**2))
#figi.write_html('second_figure.html', auto_open=True)
#print(type(x))



df = px.data.iris()
#fige = px.scatter_matrix(df)
#fige.show()
print(df)
dfe = px.data.tips()
#fige = px.scatter_matrix(df)
#fige.show()
print(dfe)
print(type(dfe))
figa = px.scatter(dfe, x="total_bill", y="tip", trendline="ols")
figa.write_html('third_figure.html', auto_open=True)