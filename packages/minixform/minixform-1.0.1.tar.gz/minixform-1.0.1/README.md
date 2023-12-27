<i>
	<p>Un module python pour faire des questionnaires par :<br>
		<center>la centrale-cognitive</center>
	</p>
</i>

## Contexte du projet et problematique
<p style="text-align:justify;">
	Concevoir des questionnaires, voici quelque chose que nous faisons toujours pour mener des enquêtes. Depuis quelques années maintenant, nous sommes passés de questionnaires papier aux questionnaires mobiles assez simple, pratiques et permettant d’éviter beaucoup d’erreurs dû au reportage. Gain de temps, économie, … Voici quelques avantages facilement visibles de prime à bord. ODK et <b>KOBOTOOLBOX</b> sont des outils qui rentrent dans le même contexte et qui permettent en plus la collecte de données hors ligne, un gros avantage pour les enquêtes en milieu rural où l’accès à Internet n’est pas toujours évident dans nos localités. Il existe des Builder pour chacun de ces outils. Un Builder est intégré à KOBOTOOLBOX et ODK Build pour les questionnaires ODK. Une autre méthode pour faire des questionnaires compatibles avec ses deux plateformes est de faire un fichier Excel respectant les normes de formulaire <b>XLSFORM</b>. Bien que XLSFORM soit rapide, simple et facile à personnaliser, manipuler des feuilles Excel reste tout de même assez fastidieux et ennuyeux. MiniXform vient comme une solution pour palier à ce problème.
</p>



## Installation

Il suffit de tapper la commande suivante dans votre terminal: 

```bash
pip install minixform
```


## TREE Actuelle du projet


## Téléchargement et execution

Si vous arrivez à voir ce dépot, c'est que vous avez été ajouté comme collaborateur au projet. <br>

- Vous devez avoir *python* et *git* installés sur votre machine
- Vous devez connaitre les essentiels et indispensable pour travailler en collaboration sur github en utilisant *git* en ligne de commande. <br>

*langage : python3*
*Packages de teste: streamlit*



`model_questionnaire.mxf` 

