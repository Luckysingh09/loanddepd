import pandas as pd
import datetime
import numpy as np
import streamlit as st
import base64
from io import BytesIO

st.header("Welcome, Now you can process your file")

st.sidebar.write("Please Select File depd0580")
uploaded_file = st.sidebar.file_uploader("Choose a depd 0580 file")
if uploaded_file is not None:
    df=pd.read_fwf(uploaded_file,header=None,colspecs=([7,21],[22,52],[53,84],[84,91],[204,212],[213,221],[222,242],[242,253],[253,264],[265,286],[286,304],[304,314],[331,344],[383,388]),skiprows=10,names=['Account_No','Product_Desc','Customer_Name','Int_Rate','IRAC-NEW','IRAC-OLD','CURRENT_BALANCE','SANC_DT','EXP_DT','SAN_LIMIT','CUSTOMER_NO','PRODUCT','MOBILE NO','ACCT-BR'] )
    df['Account_No']=df['Account_No'].str.replace("-","")
    df['CUSTOMER_NO']=df['CUSTOMER_NO'].str.replace("-","")
    df['PRODUCT']=df['PRODUCT'].str.replace("-","")
    df=df[df['Account_No'].str.len()==11]
    df['EXP_DT']=pd.to_datetime(df['EXP_DT'], format="%d/%m/%Y",errors = 'coerce')
    df['SANC_DT']=pd.to_datetime(df['SANC_DT'], format="%d/%m/%Y",errors = 'coerce')

    df['Account_No']=pd.to_numeric(df['Account_No'])
    df['CUSTOMER_NO']=pd.to_numeric(df['CUSTOMER_NO'])
    df['PRODUCT']=pd.to_numeric(df['PRODUCT'])
    df['Int_Rate']=pd.to_numeric(df['Int_Rate'])
    
    df['SAN_LIMIT']=df['SAN_LIMIT'].str.replace(",","")
    df['SAN_LIMIT']=pd.to_numeric(df['SAN_LIMIT'])
    df2=df[df['CURRENT_BALANCE'].str.contains("-")]
    df2['CURRENT_BALANCE']=df2['CURRENT_BALANCE'].str.replace("-","")
    df2['CURRENT_BALANCE']=df2['CURRENT_BALANCE'].str.replace(",","")
    df2['CURRENT_BALANCE']=pd.to_numeric(df2['CURRENT_BALANCE'])
    df1=df[~df['CURRENT_BALANCE'].str.contains("-")]
    df1['CURRENT_BALANCE']=df1['CURRENT_BALANCE'].str.replace(",","")
    df1.loc[:,'CURRENT_BALANCE']=0
    df1['CURRENT_BALANCE']=pd.to_numeric(df1['CURRENT_BALANCE'])
    df1['ACCT-BR']=pd.to_numeric(df1['ACCT-BR'])

    dffinal=df2.append(df1,ignore_index=False)
    st.sidebar.write("Please Select File loand2390")
    uploaded_loanfile = st.sidebar.file_uploader("Choose a loand2390 file")
   
    if uploaded_loanfile is not None:
        dfl=pd.read_fwf(uploaded_loanfile,header=None,colspecs=([1,21],[22,37],[38,63],[63,100],[101,119],[119,128],[152,176],[200,212],[236,238],[241,243],[243,261]),skiprows=10,names=['Account_No','CUSTOMER_NO','Product_Desc','Customer_Name','SAN_LIMIT','Int_Rate','CURRENT_BALANCE','SANC_DT','IRAC-NEW','IRAC-OLD','MOBILE NO'] )
        dfl=dfl[dfl['Account_No'].str.len()==11]
        dfl['Account_No']=pd.to_numeric(dfl['Account_No'])
        dfl['CUSTOMER_NO']=pd.to_numeric(dfl['CUSTOMER_NO'])
        dfl['Int_Rate']=pd.to_numeric(dfl['Int_Rate'])
        dfl['SAN_LIMIT']=dfl['SAN_LIMIT'].str.replace(",","")
        dfl['SAN_LIMIT']=pd.to_numeric(dfl['SAN_LIMIT'])
        dfl['CURRENT_BALANCE']=dfl['CURRENT_BALANCE'].str.replace(",","")
        dfl['CURRENT_BALANCE']=pd.to_numeric(dfl['CURRENT_BALANCE'])
        dfl['SANC_DT']=pd.to_datetime(dfl['SANC_DT'], format="%d-%m-%Y",errors = 'coerce')
        dfl1=pd.read_excel("https://rmgbank-my.sharepoint.com/:x:/g/personal/loans_rmgb_in/EcErNXjr4VlAr2zqoCgYD0oBMVq9CD6f4cfSMo2piEVpAA?e=F3vRKb")
        dflfinal=pd.merge(dfl,dfl1,how="right",left_on='Product_Desc',right_on='Product_Desc')
        dfcom=pd.concat([dffinal,dflfinal])

        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            dfcom.to_excel(writer, sheet_name='Sheet1',index=False)
            writer.save()
            processed_data = output.getvalue()
            return processed_data


        def get_table_download_link(df):
            """Generates a link allowing the data in a given panda dataframe to be downloaded
            in:  dataframe
            out: href string
            """
            val = to_excel(df)
            b64 = base64.b64encode(val)  # val looks like b'...'
            return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download File here</a>' # decode b'abc' => abc

        
        st.write("Download Consolidated File Here:")
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)

