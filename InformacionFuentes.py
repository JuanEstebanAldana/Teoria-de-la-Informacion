from math import *
import random

def cantidad_informacion_lista_memoria_nula(fuente):
    cant_info=[]
    for i in range(len(fuente)):
        cant_info.append(log2(1/fuente[i]))
    return cant_info

def entropia_fuente(fuente):#recibe directamente las probabilidades de la fuente
    entropia=0
    cant_info=cantidad_informacion_lista_memoria_nula(fuente)
    for i in range(len(fuente)):
        entropia+=cant_info[i]*fuente[i]
    return entropia

def fuente_desde_mensaje(mensaje):
    probabilidades=[]
    alfabeto=[]
    cont=[]
    for letra in mensaje:
        if letra not in alfabeto:
            cont.append(1)
            alfabeto.append(letra)
        else:
            cont[alfabeto.index(letra)]+=1
    for i in range(len(cont)):
        probabilidades.append(cont[i]/len(mensaje))
    return alfabeto, probabilidades

def entropia_fuente_binaria(w):
    print("La entropia de una fuente binaria de w=",w, "H=",entropia_fuente([w,1-w]))

def Genera_Extension_Orden_N (alfabeto, distribucion, N):
    extension=[]
    probabilidades=[]
    extension=alfabeto.copy()
    probabilidades=distribucion.copy()
    for i in range(N-1):
        for j in range(len(extension)*(len(alfabeto)-1)):
            extension.append(extension[j])
            probabilidades.append(probabilidades[j])
        k=0
        for j in range(len(alfabeto)):
            for k in range(k,k+len(alfabeto)**(i+1)):
                extension[k]=alfabeto[j]+extension[k]
                probabilidades[k]*=distribucion[j]
            k+=1
    return extension, probabilidades

def Estado_Estacionario_Markov(matriz,tolerancia=0.000000000000000000000000001):#RECORDAR, COLUMNAS DAN 1 POR ENDE CADA SUB LISTA NO TIENE POR QUE DAR 1
    vector_estacionario=[]
    vector_auxiliar=[]
    vector_previo=[]
    for dimension in matriz:
        vector_estacionario.append(1/len(matriz))
        vector_auxiliar.append(0)
        vector_previo=vector_auxiliar.copy()
    while any(abs(a - b)>= tolerancia for a,b in zip(vector_estacionario,vector_previo)):
        for k in range(len(vector_auxiliar)):
            vector_auxiliar[k]=0
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                vector_auxiliar[i]+=vector_estacionario[j]*matriz[i][j]
        vector_previo=vector_estacionario.copy()
        vector_estacionario=vector_auxiliar.copy()
    return vector_estacionario

def Entropia_Markov_Usando_Vec_Estacionario(matriz):
    vector_estacionario=Estado_Estacionario_Markov(matriz)
    entropia=0
    for i in range(len(vector_estacionario)):
        aux=0
        for j in range(len(vector_estacionario)):
            if matriz[j][i] != 0:
                aux+=log2(1/matriz[j][i])*matriz[j][i]
        entropia+=aux*vector_estacionario[i]
    return entropia
    
def Alfabeto_De_Cadena(string):#GENERA ERROR CUANDO EL ULTIMO SIMBOLO TIENE ESA UNICA APARICION, LA ULTIMA DEL MENSAJE
    matriz=[]
    alfabeto=[]
    cont=[]
    anterior=0
    for letra in string:
        if letra not in alfabeto:
            alfabeto.append(letra)
            for fila in matriz:
                fila.append(0)
            matriz.append([0])
            for j in range(len(matriz)-1):
                matriz[len(matriz)-1].append(0)
            cont.append(0)
        if anterior != 0:
            j=0
            while j<=len(alfabeto) and alfabeto[j] != anterior:
                j+=1
            i=0
            while i<=len(alfabeto) and alfabeto[i] != letra:
                i+=1
            matriz[i][j]+=1
            cont[j]+=1
        anterior=letra
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            matriz[i][j]/=cont[j]
    return matriz, alfabeto

