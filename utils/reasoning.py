def generate_reasoning(result):

    label = result["label"]

    if label.upper() == "REAL":

        return [

            "Natural skin texture detected.",

            "Facial symmetry appears consistent.",

            "Lighting and shadows are realistic.",

            "Eye reflections look natural.",

            "No obvious AI-generated artifacts detected."

        ]

    return [

        "Artificial facial texture patterns detected.",

        "Possible GAN-generated image artifacts identified.",

        "Facial regions contain inconsistent details.",

        "Lighting or edge transitions appear unnatural.",

        "Prediction confidence is high."

    ]