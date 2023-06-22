def lane(x, y):
        region = ""
        blueBaseDistance = ((y - 300) ** 2 + (x - 300) ** 2) ** 0.5
        redBaseDistance = ((y - 14450) ** 2 + (x - 14450) ** 2) ** 0.5
        topLaneDistance = ((y - 14000) ** 2 + (x - 500) ** 2) ** 0.5
        botLaneDistance = ((y - 500) ** 2 + (x - 14000) ** 2) ** 0.5
        baronDistance = ((y - 10396) ** 2 + (x - 5055) ** 2) ** 0.5
        dragDistance = ((y - 4524) ** 2 + (x - 9850) ** 2) ** 0.5
        topBrushDistance = ((y - 8159) ** 2 + (x - 5180) ** 2) ** 0.5

        if blueBaseDistance <= 5250:
            region = "Blue Base"
        elif redBaseDistance <= 5100:
            region = "Red Base"
        elif y >= 13000:
            region = 'Top Lane'
        elif x <= 2000:
            region = "Top Lane"
        elif topLaneDistance <= 3000:
            region = "Top Lane"
        elif y <= 2000:
            region = "Bot Lane"
        elif x >= 13000:
            region = "Bot Lane"
        elif botLaneDistance <= 3000:
            region = "Bot Lane"
        elif ((x * .937 - 400) <= y) and (y <= (x * .937 + 1430)):
            region = "Mid Lane"
        elif (x * .937 - 400) <= y:
            region = "Top Jungle"
        elif y <= (x * .937 + 1430):
            region = "Bot Jungle"
        else:
            region = "*"

        if (region == "Top Jungle" or region == "Bot Jungle") and (
            (y < (x * -.83 + 15000)) and (y > (x * -.85 + 12600))):
            if y <= (x * .937 + 1430):
                region = "Bot River"
            else:
                region = "Top River"
        if region == "Top Jungle" or region == "Bot Jungle":
            if y >= (x * -.85 + 13500):
                region = "Red " + region
            else:
                region = "Blue " + region

        if baronDistance < 850:
            region = "Top River"
        if dragDistance < 700:
            region = "Bot River"
        if topBrushDistance < 415:
            region = "Top River"
        return region