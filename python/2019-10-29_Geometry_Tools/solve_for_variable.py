def main(eq, var):
    if var not in eq:
        raise ValueError(var + " not in equation")
    opposites = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*"
    }
    specials = {
        "^": "sqrt"
    }
    half1, half2 = eq.split("=")
    if var not in half1:
        half1, half2 = half2, half1
    

    


    print(half1)
    half1 = var
    return half1 + "=" + half2