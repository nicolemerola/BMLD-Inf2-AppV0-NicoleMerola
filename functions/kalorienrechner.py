def BMR_rechner( gewicht, groesse, alter, geschlecht):
    if geschlecht == "Mann":
        bmr = 10 * gewicht + 6.25 * groesse - 5 * alter + 5
    elif geschlecht == "Frau":
        bmr = 10 * gewicht + 6.25 * groesse - 5 * alter - 161
    else:
        raise ValueError("Ungültiges Geschlecht. Bitte 'Mann' oder 'Frau' eingeben.")
    return bmr