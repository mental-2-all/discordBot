emos = [{"emo":"sad"},{"emo":"angry"},{"emo":"sad"},{"emo":"sad"},{"emo":"sad"},{"emo":"sad"}]

table = {}
for emo in emos:
    if emo not in table:
        table[emo["emo"]] = 0
    table[emo["emo"]] += 1
    


{
    "sad": 5,
    "angry":4
    
}