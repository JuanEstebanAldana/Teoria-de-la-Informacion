
def No_Singular(palabras):
    no_singular=True
    for i in range(len(palabras)):
        for j in range(len(palabras)):
            no_singular = palabras[i]!=palabras[j] or i==j
            if not no_singular:
                return no_singular
    return no_singular

def Instantaneo(palabras):
    for palabra in palabras:
        for palabrita in palabras:
            if palabra != palabrita and palabrita.startswith(palabra):
                return False
    return True

#SARDINAS PATTERSON
def Univocamente_Decodificable(palabras):
    # If two different source symbols have the same codeword
    if len(palabras) != len(set(palabras)):
        return False
    codigo = set(palabras)
    # Generate S1
    conjunto_i = set()
    for x in codigo:
        for y in codigo:
            if x != y and x.startswith(y):
                sufijo = x.removeprefix(y)
                if sufijo != "":
                    conjunto_i.add(sufijo)
    conjuntos_vistos = set()
    while True:
        # If Si is empty, no ambiguity can appear
        if len(conjunto_i) == 0:
            return True
        # If Si contains a codeword, the code is not uniquely decodable
        if any(x in codigo for x in conjunto_i):
            return False
        # If this set has already appeared, the process will repeat forever
        clave = frozenset(conjunto_i)
        if clave in conjuntos_vistos:
            return True
        conjuntos_vistos.add(clave)
        # Generate Si+1
        conjunto_ii = set()
        for x in codigo:
            for y in conjunto_i:
                # y is prefix of x
                if x.startswith(y):
                    sufijo = x.removeprefix(y)
                    if sufijo == "":
                        return False
                    conjunto_ii.add(sufijo)
                # x is prefix of y
                if y.startswith(x):
                    sufijo = y.removeprefix(x)
                    if sufijo == "":
                        return False
                    conjunto_ii.add(sufijo)
        conjunto_i = conjunto_ii


####################################################################################################################################################
####################################################################################################################################################


#codificacion=["011","000","010","101","001","100"]
codificacion=[".,",";",",,",":","...",",:;"]
print("La codificacion:",codificacion,"es: ")
if(No_Singular(codificacion)):
    if(Univocamente_Decodificable(codificacion)):
        if(Instantaneo(codificacion)):
            print("INSTANTANEO")
        else:
            print("UNIVOCAMENTE DECODIFICABLE")
    else:
        print("NO SINGULAR")
else:
    print("BLOQUE")



####################################################################################################################################################
####################################################################################################################################################


"""
###############################       DEFINICIONES      ############################################################################################


CALIFICACION DE CODIGOS
    secuencias fijas? Si:BLOQUE No:NO BLOQUE
    BLOQUE  palabras distintas para cada simbolo?   Si:NO SINGULAR  No:SINGULAR(BLOQUE)
        NO SINGULAR se puede decodificar sin ambiguedad?    Si:UNIVOCAMENTE DECODIFICABLE   No:NO UNIVOCO(NO SINGULAR)
            UNIVOCAMENTE DECODIFICABLE  se puede decodificar sin ver todo el mensaje?   Si:INSTANTANEO  No:NO INSTANTANEO(UNIVOCAMENTE DECODIFICABLE)



"""
