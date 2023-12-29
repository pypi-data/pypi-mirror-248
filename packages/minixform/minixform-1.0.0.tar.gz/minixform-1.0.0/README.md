<i>
	<p>Un module python pour faire des questionnaires par :<br>
		<center>la centrale-cognitive</center>
	</p>
</i>

## Contexte du projet et problematique

<p style="text-align:justify;">
Un Builder est intégré à <b>KOBOTOOLBOX</b> et ODK Build permet de réaliser les questionnaires ODK. Une autre méthode pour faire des questionnaires compatibles avec ses deux plateformes est de faire un fichier Excel respectant les normes de formulaire <b>XLSFORM</b>. Bien que XLSFORM soit rapide, simple et facile à personnaliser, manipuler des feuilles Excel reste tout de même assez fastidieux et ennuyeux. MiniXform vient comme une solution pour palier à ce problème en permettant de creer un formulaire XLSFORM grace au langage yaml.
</p>

## Installation

Il suffit de tapper la commande suivante dans votre terminal:

```bash
pip install minixform
```

## Utilisation

Le principe d'utilisation est simple: creer un fichier minixform en yaml le convertir avec minixform en XLSFORM

```mermaid
graph TD
	yaml[Fichier yaml formaté en minixform \n formulaire_minixform.yaml]--> minixform[Conversion du formulaire avec minixform: \n from minixform import * \n form=Questionnaire_yaml('formulaire_minixform.yaml') \n form.to_xslform('formulaire_xlsform.xlsx')]
	minixform-->xlsform[Fichier xlsform prèt à être deployé: \n formulaire_xlsform.xlsx]
```

### Creation d'un formulaire minixform

Vous pouvez creer votre fichier de fomulaire minixform basé sur le modele suivant:

`model_formulaire.yaml`

```yaml
# Les parametres du formulaire qui comprennent le titre, la description et les metadonnées à ajouter au formulaire.
parametres:
  titre: Voici le titre de la demo
  description: >
    ici vous pouvez decrire votre formulaire. Cette description sera ajouter a votre formulaire numerique deployé.


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

# Liste des proposition de choix unique ou multiples (la feuille choices de XLSFORM)
choix:
  sexe: &sexe
    - Homme
    - Femme
  bool: &bool [Oui, Non]
  enqueteurs: _(modeles/excel_csv/enqueteurs.csv)
  lieu: _(modeles/excel_csv/lieu.csv)
  region: &region ['Bélier', "N'zi", 'Zanzan', 'Moronou', 'Cavali']

# Correspont a la feuille survey qui est la liste des questions du formulaire.
questions:
  I: # groupe I
    titre: "DONNEES SUR L'ENQUETEUR"
    description: Il s'agit de meta données sur les eqnueêteurs et l'enquête en vu d'assurer la tracabilitée des données. _note
    date: Date d'enquête (jj-mm-aaaa) _date
    nom_enqueteur: #
      - Nom et prénoms de l'enqueteur() _s1
      - [enqueteurs]
    num_enqueteur: Numéro de l'enqueteur (Doit être un numéro à 10 chiffre) $(num) # Modele d'une question
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

### Composition du formulaire et syntaxe

Ce exemple montre la structuration d'un fichier MiniXform (.yaml).

Il est composé de 3 partie : 1- parametres : La liste des parametres compotant le titre, la descrition et les meta données à inclure dans le formulaire 2- choix : la liste des choix correspondant à feuille choices d'un formulaire XLSFORM Une liste de choix se presente sous la forme suivant:

```yaml
sexe:
  &sexe # $sexe est la clé de la liste et est generalement identique au nom de la liste
  - Homme # les proposition de choix peuvent être ecrit aussi dans une liste python comme
  - Femme
```

3-questions : Cette partie est composé des groupes et questions. Les questions sont de plusieurs types qui sont les types de

La liste des types est définie comme suit:

| XLSFORM                   | MINIXFORM |
| ------------------------- | --------- |
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

Les questions sont organisées en groupes.

```yaml
questions: # Debut des groupes des questions
  I: # groupe I
    titre: "DONNEES SUR L'ENQUETEUR" # Titre du groupe
    description: Il s'agit de meta données sur les eqnueêteurs et l'enquête en vu d'assurer la tracabilitée des données. _note # Description groupe de question
    date: Date d'enquête (jj-mm-aaaa) _date # Une question de type date
    nom_enqueteur: Nom de l'enquêteur (Saisir en majuscule) _txt
    num_enqueteur:
      Numéro de l'enqueteur (Doit être un numéro à 10 chiffre) $(num) # Modele d'une question
    Source_info: Nom et prénoms de la source d'information() _texte
    region_enquete:
      - Région (selectionner une region)  _s1
      - *regions # region se trouve dans la liste
    lieu_enqu:
      - Lieu d'enquête() _s1 # question à choix unique
      - [yamoussoukro, bonon, bouaflé, zatta] # Liste de choix
```

La structure d'une question est la suivante :

```yaml
nom_question: La question est posé ici (La description de la question est entre les paranthèses ) _typequestion $[proposition1, proposition2, proposition3]
```

### Execution de minixform

J'utilise **pew** pour ce faire. Pour installer pew, vous pouvez faire

```bash
pip install pew
```

Creer et activer un nouvelle environnement virtuel en faisant

```bash
pew new venv
pew workon venv
```

Puis installer minixform

```bash
pip install minixform
```

Creer ensuite le fichier yaml du formulaire **formulaire.yaml** et le fichier de script python **main.py**.

```python
from minixform import *
form = yaml_form("formulaire.yaml")
resultat = form.to_xslform("formulaire.xlsx")
```

Pour executer le script, il suffit de faire

```bash
py main.py
```
