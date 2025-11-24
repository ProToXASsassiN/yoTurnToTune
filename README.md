# yoTuneToTune - Effets de Guitare Gratuits

Un processeur d'effets de guitare **100% gratuit** pour Windows qui transforme ton ordinateur en pedale d'effets!

## Caracteristiques

### Types de Distortion
- **Overdrive** - Son chaud et doux, parfait pour le blues et le rock
- **Fuzz** - Son agressif et vintage, ideal pour le rock psychedelique
- **Metal** - Distortion moderne et agressee pour le metal
- **Clean Boost** - Amplification propre sans distortion

### Controles en Temps Reel
- **Gain** - Controle l'intensite de la distortion (1.0 a 20.0)
- **Level** - Ajuste le volume de sortie (0.0 a 1.0)
- **Tone** - Filtre passe-bas pour controler les aigus (0.0=sombre, 1.0=brillant)

## Installation

### Prerequis
1. **Python 3.7 ou superieur**
   - Telecharge depuis: https://www.python.org/downloads/
   - IMPORTANT: Coche "Add Python to PATH" pendant l'installation!

2. **Interface Audio** (recommande)
   - Une interface audio USB avec entree instrument
   - Pilotes ASIO pour une latence minimale (optionnel mais recommande)
   - Exemples: Focusrite Scarlett, Behringer UMC, PreSonus AudioBox

### Installation Rapide

1. **Telecharge le dossier yoTuneToTune**

2. **Double-clique sur `lancer.bat`**
   - Le script va automatiquement installer les dependances
   - Puis lancer le programme

**C'est tout!**

### Installation Manuelle (optionnel)

Si le script automatique ne fonctionne pas:

```cmd
cd yoTuneToTune
pip install -r requirements.txt
python guitar_fx.py
```

## Utilisation

### Branchement
1. Branche ta guitare a l'entree de ton interface audio
2. Branche ton casque ou ampli a la sortie de l'interface audio
3. Lance `lancer.bat`

### Configuration
1. Le programme affichera la liste des peripheriques audio
2. Entre le numero du peripherique d'ENTREE (ta guitare)
3. Entre le numero du peripherique de SORTIE (ton casque/ampli)
4. Appuie sur Entree pour demarrer

### Commandes Pendant l'Execution

Une fois le programme lance, tape ces commandes:

- `d` - Changer le type de distortion
- `g` - Ajuster le gain (intensite)
- `l` - Ajuster le level (volume de sortie)
- `t` - Ajuster le tone (tonalite)
- `i` - Voir les parametres actuels
- `q` - Quitter

### Exemple de Session

```
> d
Types disponibles:
  1. overdrive (chaud et doux)
  2. fuzz (agressif et vintage)
  3. metal (moderne et agressif)
  4. clean (boost propre)
Choix (1-4): 2
Type change: fuzz

> g
Gain actuel: 5.0 | Nouveau (1.0-20.0): 8.5
Gain: 8.5

> t
Tone actuel: 0.50 | Nouveau (0.0-1.0): 0.7
Tone: 0.70 (0=sombre, 1=brillant)

> i
Parametres actuels:
  Type: fuzz
  Gain: 8.5
  Level: 0.50
  Tone: 0.70
```

## Conseils pour une Meilleure Experience

### Reduire la Latence
1. Utilise une interface audio USB (pas la carte son integree)
2. Installe les pilotes ASIO pour ton interface
3. Ferme les autres applications audio
4. Reduis la taille du buffer audio (dans les parametres de ton interface)

### Reglages Recommandes par Style

**Blues/Rock Classique**
- Type: overdrive
- Gain: 4.0 - 7.0
- Level: 0.5 - 0.6
- Tone: 0.5 - 0.7

**Rock Psychedelique**
- Type: fuzz
- Gain: 8.0 - 12.0
- Level: 0.4 - 0.5
- Tone: 0.6 - 0.8

**Metal Moderne**
- Type: metal
- Gain: 10.0 - 15.0
- Level: 0.5 - 0.6
- Tone: 0.4 - 0.6

**Boost Propre**
- Type: clean
- Gain: 3.0 - 8.0
- Level: 0.6 - 0.8
- Tone: 0.7 - 1.0

## Depannage

### "Python n'est pas installe"
- Telecharge Python depuis https://www.python.org/downloads/
- IMPORTANT: Coche "Add Python to PATH" pendant l'installation
- Redemarre ton ordinateur apres installation

### "Aucun peripherique audio detecte"
- Verifie que ton interface audio est branchee
- Installe les pilotes de ton interface audio
- Verifie dans les parametres Windows que l'interface est reconnue

### "Latence trop importante"
- Utilise une interface audio USB (pas la carte son integree)
- Installe les pilotes ASIO de ton interface
- Reduis la taille du buffer dans les parametres de l'interface
- Ferme les autres applications

### "Son sature/distordu meme en clean"
- Baisse le gain de ta guitare
- Reduis le parametre "Level" dans le programme
- Verifie le niveau d'entree de ton interface audio

### "Pas de son"
- Verifie que tu as selectionne les bons peripheriques
- Augmente le parametre "Level"
- Verifie le volume de ton interface audio
- Verifie que ton casque/ampli est bien branche

## Structure du Projet

```
yoTuneToTune/
├── guitar_fx.py       # Programme principal
├── requirements.txt   # Dependances Python
├── lancer.bat        # Script de lancement Windows
└── README.md         # Ce fichier
```

## Technologies Utilisees

- **Python 3** - Langage de programmation
- **NumPy** - Traitement numerique pour les effets audio
- **SoundDevice** - Interface audio en temps reel

## Licence

Ce projet est gratuit et open source. Utilise-le, modifie-le, partage-le comme tu veux!

## Auteur

Cree avec Claude Code

## Support

Si tu rencontres des problemes:
1. Lis la section Depannage ci-dessus
2. Verifie que Python est correctement installe
3. Verifie que ton interface audio fonctionne dans d'autres applications

## Roadmap Future (idees)

- Interface graphique (GUI)
- Plus d'effets (delay, reverb, chorus)
- Presets sauvegardables
- Accordeur integre
- Support MIDI pour pedalier
- Enregistrement audio

---

**Bon jeu et bon rock!**
