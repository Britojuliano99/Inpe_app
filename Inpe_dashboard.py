import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache
def read_table():
    df=pd.read_excel("2022_data.xlsx",index_col="Date_Time",parse_dates=["Date_Time"])
    df.sort_index(inplace=True)
    return df
@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def hist(df,Variavel):
    fig, ax = plt.subplots()
    ax.hist(df[Variavel], bins=20,color="Blue")
    ax.set_title(f"Histograma de {Variavel}")

    return fig
st.title("INPE LAVAT/CONEM Davis and Solarmetric Station")

df=read_table()

st.write("Aqui vocẽ encontra os dados do Lavat para visualização ou para download dos dados brutos")
colunasnumericas=df.columns[df.dtypes=="float"]


if st.select_slider("Qual periodo você quer ver os dados",options=(df.index),value=(df.index[0],df.index[-1]),key="Timeslider"):
    slider=st.session_state.Timeslider
    sliderdf=df.loc[slider[0]:slider[1]]
    radio=st.radio("Você gostaria de baixar ou vizualizar",options=("Baixar","Visualizar"))
    if radio=="Baixar":
        Variaveis=st.multiselect("Quais variaveis você gostaria de baixar",options=df.columns)
        csv=convert_df(sliderdf[Variaveis])
        st.download_button("Baixar os dados brutos",data=csv,file_name="Natal_weatherdata.csv",mime="text/csv")
    
    
    
    
    
    if radio=="Visualizar":
        Tipos=st.radio("Você gostaria de ver histogramas ou series temporais",options=("Serie Temporais","Histogramas"))
        if Tipos=="Serie Temporais":
            Variaveis_visualizar=st.multiselect("Quais variaveis você gostaria de Visualizar",options=colunasnumericas)  
            st.line_chart(sliderdf[Variaveis_visualizar])
        
        if Tipos =="Histogramas":
            Variavel=st.selectbox("Qual variavel você gostaria de Visualizar",options=df.columns)
            try:
                fig=hist(sliderdf,Variavel)
                st.pyplot(fig)
            except:
                st.write(" ")
