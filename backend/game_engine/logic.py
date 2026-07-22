#backend/game_engine/logic.py
import random

def resolve_action(num_dice=1, modifier=0, tags=[]):

    dice_pool = num_dice
    total_modifier = modifier

    for tag in tags:

        effect = tag.get('effect', '')

        if effect == 'bonus_die':

            dice_pool += 1

        elif effect == 'malus_die':

            dice_pool = max(1, dice_pool - 1) # Non si può scendere sotto 1 dado

        elif effect == 'bonus_2':

            total_modifier += 2

        elif effect == 'malus_2':

            total_modifier -= 2

        elif effect == 'auto_fail':

            return {
                "rolls": [],
                "total": 0,
                "success_level": "Auto-Fail",
                "tags_used": [t['name'] for t in tags],
                "message": "Il tag ha causato un fallimento automatico."
            }

    rolls = []

    for _ in range(dice_pool):

        rolls.append(random.randint(1, 6))

    raw_total = sum(rolls)
    final_total = raw_total + total_modifier
    success_level = "Fail"
    message = "L'azione fallisce."

    if final_total >= 15:

        success_level = "Critical"
        message = "Successo straordinario! Ottieni un vantaggio extra."

    elif final_total >= 10:

        success_level = "Success"
        message = "Successo pieno. Raggiungi il tuo obiettivo."

    elif final_total >= 6:

        success_level = "Partial"
        message = "Successo parziale. Ce la fai, ma con una complicazione o un costo."

    return {
        "dice_pool": dice_pool,
        "rolls": rolls,
        "raw_total": raw_total,
        "modifier_applied": total_modifier,
        "final_total": final_total,
        "success_level": success_level,
        "message": message,
        "tags_used": [t['name'] for t in tags]
    }
