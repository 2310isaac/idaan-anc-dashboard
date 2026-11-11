import pandas as pd, streamlit as st, plotly.express as px

st.set_page_config(page_title="IDAAN · Agua no contabilizada", layout="wide")
NOMBRES = {"ARRAIJAN":"Arraiján","BOCAS DEL TORO":"Bocas del Toro","CHIRIQUI":"Chiriquí","COCLE":"Coclé",
           "COLON":"Colón","HERRERA":"Herrera","LOS SANTOS":"Los Santos","PANAMA ESTE Y DARIEN":"Panamá Este y Darién",
           "PANAMA METRO":"Panamá Metro","PANAMA OESTE":"Panamá Oeste","VERAGUAS":"Veraguas"}

@st.cache_data
def cargar():
    a = pd.read_csv("salida_ma/asignacion_sma.csv", index_col=0); a.index = a.index.map(NOMBRES)
    m = pd.read_csv("salida_ma/metricas_sma.csv", index_col=0)
    p = pd.read_csv("salida/proyeccion_anc_2021_2023.csv"); p["region"] = p["region"].map(NOMBRES)
    al = pd.read_csv("salida/alertas_anomalias.csv")
    return a, m, p, al
a, m, p, al = cargar()

st.title("Agua no contabilizada (ANC) – Tablero de decisión")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Presupuesto asignado (M B/.)", f"{a['Presupuesto (M B/.)'].sum():.0f}")
c2.metric("Cuadrillas", int(a["Cuadrillas"].sum()))
c3.metric("Agua recuperada (mil mill. gal/año)", f"{a['Agua recuperada (mil mill. gal/año)'].sum():.1f}")
c4.metric("Región prioritaria", a["IP"].idxmax())

t1, t2, t3, t4 = st.tabs(["Asignación", "Mapa de calor", "Proyección ANC", "Alertas y métricas"])
with t1:
    st.plotly_chart(px.bar(a.reset_index(), x="index", y="Presupuesto (M B/.)", color="IP",
                           labels={"index": "Región"}), use_container_width=True)
    st.dataframe(a[["Prior.","IP","Presupuesto (M B/.)","Cuadrillas","Acción recomendada"]])
with t2:
    cols = ["IP","Criticidad","ANC proy. (%)","Vol. perdido (mil mill. gal/año)","Presupuesto (M B/.)"]
    st.plotly_chart(px.imshow((a[cols] / a[cols].max()).T, color_continuous_scale="YlOrRd",
                              aspect="auto"), use_container_width=True)
with t3:
    st.plotly_chart(px.line(p, x="anio", y="anc_pct_proy", color="region", markers=True), use_container_width=True)
with t4:
    st.dataframe(al); st.dataframe(m.iloc[:, :3])