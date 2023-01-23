# YOLO Project - Data Analysis

## Quin és el propòsit d'aquest repositori?

Ens han encarregat analitzar imatges de carrers de diferents ciutats europees, per un projecte relacionat amb smart-cities. Per tal de començar el projecte, tenim un datatset d'imatges de tres ciutats on les imatges han estat filmades des d'un cotxe des de diferents punts de la ciutat. El data set complet el podeu trobar aquí
(https://www.cityscapes-dataset.com). Junt amb les imatges ens han donat també uns fitxers de text on podem trobar els tipus d'objecte que hi ha i les posicions per cada un d'ells, de tal manera que tenim un fitxer de text per a cada imatge. Ens indiquen que aquesta informació s'ha extret utilitzant YOLOv5 (https://docs.ultralytics.com), (YOLO, You Only Look Once) que és un algoritme basat en xarxes convolucionals molt potent per a la detecció d'objectes en temps real.

En aquesta PAC haureu de treballar amb aquests fitxers per tal d'analitzar les imatges i extreure'n conclusions sense haver de mirar cadascuna de les imatges. La carpeta dataset s'estrctura de la manera següent:
- images: Carpeta que conté totes les imatges. Fixeu-vos que en el nom del fitxer hi surt la ciutat i la data
en la que la fotografia ha estat presa.

### Exemple d'una imatge
![berlin_000001_000019_leftImg8bit_15-01-2018.png](/dataset_cities/images/berlin_000001_000019_leftImg8bit_15-01-2018.png)

- labels: En aquesta carpeta trobareu els arxius .txt amb el mateix nom base que la imatge a la que correspon. A cada arxiu hi hauran tantes linees com objectes trobats a la imatge. Per a cada objecte trobareu 6 columnes amb la següent informació:

### Exemple d'un arxiu de labels:
2 0.454346 0.441895 0.0405273 0.0576172 0.205418 \
[...] on
* **identificador de l'objecte**: enter entre 0 i 80, que són la quantitat d'objectes que contempla el model de YOLO (us donem una relació entre l'identificador i el tipus d'objete a l'arxiu class_name.txt)
* **coordenades objecte $x^n_c$, $y^n_c$ , $w^n$ , $h^n$**: La posició de l'objecte detectat es defineix per la *bounding box*, que és el rectangle que conté l'objecte. Aquest ve definit per 4 coordenades, en aquest cas les coordenades són el valor central ( $x^n_c$ , $y^n_c$ ), l'amplada i l'alçada ( $w^n$ , $h^n$ ). YOLO dóna tots aquests valors normalitzats, per tant es trobaran entre 0 i 1, és a dir, les coordenades horitzon tals van dividides per l'amplada total de la imatge i les coordenades verticals per l'alçada total de la imatge
* **confiança de la detecció**: la última columna tenim la probabilitat que dóna el model de YOLO de que la posició de l'objecte sigui la correcta.

De tal manera que, l'unió entre els dos arxius corresponents, quedaría tal que així:
### Exemple de resultat desitjat:
![berlin_000001_000019_leftImg8bit_15-01-2018.png i berlin_000001_000019_leftImg8bit_15-01-2018.txt](/dataset_cities/Ex3_Fig1.png)

## Com funciona el codi?

S'ha fet proves amb èxit tant en un entorn virtual de distribució Ubuntu 20.04 LTS com Windows 10 21h2. Teniu a disposició de les versions de les llibreries emprades a requirements.txt així com la llicència de distribució de la present.

### Input format

El codi no exigeix cap argument, tot i que espera que tinguem a disposició dels arxius amb el seu format corresponent dintre del dataset (dataset_cities/images/, dataset_cities/labels/ i dataset_cities/class_name.txt), ja bé sigui amb els noms d'aquests ordenats com desordenats. Opcionalment, es pot introduir manualment la seva ruta del projecte ubicada en el seu sistema en qüestió, però, remarcar que no cal afegir-la perquè està automatitzat per a que el codi ens llegeixi la ruta on es localitza el projecte des del main fins a la resta d'arxius esmentats.

Pycharm:
Per tant, *premeu l'opció **RUN** directament i vegeu per consola tot l'anàlisi desenvolupat* exclusivament al mòdul main() -- Ídem a l'opció de test files(testutils i testplots).

Consola: (des de l'ubicació del projecte principal - main) -- Ídem a l'opció de test files(testutils i testplots): \
$ python3 main.py

### Consola (Ubuntu) - Coverage:
Per analitzar Coverage dels tests. Cal seguir les següents pases:

1. Install Coverage.py (omitiu aquest pas en cas instal·lat):\
 $ pip install coverage
 
2. Comprovació:\
$ coverage --version

3. Execució: utilitzeu -lo per executar el vostre conjunt de proves i recopilar dades: \
$ coverage run -m unittest discover

4. Utilitzeu -lo per informar dels resultats: coverage report:\
$ coverage report -m testutils.py \
$ coverage report -m testplots.py


### Program output

El codi ens mostra per consola tot el desenvolupament del projecte. A més, l'ús de gràfics s'obren automàticament a través del navegador que tingeu per defecte. Un cop executat el codi, llegirà seqüencialment fins a arribar a l'últim punt amb èxit on podreu veure tot l'anàlisi emprat.
