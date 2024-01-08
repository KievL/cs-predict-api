import pandas as pd
import numpy as np

def engData(data):
    try:
        data_full = {
           'm1': data,
           'm2': data
        }
        df = pd.DataFrame(data_full).T
        df["series"] = df["series"].apply(bestsof)

        df_info = df[['team_1','team_2','team1_src','team2_src']]

        df.drop(["team_1", "team_2",'team1_src','team2_src'], axis=1, inplace=True)

        df["team1_ranking"] = np.where(df["team1_ranking"]=="Unranked", 300,df["team1_ranking"])
        df["team2_ranking"] = np.where(df["team2_ranking"]=="Unranked", 300,df["team2_ranking"])

        df.drop(df[df['winstreak_t1'].isna()].index, inplace=True)
        df = df.reset_index(drop=True)
        X = df.iloc[:,:]
        return X, df_info

    except Exception as e:
        return e
    
def bestsof(x):
  if x == "bo3":
    return 3
  elif x == "bo5":
    return 5
  else:
    return 1


    