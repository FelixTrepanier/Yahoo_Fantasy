
def points_earned(cat, cat_opp):
    if cat > cat_opp:
        return 2
    elif cat < cat_opp:
        return 0
    else:
        return 1

def win(cat, cat_opp):
    if cat > cat_opp:
        return 1
    else:
        return 0

def tie(cat, cat_opp):
    if cat == cat_opp:
        return 1
    else:
        return 0

def loss(cat, cat_opp):
    if cat < cat_opp:
        return 1
    else:
        return 0