# yoTuneToTune PRO - Studio Edition

**Interface graphique premium avec tous les effets des logiciels professionnels!**

## Nouveautes PRO

### Interface Graphique Premium
- Design professionnel noir/gris avec accents orange
- Controles visuels avec sliders pour tous les parametres
- Boutons de presets rapides
- Interface intuitive et moderne
- Aucun degradé violet d'IA - design sobre et professionnel!

### Effets Professionnels Complets

#### AMPLIFICATEUR/DISTORTION
- **Clean** - Son cristallin
- **Blues** - Doux avec harmoniques
- **Crunch** - Rock classique
- **Overdrive** - Chaud et doux
- **Fuzz** - Agressif vintage
- **Metal** - Moderne et puissant

#### EQUALIZER 3 BANDES
- **Bass** - Controle des graves
- **Mid** - Controle des mediums
- **Treble** - Controle des aigus
- Ajustement precis de -100% a +100% sur chaque bande

#### DELAY/ECHO
- **Mix** - Dosage de l'effet
- **Time** - Temps de delai (0.1s a 1.0s)
- **Feedback** - Nombre de repetitions
- Parfait pour les solos et le rock psychedelique

#### REVERB
- **Mix** - Dosage de la reverb
- **Size** - Taille de la salle
- Ajoute de la profondeur et de l'espace a ton son

#### CHORUS
- **Depth** - Profondeur de la modulation
- **Rate** - Vitesse de la modulation
- Pour un son riche et spacieux

#### COMPRESSOR
- Lisse les dynamiques
- Sustain accru
- Son plus professionnel

### 12 Presets Professionnels Pre-configures

1. **CLEAN JAZZ** - Son propre avec reverb et chorus
2. **BLUES CLASSIC** - Blues authentique avec harmoniques
3. **ROCK CLASSIC** - Rock des annees 70-80
4. **ROCK MODERNE** - Rock contemporain puissant
5. **METAL MODERNE** - Metal precis et agressif
6. **METAL HEAVY** - Maximum de gain pour le metal extreme
7. **PUNK ROCK** - Fuzz energique des annees 70
8. **PSYCHEDELIC** - Fuzz + delay + reverb + chorus
9. **INDIE ROCK** - Son indie avec effets atmospheriques
10. **GRUNGE** - Le son de Seattle
11. **HARD ROCK** - AC/DC, Led Zeppelin style
12. **LEAD SOLO** - Optimise pour les solos avec delay

## Installation

### Prerequis
- **Python 3.7+** avec Tkinter (inclus par defaut)
- **Interface audio** (recommande pour une latence minimale)
- **Pilotes ASIO** (optionnel mais recommande)

### Lancement Rapide

**Double-clique sur `lancer_pro.bat`**

C'est tout! L'interface graphique s'ouvrira automatiquement.

## Utilisation de l'Interface

### 1. Configuration Audio
1. Clique sur "VOIR LES PERIPHERIQUES" pour lister tes interfaces audio
2. Note le numero de ton interface d'entree (guitare)
3. Note le numero de ton interface de sortie (casque/ampli)
4. Entre ces numeros dans les champs "Device IN" et "Device OUT"

### 2. Choix Rapide avec Presets
1. Clique simplement sur un des 12 presets dans la colonne de droite
2. Tous les parametres se configurent automatiquement
3. Clique sur "START" pour commencer a jouer
4. Ajuste les parametres en temps reel avec les sliders

### 3. Configuration Manuelle
- **Section AMPLIFICATEUR** : Choisis ton type de distortion et ajuste Gain/Level/Tone
- **Section EQUALIZER** : Sculpte ton son avec Bass/Mid/Treble
- **Section DELAY** : Active et configure l'echo
- **Section REVERB** : Ajoute de la profondeur
- **Section CHORUS** : Enrichis ton son
- **Section COMPRESSOR** : Active pour un son plus pro

### 4. Controle en Temps Reel
- Tous les sliders fonctionnent en temps reel pendant que tu joues
- Change de type de distortion instantanement avec les boutons
- Active/desactive les effets avec les checkboxes
- Charge un nouveau preset a tout moment

