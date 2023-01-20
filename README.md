# YOLO_Dataset

## En que consisteix aquest repository?

Ens han encarregat analitzar imatges de carrers de diferents ciutats europees, per un projecte relacionat amb smart-cities. Per tal de començar el projecte, tenim un datatset d'imatges de tres ciutats on les imatges han estat filmades des d'un cotxe des de diferents punts de la ciutat. El data set complet el podeu trobar aquí
(https://www.cityscapes-dataset.com). Junt amb les imatges ens han donat també uns fitxers de text on podem trobar els tipus d'objecte que hi ha i les posicions per cada un d'ells, de tal manera que tenim un fitxer de text per a cada imatge. Ens indiquen que aquesta informació s'ha extret utilitzant YOLOv5 (https://docs.ultralytics.com), (YOLO, You Only Look Once) que és un algoritme basat en xarxes convolucionals molt potent per a la detecció d'objectes en temps real.

En aquesta PAC haureu de treballar amb aquests fitxers per tal d'analitzar les imatges i extreure'n conclusions sense haver de mirar cadascuna de les imatges.
La carpeta dataset s'estrctura de la manera següent:
• images: Carpeta que conté totes les imatges. Fixeu-vos que en el nom del fitxer hi surt la ciutat i la data
en la que la fotografia ha estat presa.

### Exemple d'una imatge
![berlin_000001_000019_leftImg8bit_15-01-2018.png](/dataset_cities/images/berlin_000001_000019_leftImg8bit_15-01-2018.png)