def Emision_Mensaje_Markov(matriz,alfabeto,N):
    letra=random.random()*len(alfabeto)
    letra=int(letra//1)
    mensaje=''
    for i in range(N):
        sig=random.random()
        aux=0
        j=0
        while j<len(alfabeto) and aux<sig:
            aux+=matriz[j][letra]
            j+=1
        mensaje+=alfabeto[j-1]
        letra=j-1
    return mensaje

def Fuente_Tiene_Memoria(matriz, tolerancia=0.000000000000000000000000001):

    for i in range(len(matriz)):
        diferencia = max(matriz[i]) - min(matriz[i])

        if diferencia > tolerancia:
            return True

    return False



####################################################################################################################################################
####################################################################################################################################################


#fuente=[0.25,0.25,0.25,0.25]
#print("Cantidad de informacion de la fuente:", cantidad_informacion_lista_memoria_nula(fuente))
#print("La entropia de la fuente es", entropia_fuente(fuente))


#FUENTE DESDE MENSAJE
"""
alfabeto=[]
probabilidades=[]
alfabeto, probabilidades = fuente_desde_mensaje("ABDAACAABACADAABDAADABDAAABDCDCDCDC")
for i in range(len(alfabeto)):
    print(alfabeto[i]+" ",probabilidades[i])
print("La entropia de la fuente es",entropia_fuente(probabilidades))
"""



#entropia_fuente_binaria(1)


#GENERADOR DE EXTENSIONES DESDE ALFABETO Y DISTRIBUCION

alfabeto=['X','Y','Z']
distribucion=[0.5,0.1,0.4]
extension=[]
probabilidades=[]
extension, probabilidades=Genera_Extension_Orden_N(alfabeto,distribucion,3)
print ("EXT     PROB")
for k in range(len(extension)):
    print(extension[k],"   ",probabilidades[k])
print("La entropia de la extension es",entropia_fuente(probabilidades))
#print("La entropia de la fuente es", entropia_fuente(distribucion))





#ALFABETO DE CADENA, FUENTE CON O SIN MEMORIA, ENTROPIA
'''
alfabeto=[]
matriz=[[1/2,0,0,1/2],[1/2,0,0,0],[0,1/2,0,0],[0,1/2,1,1/2]]
matriz, alfabeto =Alfabeto_De_Cadena(")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])")
print("El alfabeto correspondiente a la cadena y sus probabilidades son:",alfabeto,matriz)
#matriz=[[1/3,0,1,1/2,0],[1/3,0,0,0,0],[0,1,0,0,0],[1/3,0,0,0,1/2],[0,0,0,1/2,1/2]]
if(Fuente_Tiene_Memoria(matriz)):
    print("La fuente tiene memoria.")
    print("El vector estacionario de la fuente de Markov es:",Estado_Estacionario_Markov(matriz))
    print("La entropia de la fuente de Markov es:",Entropia_Markov_Usando_Vec_Estacionario(matriz),"bits")
else:
    print("La fuente no tiene memoria.")
    promedio=[]
    for i in range(len(matriz)):
        promedio.append(0)
        for elemento in matriz[i]:
            promedio[i]+=elemento
        promedio[i]/=len(matriz)
    print("La entropia de la fuente de es:",entropia_fuente(promedio),"bits")
'''



#print("La entropia de la fuente de Markov es:",Entropia_Markov_Usando_Vec_Estacionario([[0.5,1/3,0],[0.5,1/3,1],[0,1/3,0]]))
#print("El vector estacionario de la fuente de Markov es:",Estado_Estacionario_Markov([[0.5,1/3,0],[0.5,1/3,1],[0,1/3,0]]))
#print("Mensaje aleatorio de la fuente de Markov",Emision_Mensaje_Markov([[0.1,0.2,0.2],[0.2,0.3,0.5],[0.7,0.5,0.3]],['a','b','c'],30))


####################################################################################################################################################
####################################################################################################################################################

"""
###############################       DEFINICIONES      ###############################
FUENTE DE MARKOV: UNA FUENTE DE MARKOV ES UNA FUENTE CON PROBABILIDADES CONDICIONADAS, ERGODICA, CON ERGODICA=IRREDUCTIBLE(TRANSITIVA)+APERIODICA
APERIODICA: UNA FUENTE APERIODICA ES UNA FUENTE QUE NO ESTA FORZADA A SEGUIR UN UNICO CICLO, ES DECIR, VARIA LA SECUENCIA DE SIMBOLOS QUE GENERA

6.
Para una fuente de memoria con un unico simbolo, la entropia sera siempre cero. Esto se debe a que cuando hay un unico simbolo
se sabe que es lo que va a pasar, va a aparecer ese simbolo. Esto se denomina un suceso cierto, por lo que no aporta por definicion
nada de informacion. Por ende, la entropia, que es la cantidad media de informacion de la fuente, es necesariamente 0.
7.
La maxima entropia para una fuente de memoria nula de cuatro simbolos es de 2 bits, esto se da cuando los simbolos son equiprobables.
Esto es logico ya que se trata de el caso mas lejano posible a la existencia de un suceso cierto.
9.
w= 0.25 H= 0.8112781244591327
w= 0.75 H= 0.8112781244591327
Para estos dos es evidente lo que sucede, w=0,25 y w=0,75 son escencialmente lo mismo, ya que la probabilidad del otro simbolo
es 1-w, por lo que las probabilidades son exactamente iguales.
w= 0.5 H= 1.0
Este es el caso de mayor entropia, dos simbolos equiprobables, esta es la situacion mas lejana posible a un suceso cierto.
w= 1 H=0.0
w= 0 H=0.0
Estos dos son lo contrario de lo que sucedio en los casos anteriores, son en ambos casos un suceso cierto y un suceso imposible,
por lo que no existe informacion en el suceso, ya que es 100% predecible.
"""
