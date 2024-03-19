
import pandas as pd
import numpy as np
import time
import re


def infer_and_convert_data_types(df):
    # drop empty roll and col
    df = df.dropna(axis=1, how='all')
    df = df[df.iloc[:, 1:].notnull().any(axis=1)]
    
    for col in df.columns:
        
        #remove symbol and temp postfix
        df[col]=df[col].astype(str)
        df[col] = df[col].str.replace(r'[^a-zA-Z0-9.\-/\+]|C$|F$|K$', '', regex=True)
        
        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        # If not all values are N/A, with some outliers
        if (not df_converted.isna().all()) & (len(df_converted[df_converted.isna()]) / len(df_converted)<0.5):        
            df_no_na=df_converted.dropna()

            # if all digits are int
            if df_no_na.astype(int).eq(df_no_na).all():
                # if int is timestamp (unix:s)
                if len(df_no_na[df_no_na.apply(lambda x: int(x)>=int(time.mktime(time.strptime('2005-01-01', '%Y-%m-%d'))) and int(x)<=int(time.mktime(time.strptime('2035-01-01', '%Y-%m-%d'))))])/len(df_no_na)>0.5:   
                    try:
                        df[col] = pd.to_datetime(df_converted,unit='s',errors='coerce')
                        continue
                    except (ValueError, TypeError):
                        pass
                
                # if int is timestamp (unix:ms)
                elif len(df_no_na[df_no_na.apply(lambda x: int(x)>=int(time.mktime(time.strptime('2005-01-01', '%Y-%m-%d'))* 1000) and int(x)<=int(time.mktime(time.strptime('2035-01-01', '%Y-%m-%d'))* 1000))])/len(df_no_na)>0.5:
                    
                    try:
                        df[col] = pd.to_datetime(df_converted,unit='ms',errors='coerce')
                        continue
                    except (ValueError, TypeError):
                        pass
                
                # if int is time (YYYYMMDD)
                elif len(df_no_na[df_no_na.apply(lambda x: x>=20050101 and x<=20350101)])/len(df_no_na)>0.5:
                    try:
                        df[col] = pd.to_datetime(df_converted,format='%Y%m%d',errors='coerce')
                        continue
                    except (ValueError, TypeError):
                        pass

                # if int is bool
                elif len(df_no_na[df_no_na.apply(lambda x: x==1 or x==0)])/len(df[col])>0.5:
                    df[col]=df_converted.apply(lambda x: True if x == 1 else (False if x==0 else None))
                    df[col]=df[col].astype('boolean')  # boolean can only accept True/false
                    continue

                #  if all ele are int, covert into int (NaN cannot be converted into int)
                if not df_converted.isna().any():
                    if df_converted.max()<np.iinfo(np.int8).max:  
                        df[col]=df_converted.astype('int8')
                        continue
                    elif df_converted.max()<np.iinfo(np.int16).max:  
                        df[col]=df_converted.astype('int16')
                        continue
                    elif df_converted.max()<np.iinfo(np.int32).max:  
                        df[col]=df_converted.astype('int32')
                        continue
                    else: 
                        df[col]=df_converted.astype('int64')
                        continue

            # if any float/NaN, covert into float
            if df_converted.max()<np.finfo(np.float32).max:
                # check if there is any precision loss when convert into float32
                if df_no_na.astype('float32').eq(df_no_na).all():
                    df[col]=df_converted.astype('float32')
                else:
                    df[col]=df_converted
            else:
                df[col]=df_converted
            continue
        
        # Attempt to convert to complex
        df_no_na=df[col].dropna()
        if len(df_no_na[df_no_na.str.match('\(?[-+]?[0-9]*\.?[0-9]+[+-][0-9]*\.?[0-9]*j\)?')]) / len(df_no_na) > 0.5:
            try:
                df[col]=df[col].apply(lambda x:complex(x))
                continue
            except (ValueError, TypeError):
                pass

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass
        

        # Check if the column should be categorical --> save memmory
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization

            # if catetories are true/false, convert into bool
            df_low_case=df[col].astype(str).str.lower()
            if len(df_low_case[df_low_case.apply(lambda x: x=='true' or x=='false')])/len(df[col])>0.5:
                # print(df_low_case)
                df[col]=df_low_case.apply(lambda x: True if x.lower() == 'true' else (False if x=='false' else None))
                df[col]=df[col].astype('boolean')  # boolean can only accept True/false
                continue

            # if not bool, identify as common category
            df[col] = pd.Categorical(df[col])


            

    return df

# Test the function with your DataFrame
# df = pd.read_csv('sample_data.csv', encoding = 'unicode_escape')
# print("Data types before inference:")
# print(df.dtypes)

# def str_to_complex(s):
#     real, imag = map(float, s.replace('j', '').split('+'))
#     return complex(real, imag)
# def custom_converter(value):
#     try:
#         # 尝试将值转换为整数
#         return int(value)
#     except ValueError:
#         try:
#             # 尝试将值转换为浮点数
#             return float(value)
#         except ValueError:
#             # 尝试将值转换为日期时间类型
#             return pd.to_datetime(value, errors='coerce')
        
# print("----- DataFrame after inferring data types:")
# mix_test_list=df["Score"].apply(lambda x: pd.api.types.is_numeric_dtype(x))
# print("--- max timestamp:")
# print(int(time.mktime(time.strptime('2005-01-01', '%Y-%m-%d'))))
# print("--- min timestamp:")
# print(int(time.mktime(time.strptime('2035-01-01', '%Y-%m-%d'))))
# print(" --------- time stamp --------- ")
# print(time.time(),time.mktime(time.strptime("2023-06-05", "%Y-%m-%d")))

# df = infer_and_convert_data_types(df)

# print("\nData types after inference:")
# print(df.dtypes)
# print(df)