```yaml
parametres:
  titre: Questionnaire coopérative PPCA
  description: >
    Il s'agit d'un questionnaire rélative au coopérative de production de noix brute de cajou. Ce questionnaire à été dréssé dans le cadre de mappind des parcelles des producteurs. Il vise à avoir des informations sur les coopérative en elles même à fin de mieux les connaitres.


  date: 2023-05-04
  auteur:
    - Nom: KOUAME
      Prenom: Koffi
      Email: kanicetcyrille@gmail.com
      Tel: 0707070707
  serveur: 'google_sheet'
  metadata:
    [
      start,
      end,
      today,
      deviceid,
      phonenumber,
      username,
      email,
      audit,
      simserial,
    ]

choix:
  sexe: &sexe
    - Homme
    - Femme
  bool: &bool [Oui, Non]
  enqueteurs: _(modeles/excel_csv/enqueteurs.csv)
  lieu: _(modeles/excel_csv/lieu.csv)
  region: &region ['Bélier', "N'zi", 'Zanzan', 'Moronou', 'Cavali']

questions:
  I:
    titre: "DONNEES SUR L'ENQUETEUR"
    description: Il s'agit de meta données sur les eqnueêteurs et l'enquête en vu d'assurer la tracabilitée des données. _note
    date: Date d'enquête (jj-mm-aaaa) _date
    nom_enqueteur:
      - Nom et prénoms de l'enqueteur() _s1
      - [enqueteurs.nom]
    num_enqueteur:
      Numéro de l'enqueteur (Doit être un numéro à 10 chiffre) $(num)
      # - [enqueteurs.num]
    Source_info: Nom et prénoms de la source d'information() _texte
    lieu_enqu:
      - Lieu d'enquête() _s1
      - [yamoussoukro, bonon, bouaflé, zatta]
  II:
    titre: SIEGE DE LA COOPERATIVE
    1:
      - Nom de la coopérative()
      - [Copab, Scopako, Coprodigo, Copavgon]
    2: Année de création de la coopérative() _date_annee
    3:
      - Region de la coopérative() _s1
      - *region
    4:
      - Departement de la coopérative()
      - [lieu.departement]
    5: Nombre d'établissement primaires() _e **
    6: Nombre d'établissement secondaire() _e **
    7: Nombre d'établissement sanitaire() _e **
    8: Nombre de femmes() _e
    9: Nombre d'hommes() _e
    10:
      - Activité economique()
      - [
          Pèche,
          Maraicher,
          Cultures de rentes,
          Chasse,
          Industries,
          Commerce,
          Artisanat,
        ]
    11:
      - Avez vous une unité de transformation ?() _s1 **
      - *bool
    12:
      - Si oui() $si(II_11=Oui)
      - g:
          1: Nombre d'unité de transformation() _i
          2: Capacité de transformation (en tonne/an) _r {$>1}
  III:
    titre: SECTIONS DE LA COOPERATIVE
    1: Nombre de section _entier()
    table_1:
      legende: Information sur la sectione
      lignes: [III_1]
      colonnes:
        - - Nom de la section()
          - [goumere, tankesse, goutouko, coutou]
        - Nom du responsable de la section() _texte
        - Nombre de magasin de stockage() _i
        - Capacité totale des magasins de stockage (En tonnes) _entier
        - Coordonnées du siège() _geopoint
        - production: production de la campagne précedentes(en tonnes) _entier
  IV:
    titre: VEHICULES DE LA COOPERATIVE
    1:
      - types de véhicules
      - [Moto, Tricyle, Rémorque, Camion, Vélo, Baché, Autre]
    g1:
      1: Nombre de moto() _i
      2: Nombre de tricyle() _i
      3: Nombre de Remorque() _i
      4: Nombre de camion() _i
      5: Nombre de vélo() _i
      6: Nombre de bachés() _i
      7: Nombre d'autre produit() _entier
    table-1:
      legende: Informations sur les véhicules
      colonnes:
        [
          Modèle (Modele du vehicule) _texte,
          Année (Année d'achat du véhicule) _annee,
          Nombre (Nombre de véhicule) _entier,
        ]
      lignes:
        - Moto
        - tricyle
        - Remorques
        - Camion
        - Vélo
        - Baché
        - Autre

    table-2:
      legende: Informations sur les véhicules
      colonnes:
        [
          Modèle (Modele du vehicule) _texte,
          Année (Année d'achat du véhicule) _annee,
          Nombre (Nombre de véhicule) _entier,
        ]
      lignes: [1]

```

Ce exemple montre la structuration d'un fichier MiniXform (.mxf):
<p style="text-align:justify;">
	--- : Sépare le questionnaire en trois parties (Settings, Choices, Survey) <br>
	**titre : Represente le debut d'un groupe ou une liste <br>
	x,texte : represente une question avec x le numero d'ordre de la question <br>
	(texte) : Description d'une question <br>
	::type : type de la question <br>
	{...}: regle ou contrainte de la question <br>
	[*oui_non] ou [feminin,masculain]: liste de choix de la question <br>
</p>

<br>
La liste des types est définie comme suit:

| XLSFORM                   | MINIXFORM |
|---------------------------|-----------|
| integer                   | i         |
| integer                   | e         |
| decimal                   | r         |
| decimal                   | d         |
| range                     | rg        |
| text                      | t         |
| text                      | txt       |
| select_one                | so        |
| select_one                | liste_u   |
| select_one                | lu        |
| select_one                | liste u   |
| select_multiple           | sm        |
| select_multiple           | lm        |
| select_one_from_file      | sof       |
| select_multiple_from_file | smf       |
| rank                      | rk        |
| rank                      | rn        |
| note                      | n         |
| note                      | nt        |
| geopoint                  | point     |
| geotrace                  | trace     |
| geoshape                  | shape     |
| date                      | de        |
| date                      | date      |
| time                      | tm        |
| time                      | te        |
| dateTime                  | dtme      |
| image                     | img       |
| audio                     | audio     |
| audio                     | o         |
| background-audio          | bg-audio  |
| video                     | video     |
| video                     | v         |
| file                      | f         |
| barcode                   | bc        |
| calculate                 | calc      |
| acknowledge               | ack       |
| hidden                    | hd        |
| xml-external              | xml       |
| begin_group               | g         |
| begin_group               | group     |
| end_group                 | end       |
| end_group                 | eg        |
| repeat_group              | repeat    |
| repeat_group              | re        |
| end_repeat                | er        |
| end_repeat                | endr      |
