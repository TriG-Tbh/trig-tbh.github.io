def main(eq):
    half1, half2 = eq.split("=")
    inhalf1 = ("x" in half1 and "y" in half1)
    inhalf2 = ("x" in half2 and "y" in half2)
    # Slope Intercept
    if not inhalf1 and not inhalf2:
        if "y" not in half1:
            half1, half2 = half2, half1
        if len(half1) != 1:
            import solve_for_variable as sfv
            neq = half1 + "=" + half2
            neq = sfv.main(neq, "y")
            print(neq)



while True:
    eq = input("> ")
    eq = eq.strip().replace(" ", "")
    main(eq)