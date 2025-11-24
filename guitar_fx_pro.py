#!/usr/bin/env python3
"""
yoTuneToTune PRO - Processeur d'effets guitare professionnel
Tous les effets des logiciels premium, interface premium!
"""

import numpy as np
import sounddevice as sd
from collections import deque

class GuitarFXPro:
    def __init__(self, sample_rate=44100, block_size=256):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.running = False

        # Parametres principaux
        self.gain = 5.0
        self.level = 0.7
        self.tone = 0.5
        self.distortion_type = "overdrive"

        # Effets additionnels
        self.delay_enabled = False
        self.delay_time = 0.3  # secondes
        self.delay_feedback = 0.4
        self.delay_mix = 0.3

        self.reverb_enabled = False
        self.reverb_size = 0.5
        self.reverb_mix = 0.3

        self.chorus_enabled = False
        self.chorus_rate = 2.0
        self.chorus_depth = 0.3

        self.compressor_enabled = True
        self.compressor_threshold = 0.6
        self.compressor_ratio = 4.0

        # EQ 3 bandes
        self.eq_low = 0.5
        self.eq_mid = 0.5
        self.eq_high = 0.5

        # Buffers pour effets
        max_delay_samples = int(1.0 * sample_rate)
        self.delay_buffer = deque([0.0] * max_delay_samples, maxlen=max_delay_samples)

        self.reverb_buffers = [deque([0.0] * int(0.03 * sample_rate), maxlen=int(0.03 * sample_rate)) for _ in range(4)]

        self.chorus_phase = 0.0

        # Filtre states
        self.filter_state = 0.0
        self.eq_low_state = 0.0
        self.eq_high_state = 0.0

    def overdrive(self, audio):
        """Overdrive - son chaud et doux"""
        x = audio * self.gain
        y = np.where(x > 0, 1 - np.exp(-x), -1 + np.exp(x))
        return y

    def fuzz(self, audio):
        """Fuzz - son agressif vintage"""
        x = audio * self.gain * 2
        y = np.clip(x, -0.7, 1.0)
        y = np.tanh(y * 2)
        return y

    def metal(self, audio):
        """Metal - distortion moderne"""
        x = audio * self.gain * 1.5
        y = np.tanh(x)
        y = np.tanh(y * 3)
        return y

    def blues(self, audio):
        """Blues - doux avec harmoniques"""
        x = audio * self.gain * 0.8
        y = np.tanh(x * 1.5)
        return y

    def crunch(self, audio):
        """Crunch - rock classique"""
        x = audio * self.gain * 1.2
        y = 2 * x / (1 + abs(x))
        return y

    def clean_boost(self, audio):
        """Clean boost"""
        return audio * self.gain * 0.3

    def apply_compressor(self, audio):
        """Compresseur dynamique"""
        if not self.compressor_enabled:
            return audio

        output = np.zeros_like(audio)
        for i, sample in enumerate(audio):
            level = abs(sample)
            if level > self.compressor_threshold:
                excess = level - self.compressor_threshold
                reduction = excess / self.compressor_ratio
                gain_reduction = (self.compressor_threshold + reduction) / level
                output[i] = sample * gain_reduction
            else:
                output[i] = sample
        return output

    def apply_eq(self, audio):
        """Equalizer 3 bandes"""
        # Low (bass)
        alpha_low = 0.1
        low_filtered = np.zeros_like(audio)
        for i, sample in enumerate(audio):
            self.eq_low_state = alpha_low * sample + (1 - alpha_low) * self.eq_low_state
            low_filtered[i] = self.eq_low_state

        # High (treble)
        alpha_high = 0.9
        high_filtered = np.zeros_like(audio)
        high_state = 0.0
        for i, sample in enumerate(audio):
            high_state = alpha_high * sample + (1 - alpha_high) * high_state
            high_filtered[i] = sample - high_state

        # Mid
        mid_filtered = audio - low_filtered - high_filtered

        # Mix avec les controles EQ
        eq_low_gain = (self.eq_low - 0.5) * 2 + 1
        eq_mid_gain = (self.eq_mid - 0.5) * 2 + 1
        eq_high_gain = (self.eq_high - 0.5) * 2 + 1

        return low_filtered * eq_low_gain + mid_filtered * eq_mid_gain + high_filtered * eq_high_gain

    def apply_delay(self, audio):
        """Delay/Echo"""
        if not self.delay_enabled:
            return audio

        output = np.zeros_like(audio)
        delay_samples = int(self.delay_time * self.sample_rate)

        for i, sample in enumerate(audio):
            delayed = self.delay_buffer[-delay_samples] if len(self.delay_buffer) >= delay_samples else 0.0
            output[i] = sample + delayed * self.delay_mix
            self.delay_buffer.append(sample + delayed * self.delay_feedback)

        return output

    def apply_reverb(self, audio):
        """Reverb simple"""
        if not self.reverb_enabled:
            return audio

        output = np.zeros_like(audio)

        for i, sample in enumerate(audio):
            wet = sample
            for buf in self.reverb_buffers:
                if len(buf) > 0:
                    wet += buf[0] * 0.3
                buf.append(wet * self.reverb_size)

            output[i] = sample * (1 - self.reverb_mix) + wet * self.reverb_mix

        return output

    def apply_chorus(self, audio):
        """Chorus"""
        if not self.chorus_enabled:
            return audio

        output = np.zeros_like(audio)

        for i, sample in enumerate(audio):
            # LFO pour modulation
            lfo = np.sin(self.chorus_phase) * self.chorus_depth
            self.chorus_phase += 2 * np.pi * self.chorus_rate / self.sample_rate

            # Simple chorus effect
            output[i] = sample * 0.7 + sample * 0.3 * (1 + lfo)

        return output

    def apply_tone_control(self, audio):
        """Filtre de tonalite"""
        alpha = self.tone
        output = np.zeros_like(audio)

        for i, sample in enumerate(audio):
            self.filter_state = alpha * sample + (1 - alpha) * self.filter_state
            output[i] = self.filter_state

        return output

    def process_audio(self, indata, outdata, frames, time, status):
        """Traitement audio principal"""
        if status:
            print(f"Status: {status}")

        # Input
        audio = indata[:, 0] if indata.shape[1] > 0 else indata

        # Distortion
        if self.distortion_type == "overdrive":
            processed = self.overdrive(audio)
        elif self.distortion_type == "fuzz":
            processed = self.fuzz(audio)
        elif self.distortion_type == "metal":
            processed = self.metal(audio)
        elif self.distortion_type == "blues":
            processed = self.blues(audio)
        elif self.distortion_type == "crunch":
            processed = self.crunch(audio)
        elif self.distortion_type == "clean":
            processed = self.clean_boost(audio)
        else:
            processed = audio

        # EQ
        processed = self.apply_eq(processed)

        # Tone
        processed = self.apply_tone_control(processed)

        # Compressor
        processed = self.apply_compressor(processed)

        # Modulation effects
        processed = self.apply_chorus(processed)

        # Time effects
        processed = self.apply_delay(processed)
        processed = self.apply_reverb(processed)

        # Master level
        processed = processed * self.level

        # Limiter final
        processed = np.clip(processed, -1.0, 1.0)

        # Output stereo
        outdata[:, 0] = processed
        if outdata.shape[1] > 1:
            outdata[:, 1] = processed

    def load_preset(self, preset_name):
        """Charge un preset"""
        presets = {
            "clean_jazz": {
                "distortion_type": "clean",
                "gain": 2.0,
                "level": 0.8,
                "tone": 0.7,
                "delay_enabled": False,
                "reverb_enabled": True,
                "reverb_mix": 0.2,
                "chorus_enabled": True,
                "chorus_depth": 0.2,
                "eq_low": 0.6,
                "eq_mid": 0.5,
                "eq_high": 0.6
            },
            "blues_classic": {
                "distortion_type": "blues",
                "gain": 6.0,
                "level": 0.7,
                "tone": 0.6,
                "delay_enabled": False,
                "reverb_enabled": True,
                "reverb_mix": 0.15,
                "chorus_enabled": False,
                "eq_low": 0.6,
                "eq_mid": 0.6,
                "eq_high": 0.5
            },
            "rock_classic": {
                "distortion_type": "crunch",
                "gain": 7.0,
                "level": 0.75,
                "tone": 0.6,
                "delay_enabled": True,
                "delay_time": 0.35,
                "delay_mix": 0.2,
                "reverb_enabled": True,
                "reverb_mix": 0.2,
                "eq_low": 0.5,
                "eq_mid": 0.6,
                "eq_high": 0.6
            },
            "rock_moderne": {
                "distortion_type": "overdrive",
                "gain": 8.5,
                "level": 0.7,
                "tone": 0.55,
                "delay_enabled": False,
                "reverb_enabled": True,
                "reverb_mix": 0.15,
                "chorus_enabled": False,
                "eq_low": 0.6,
                "eq_mid": 0.5,
                "eq_high": 0.6
            },
            "metal_moderne": {
                "distortion_type": "metal",
                "gain": 12.0,
                "level": 0.65,
                "tone": 0.45,
                "delay_enabled": False,
                "reverb_enabled": False,
                "chorus_enabled": False,
                "compressor_enabled": True,
                "eq_low": 0.7,
                "eq_mid": 0.4,
                "eq_high": 0.6
            },
            "metal_heavy": {
                "distortion_type": "metal",
                "gain": 15.0,
                "level": 0.6,
                "tone": 0.4,
                "delay_enabled": False,
                "reverb_enabled": False,
                "eq_low": 0.8,
                "eq_mid": 0.3,
                "eq_high": 0.7
            },
            "punk_rock": {
                "distortion_type": "fuzz",
                "gain": 10.0,
                "level": 0.75,
                "tone": 0.65,
                "delay_enabled": False,
                "reverb_enabled": False,
                "chorus_enabled": False,
                "eq_low": 0.5,
                "eq_mid": 0.7,
                "eq_high": 0.7
            },
            "psychedelic": {
                "distortion_type": "fuzz",
                "gain": 9.0,
                "level": 0.7,
                "tone": 0.6,
                "delay_enabled": True,
                "delay_time": 0.4,
                "delay_feedback": 0.5,
                "delay_mix": 0.35,
                "reverb_enabled": True,
                "reverb_mix": 0.3,
                "chorus_enabled": True,
                "chorus_depth": 0.4,
                "eq_low": 0.5,
                "eq_mid": 0.6,
                "eq_high": 0.6
            },
            "indie_rock": {
                "distortion_type": "crunch",
                "gain": 6.5,
                "level": 0.7,
                "tone": 0.65,
                "delay_enabled": True,
                "delay_time": 0.3,
                "delay_mix": 0.25,
                "reverb_enabled": True,
                "reverb_mix": 0.25,
                "chorus_enabled": True,
                "chorus_depth": 0.25,
                "eq_low": 0.5,
                "eq_mid": 0.6,
                "eq_high": 0.6
            },
            "grunge": {
                "distortion_type": "fuzz",
                "gain": 11.0,
                "level": 0.7,
                "tone": 0.5,
                "delay_enabled": False,
                "reverb_enabled": True,
                "reverb_mix": 0.2,
                "chorus_enabled": True,
                "chorus_depth": 0.3,
                "eq_low": 0.6,
                "eq_mid": 0.5,
                "eq_high": 0.5
            },
            "hard_rock": {
                "distortion_type": "overdrive",
                "gain": 9.0,
                "level": 0.75,
                "tone": 0.55,
                "delay_enabled": True,
                "delay_time": 0.25,
                "delay_mix": 0.15,
                "reverb_enabled": True,
                "reverb_mix": 0.15,
                "eq_low": 0.6,
                "eq_mid": 0.6,
                "eq_high": 0.6
            },
            "lead_solo": {
                "distortion_type": "overdrive",
                "gain": 7.5,
                "level": 0.8,
                "tone": 0.7,
                "delay_enabled": True,
                "delay_time": 0.35,
                "delay_feedback": 0.4,
                "delay_mix": 0.3,
                "reverb_enabled": True,
                "reverb_mix": 0.25,
                "chorus_enabled": False,
                "eq_low": 0.4,
                "eq_mid": 0.7,
                "eq_high": 0.7
            }
        }

        if preset_name in presets:
            preset = presets[preset_name]
            for key, value in preset.items():
                setattr(self, key, value)
            return True
        return False

    def get_all_presets(self):
        """Retourne la liste des presets"""
        return [
            "clean_jazz",
            "blues_classic",
            "rock_classic",
            "rock_moderne",
            "metal_moderne",
            "metal_heavy",
            "punk_rock",
            "psychedelic",
            "indie_rock",
            "grunge",
            "hard_rock",
            "lead_solo"
        ]
