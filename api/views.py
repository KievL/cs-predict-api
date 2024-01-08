from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scraper import scrap
from xgboost import XGBClassifier
import pickle
from .data_eng import engData
from pathlib import Path
import joblib
import pandas as pd



# Create your views here.
def post(request, *args, **kwargs):
    print(request)
    response = JsonResponse({'key': 'value'})
    return response

@api_view(['POST','GET'])
def api_model(request, *args, **kwargs):
    try:
        html_scraped = scrap(request.data['html'])
    except:
        return JsonResponse({'error':'Invalid HTML'}, status=400)

    model = joblib.load('api\model.joblib')

    try:
        model_data, match_info = engData(html_scraped)
    except:
        return JsonResponse({'error':'Invalid Match'}, status=400)
    
    try:
        data_ready = pd.DataFrame(model_data.astype(int))
        pred = model.predict(data_ready)[0]
        match_info = match_info.iloc[0]
    except:
        return JsonResponse({'error':"Couldnt make a prediction"}, status=400)
    
    return JsonResponse({'winner':int(pred),'team1':match_info['team_1'],'team2':match_info['team_2'],'team1_logo':match_info['team1_src'], 'team2_logo':match_info['team2_src']})
