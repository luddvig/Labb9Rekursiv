from LinkedQFile import LinkedQ


class Syntaxfel(Exception):
    pass


def checkMoleculeSyntax(molecule):
    """Kontrollerar om angiven molekyl följer syntax"""
    q = storeMolecule(molecule)
    try:
        readformel(q)                               # Startar kontroll
        return "Formeln är syntaktiskt korrekt"
    except Syntaxfel as error:                      # Fångar fel i syntax
        return str(error) + str(q)                  # Skriver ut  fel


def storeMolecule(molecule):
    """Hjälpfuntion för att lägga in molekylnamn i kö"""
    q = LinkedQ()
    for var in molecule:
        q.enqueue(var)
    return q


def readformel(q):
    """Startar första syntaxkontroll"""
    readmol(q, False)                       # False = ingen tidigare startparentes


def readmol(q, startpar):
    """Kollar molekyl. Startpar=True om startparentes tidigare påträffats i grupp, annas False."""
    readgroup(q)
    if not q.isEmpty() and q.peek() == ")" and startpar:    # Om slutpar påträffas sedan tidigare påträffad startpar
        return
    if not q.isEmpty():
        readmol(q, startpar)


def readgroup(q):
    """Kollar grupp i molekyl. Grupp måste starta med stor bokstav eller öppen parentes."""
    if not q.isEmpty() and q.peek().isalpha():              # Stor och eventuellt liten bokstav, dvs atom
        readatom(q)
        if not q.isEmpty() and q.peek().isnumeric():        # Läser eventuell siffra efter atom
            readNum(q)

    elif not q.isEmpty() and q.peek() == "(":               # Startparentes, påträffad molekyl
        q.dequeue()
        readmol(q, True)                                    # Kallar på readmol för att läsa påträffad molekyls innehåll
        if q.isEmpty():
            raise Syntaxfel("Saknad högerparentes vid radslutet ")  # Fall då slutparentes saknas
        if not q.isEmpty() and q.peek() == ")":
            q.dequeue()
            if not q.isEmpty() and q.peek().isnumeric():
                readNum(q)
            else:
                raise Syntaxfel("Saknad siffra vid radslutet ")     # Fall då siffra efter slutparentes saknas

    else:
        raise Syntaxfel("Felaktig gruppstart vid radslutet ")       # Om ej atom eller startpar


def readatom(q):
    """Läser atom. Består av Stor och eventuell liten bokstav."""
    atoms = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
                 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
                 'Rb',
                 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
                 'Cs',
                 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf',
                 'Ta',
                 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
                 'Pa',
                 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs',
                 'Mt',
                 'Ds', 'Rg', 'Cn', 'Fl', 'Lv']
    cap = readCap(q)                                # Läser stor bokstav
    atom = cap
    if not q.isEmpty() and q.peek().islower():
        small = readSmall(q)                        # Läser liten bokstav
        atom = cap + small
    if atom not in atoms:
        raise Syntaxfel("Okänd atom vid radslutet ")    # Kollar om korrekt atom


def readCap(q):
    """Läser bokstav, dequeue om stor, annars raise Syntaxfel."""
    if not q.isEmpty() and q.peek().isupper():
        return q.dequeue()
    if q.isEmpty() or not q.peek().isupper():
        raise Syntaxfel("Saknad stor bokstav vid radslutet ")


def readSmall(q):
    """Läser bokstav, dequeue om liten."""
    if not q.isEmpty() and q.peek().islower():
        return q.dequeue()


def readNum(q):
    """Läser nummer, måste vara större än 1, ex H2."""
    if not q.isEmpty() and q.peek() == "0":                     # Om nummer=0
        q.dequeue()
        raise Syntaxfel("För litet tal vid radslutet ")
    if not q.isEmpty() and q.peek() == "1":                     # Om nummer=1
        q.dequeue()
        if q.isEmpty() or not q.isEmpty() and not q.peek().isnumeric():
            raise Syntaxfel("För litet tal vid radslutet ")
    while not q.isEmpty() and q.peek().isnumeric():             # Dequeuear alla siffror i nummer
        q.dequeue()


def main():
    while True:
        uinput = input()
        if uinput == "#":
            break
        print(checkMoleculeSyntax(uinput))


if __name__ == "__main__":
    main()

