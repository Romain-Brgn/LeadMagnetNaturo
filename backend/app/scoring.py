from typing import List

TEMPERAMENTS = ["sanguin", "bilieux", "lymphatique", "nerveux"]


def compute_temperaments(selectedInForm: List[str]):
    result = {
        "answers": selectedInForm,
        "scores": {"sanguin": 0, "bilieux": 0, "lymphatique": 0, "nerveux": 0},
        "percentages": {"sanguin": 0, "bilieux": 0, "lymphatique": 0, "nerveux": 0},
        "top1": [],
        "top2": [],
        "isValid": True,
        "error_code": None,
        "error_message": None 
        }

    for s in selectedInForm:
        s = s.strip()
        if s in TEMPERAMENTS:
            result["scores"][s] += 1
    basePourcent = sum(result["scores"].values())
    if basePourcent == 0:
        result["isValid"] = False
        result["error_message"] = "Pas de réponses cochées ? Pas de profil."
        result["error_code"] = "NO_ANSWERS"
        return result
    
    for key in result["scores"]:
        result["percentages"][key] = round(result["scores"][key]*100/basePourcent,2)

    max_score = (max(result["scores"].values()))
    for key, value in result["scores"].items():
        if value == max_score and value > 0:
           result["top1"].append(key)
    if len(result["top1"]) > 1:
        return result
    if len(result["top1"]) == 1: 
        for key, value in result["scores"].items():
            if value < max_score and value > 0:
                result["top2"].append(value)
    if len(result["top2"]) > 0:
            max_score2 = max(result["top2"])
            result["top2"] = list()

            for key, value in result["scores"].items():
                if value == max_score2:
                    result["top2"].append(key)
    else:
        result["top2"] = []

    return result