## Exemples de Reglages

### Solo de Guitare Rock
1. Charge le preset "LEAD SOLO"
2. Ou configure manuellement :
   - Type: Overdrive
   - Gain: 7.5
   - Tone: 0.7 (brillant)
   - EQ: Bass 0.4, Mid 0.7, Treble 0.7
   - Delay: ON (Mix 0.3, Time 0.35s)
   - Reverb: ON (Mix 0.25)

### Rythmique Metal
1. Charge le preset "METAL MODERNE"
2. Ou configure :
   - Type: Metal
   - Gain: 12.0
   - Tone: 0.45
   - EQ: Bass 0.7, Mid 0.4, Treble 0.6
   - Compressor: ON
   - Autres effets: OFF

### Ambiance Psychedelique
1. Charge le preset "PSYCHEDELIC"
2. Ou configure :
   - Type: Fuzz
   - Gain: 9.0
   - Delay: ON (Mix 0.35, Feedback 0.5)
   - Reverb: ON (Mix 0.3)
   - Chorus: ON (Depth 0.4)

## Comparaison avec les Logiciels Payants

| Fonctionnalite | yoTuneToTune PRO | Logiciels Payants |
|----------------|------------------|-------------------|
| Distortion/Overdrive | ✓ 6 types | ✓ |
| Equalizer 3 bandes | ✓ | ✓ |
| Delay | ✓ | ✓ |
| Reverb | ✓ | ✓ |
| Chorus | ✓ | ✓ |
| Compressor | ✓ | ✓ |
| Presets | ✓ 12 presets | ✓ |
| Interface graphique | ✓ Premium | ✓ |
| Controles temps reel | ✓ | ✓ |
| **Prix** | **GRATUIT** | **50-200€** |

## Conseils Pro

### Pour Reduire la Latence
1. Utilise une interface audio USB (Focusrite, Behringer, PreSonus)
2. Installe les pilotes ASIO de ton interface
3. Configure la taille du buffer a 256 samples ou moins
4. Ferme les autres applications

### Pour un Son Optimal
1. Commence avec un preset qui correspond a ton style
2. Ajuste le gain jusqu'a obtenir la distortion voulue
3. Utilise l'EQ pour sculpter ton son
4. Ajoute les effets (delay/reverb) avec parcimonie (mix < 0.3 en general)
5. Termine avec le niveau master

### Ordre de la Chaine d'Effets
Le signal passe dans cet ordre :
1. Distortion/Amplification
2. Equalizer
3. Tone Control
4. Compressor
5. Chorus
6. Delay
7. Reverb
8. Master Level

Cet ordre a ete optimise pour un son professionnel!

## Depannage

### L'interface ne s'ouvre pas
- Verifie que Python avec Tkinter est installe
- Sur Windows, Tkinter est inclus par defaut avec Python

### Latence trop importante
- Utilise une interface audio USB
- Installe les pilotes ASIO
- Reduis la taille du buffer dans les parametres de l'interface

### Son sature
- Baisse le GAIN
- Baisse le LEVEL
- Verifie le niveau d'entree de ton interface audio

### Pas de son
- Verifie les numeros de peripheriques
- Clique sur "VOIR LES PERIPHERIQUES" pour verifier
- Assure-toi d'avoir clique sur START

## Structure du Projet

```
yoTuneToTune/
├── guitar_fx.py         # Version console basique
├── guitar_fx_pro.py     # Moteur audio PRO complet
├── gui_premium.py       # Interface graphique premium
├── lancer.bat           # Lance version console
├── lancer_pro.bat       # Lance version GUI PRO
├── requirements.txt     # Dependances Python
├── README.md            # Documentation basique
└── README_PRO.md        # Ce fichier (documentation PRO)
```

## Technologies

- **Python 3** - Langage
- **NumPy** - Traitement du signal audio
- **SoundDevice** - Interface audio temps reel
- **Tkinter** - Interface graphique

## Licence

100% Gratuit et Open Source!

## Support

Pour toute question, verifie d'abord la section Depannage ci-dessus.

---

**Rock on!**
