# YOLO_Dataset

## En que consisteix aquest repository?

Ens han encarregat analitzar imatges de carrers de diferents ciutats europees, per un projecte relacionat amb smart-cities. Per tal de començar el projecte, tenim un datatset d'imatges de tres ciutats on les imatges han estat filmades des d'un cotxe des de diferents punts de la ciutat. El data set complet el podeu trobar aquí
(https://www.cityscapes-dataset.com). Junt amb les imatges ens han donat també uns fitxers de text on podem trobar els tipus d'objecte que hi ha i les posicions per cada un d'ells, de tal manera que tenim un fitxer de text per a cada imatge. Ens indiquen que aquesta informació s'ha extret utilitzant YOLOv5 (https://docs.ultralytics.com), (YOLO, You Only Look Once) que és un algoritme basat en xarxes convolucionals molt potent per a la detecció d'objectes en temps real.

En aquesta PAC haureu de treballar amb aquests fitxers per tal d'analitzar les imatges i extreure'n conclusions sense haver de mirar cadascuna de les imatges. La carpeta dataset s'estrctura de la manera següent:
- images: Carpeta que conté totes les imatges. Fixeu-vos que en el nom del fitxer hi surt la ciutat i la data
en la que la fotografia ha estat presa.

### Exemple d'una imatge
![berlin_000001_000019_leftImg8bit_15-01-2018.png](/dataset_cities/images/berlin_000001_000019_leftImg8bit_15-01-2018.png)

- labels: En aquesta carpeta trobareu els arxius .txt amb el mateix nom base que la imatge a la que correspon. A cada arxiu hi hauran tantes linees com objectes trobats a la imatge. Per a cada objecte trobareu 6 columnes amb la següent informació:

### Exemple d'un arxiu de labels:
2 0.454346 0.441895 0.0405273 0.0576172 0.205418
2 0.490723 0.438965 0.0234375 0.0615234 0.2438
[...] on
* **identificador de l'objecte**: enter entre 0 i 80, que són la quantitat d'objectes que contempla el model de YOLO (us donem una relació entre l'identificador i el tipus d'objete a l'arxiu class_name.txt)
* **coordenades objecte $x^n_c$,$y^n_c$, $w^n$, $h^n$**: La posició de l'objecte detectat es defineix per la *bounding box*, que és el rectangle que conté l'objecte. Aquest ve definit per 4 coordenades, en aquest cas les coordenades són el valor central *($x^n_c$,$y^n_c$)*, l'amplada i l'alçada *($w^n$, $h^n$)*. YOLO dóna tots aquests valors normalitzats, per tant es trobaran entre 0 i 1, és a dir, les coordenades horitzon tals van dividides per l'amplada total de la imatge i les coordenades verticals per l'alçada total de la imatge
* **confiança de la detecció**: la última columna tenim la probabilitat que dóna el model de YOLO de que la posició de l'objecte sigui la correcta.
