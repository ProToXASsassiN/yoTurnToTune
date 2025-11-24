#!/usr/bin/env python3
"""
yoTuneToTune - Processeur d'effets de guitare gratuit
Distortion, Fuzz, Overdrive et plus encore!
"""

import numpy as np
import sounddevice as sd
import sys
from typing import Optional

class GuitarFX:
    def __init__(self, sample_rate=44100, block_size=512):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.running = False

        # Parametres des effets
        self.distortion_type = "overdrive"
        self.gain = 5.0  # Gain d'entree (1.0 a 20.0)
        self.level = 0.5  # Niveau de sortie (0.0 a 1.0)
        self.tone = 0.5   # Controle de tonalite (0.0 a 1.0)

        # Filtre passe-bas pour le controle de tonalite
        self.filter_state = 0.0

    def overdrive(self, audio):
        """Distortion type overdrive - son chaud et doux"""
        # Amplification
        x = audio * self.gain
        # Soft clipping asymetrique
        y = np.where(x > 0,
                     1 - np.exp(-x),
                     -1 + np.exp(x))
        return y

    def fuzz(self, audio):
        """Distortion type fuzz - son agressif et vintage"""
        x = audio * self.gain * 2
        # Hard clipping avec asymetrie
        y = np.clip(x, -0.7, 1.0)
        # Ajoute des harmoniques
        y = np.tanh(y * 2)
        return y

    def metal(self, audio):
        """Distortion type metal - son moderne et agressif"""
        x = audio * self.gain * 1.5
        # Multi-stage clipping
        y = np.tanh(x)
        y = np.tanh(y * 3)
        return y

    def clean_boost(self, audio):
        """Boost propre sans distortion"""
        return audio * self.gain * 0.3

    def apply_tone_control(self, audio):
        """Filtre passe-bas pour controle de tonalite"""
        # Filtre simple premier ordre
        alpha = self.tone
        output = np.zeros_like(audio)

        for i, sample in enumerate(audio):
            self.filter_state = alpha * sample + (1 - alpha) * self.filter_state
            output[i] = self.filter_state

        return output

    def process_audio(self, indata, outdata, frames, time, status):
        """Callback pour traitement audio en temps reel"""
        if status:
            print(f"Statut: {status}", file=sys.stderr)

        # Recupere l'audio d'entree (mono)
        audio = indata[:, 0] if indata.shape[1] > 0 else indata

        # Applique la distortion selectionnee
        if self.distortion_type == "overdrive":
            processed = self.overdrive(audio)
        elif self.distortion_type == "fuzz":
            processed = self.fuzz(audio)
        elif self.distortion_type == "metal":
            processed = self.metal(audio)
        elif self.distortion_type == "clean":
            processed = self.clean_boost(audio)
        else:
            processed = audio

        # Applique le controle de tonalite
        processed = self.apply_tone_control(processed)

        # Ajuste le niveau de sortie
        processed = processed * self.level

        # Evite le clipping final
        processed = np.clip(processed, -1.0, 1.0)

        # Copie vers la sortie (stereo)
        outdata[:, 0] = processed
        if outdata.shape[1] > 1:
            outdata[:, 1] = processed

    def start(self):
        """Demarre le traitement audio"""
        print("\n" + "="*50)
        print("     yoTuneToTune - Effets Guitare Gratuits")
        print("="*50 + "\n")
        print("Peripheriques audio disponibles:")
        print(sd.query_devices())
        print("\n")

        try:
            # Demande le peripherique d'entree
            input_device = input("Numero du peripherique d'ENTREE (guitare): ").strip()
            output_device = input("Numero du peripherique de SORTIE (ampli/casque): ").strip()

            input_device = int(input_device) if input_device else None
            output_device = int(output_device) if output_device else None

            print(f"\nConfiguration:")
            print(f"  - Type: {self.distortion_type}")
            print(f"  - Gain: {self.gain}")
            print(f"  - Level: {self.level}")
            print(f"  - Tone: {self.tone}")
            print("\nCommandes disponibles pendant l'execution:")
            print("  d = changer type distortion")
            print("  g = ajuster gain")
            print("  l = ajuster level")
            print("  t = ajuster tone")
            print("  i = voir les infos")
            print("  q = quitter")
            print("\nAppuyez sur Entree pour commencer...")
            input()

            self.running = True

            # Cree le stream audio
            with sd.Stream(device=(input_device, output_device),
                          samplerate=self.sample_rate,
                          blocksize=self.block_size,
                          channels=2,
                          callback=self.process_audio):

                print("\nACTIF - Jouez votre guitare!\n")

                while self.running:
                    command = input("> ").strip().lower()

                    if command == 'q':
                        self.running = False
                    elif command == 'd':
                        self.change_distortion()
                    elif command == 'g':
                        self.adjust_gain()
                    elif command == 'l':
                        self.adjust_level()
                    elif command == 't':
                        self.adjust_tone()
                    elif command == 'i':
                        self.show_info()

        except KeyboardInterrupt:
            print("\n\nArret...")
        except Exception as e:
            print(f"\nErreur: {e}")
            print("\nAssurez-vous que:")
            print("  1. Votre guitare est connectee a l'interface audio")
            print("  2. L'interface audio est reconnue par Windows")
            print("  3. Les pilotes sont installes (ASIO recommande)")

    def change_distortion(self):
        """Change le type de distortion"""
        print("\nTypes disponibles:")
        print("  1. overdrive (chaud et doux)")
        print("  2. fuzz (agressif et vintage)")
        print("  3. metal (moderne et agressif)")
        print("  4. clean (boost propre)")

        choice = input("Choix (1-4): ").strip()

        types = {"1": "overdrive", "2": "fuzz", "3": "metal", "4": "clean"}
        if choice in types:
            self.distortion_type = types[choice]
            print(f"Type change: {self.distortion_type}")

    def adjust_gain(self):
        """Ajuste le gain"""
        try:
            value = float(input(f"Gain actuel: {self.gain:.1f} | Nouveau (1.0-20.0): "))
            self.gain = np.clip(value, 1.0, 20.0)
            print(f"Gain: {self.gain:.1f}")
        except:
            print("Valeur invalide")

    def adjust_level(self):
        """Ajuste le niveau de sortie"""
        try:
            value = float(input(f"Level actuel: {self.level:.2f} | Nouveau (0.0-1.0): "))
            self.level = np.clip(value, 0.0, 1.0)
            print(f"Level: {self.level:.2f}")
        except:
            print("Valeur invalide")

    def adjust_tone(self):
        """Ajuste la tonalite"""
        try:
            value = float(input(f"Tone actuel: {self.tone:.2f} | Nouveau (0.0-1.0): "))
            self.tone = np.clip(value, 0.0, 1.0)
            print(f"Tone: {self.tone:.2f} (0=sombre, 1=brillant)")
        except:
            print("Valeur invalide")

    def show_info(self):
        """Affiche les parametres actuels"""
        print(f"\nParametres actuels:")
        print(f"  Type: {self.distortion_type}")
        print(f"  Gain: {self.gain:.1f}")
        print(f"  Level: {self.level:.2f}")
        print(f"  Tone: {self.tone:.2f}\n")


def main():
    """Point d'entree principal"""
    print("Initialisation de yoTuneToTune...")
    fx = GuitarFX()
    fx.start()


if __name__ == "__main__":
    main()
