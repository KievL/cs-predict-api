from bs4 import BeautifulSoup

def scrap(html:str):
    try:
        match_html=BeautifulSoup(html, 'html.parser')
        current_match={}

        for j,teamsName in enumerate(match_html.find_all(class_='team')):
            if j>1:
                break
            current_match['team_'+str(j+1)] = teamsName.find(class_='teamName').string
            current_match['team'+str(j+1)+'_src'] = teamsName.find(class_='logo')['src']
        
        #Get the series (bo3, bo5, bo1...)
        series = 'bo'+str(len(match_html.find_all(class_='mapholder')))
        current_match['series'] = series

        rankings = match_html.find_all(class_='teamRanking')
        try:
            ranking_team1 = rankings[0].a.text #World ranking #XX
            ranking_team1 = ranking_team1[ranking_team1.find("#")+1:]
        except:
            ranking_team1="Unranked"

        try:
            ranking_team2 = rankings[1].a.text #World ranking #XX
            ranking_team2 = ranking_team2[ranking_team2.find("#")+1:]
        except:
            ranking_team2="Unranked"

        current_match['team1_ranking']=ranking_team1
        current_match['team2_ranking']=ranking_team2

        #Get winstreak and maps won
        past_matches = match_html.find_all(class_="past-matches-box")
        past_matches_t1 = past_matches[0]
        past_matches_t2 = past_matches[1]

        try:
            #Format: 'XX match win streak'
            winstreak_t1 = int(past_matches_t1.find(class_="past-matches-streak").text.split(" ")[0])
        except:
            winstreak_t1 = 0
        
        try:
            #Format: 'XX match win streak'
            winstreak_t2 = int(past_matches_t2.find(class_="past-matches-streak").text.split(" ")[0])
        except:
            winstreak_t2 = 0
        
        current_match['winstreak_t1'] = winstreak_t1
        current_match['winstreak_t2'] = winstreak_t2

        past_maps_won_t1 = 0
        past_maps_won_t2 = 0
        past_maps_lost_t1 = 0
        past_maps_lost_t2 = 0            

        def count_maps_won_and_lost(pst_matches: str, won=0, lost=0):
            past_matches_score = pst_matches.find_all(class_='past-matches-score')

            for scr in past_matches_score:

                score = scr.text.split('-')
                #From string to int
                score = list(map(lambda x : int(x), score))

                ##Left score or score[0] is t1's score
                ##Test if it is a series score or a map score
                
                if score[0]+score[1]<=5:
                    won= won + score[0]
                    lost= lost + score[1]
                else:
                    if score[0] > score[1]:
                        won= won + 1
                    else:                    
                        lost= lost+1

            return won, lost
        
        past_maps_won_t1, past_maps_lost_t1 = count_maps_won_and_lost(past_matches_t1)
        past_maps_won_t2, past_maps_lost_t2 = count_maps_won_and_lost(past_matches_t2)

        current_match['past_maps_won_t1'] = past_maps_won_t1
        current_match['past_maps_lost_t1'] = past_maps_lost_t1
        current_match['past_maps_won_t2'] = past_maps_won_t2
        current_match['past_maps_lost_t2'] = past_maps_lost_t2

        #HtH wins and overtimes
        hth = match_html.find(class_="head-to-head")
        hth_info = hth.find_all(class_="bold")
        
        ## Wins T1 - Overtimes - Wins T2
        current_match['hth_wins_t1'] = int(hth_info[0].text)
        current_match['hth_wins_t2'] = int(hth_info[2].text)
        current_match['hth_overtimes'] = int(hth_info[1].text)

        return current_match
    except:
        raise Exception("Unable to scrap")

    