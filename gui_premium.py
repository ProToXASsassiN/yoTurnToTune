#!/usr/bin/env python3
"""
yoTuneToTune PRO - Interface graphique premium
Design professionnel pour guitaristes exigeants
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sounddevice as sd
import threading
from guitar_fx_pro import GuitarFXPro

class PremiumGuitarGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("yoTuneToTune PRO - Studio d'Effets Guitare")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a1a")

        # Couleurs du theme premium
        self.bg_dark = "#1a1a1a"
        self.bg_medium = "#2a2a2a"
        self.bg_light = "#3a3a3a"
        self.accent_orange = "#ff6b35"
        self.accent_red = "#e63946"
        self.text_white = "#f1f1f1"
        self.text_gray = "#b0b0b0"

        # Moteur audio
        self.fx = GuitarFXPro()
        self.stream = None
        self.is_playing = False

        # Variables tkinter
        self.setup_variables()

        # Interface
        self.create_interface()

        # Style
        self.configure_styles()

    def setup_variables(self):
        """Initialise les variables tkinter"""
        self.var_gain = tk.DoubleVar(value=self.fx.gain)
        self.var_level = tk.DoubleVar(value=self.fx.level)
        self.var_tone = tk.DoubleVar(value=self.fx.tone)

        self.var_delay_mix = tk.DoubleVar(value=self.fx.delay_mix)
        self.var_delay_time = tk.DoubleVar(value=self.fx.delay_time)
        self.var_delay_feedback = tk.DoubleVar(value=self.fx.delay_feedback)

        self.var_reverb_mix = tk.DoubleVar(value=self.fx.reverb_mix)
        self.var_reverb_size = tk.DoubleVar(value=self.fx.reverb_size)

        self.var_chorus_depth = tk.DoubleVar(value=self.fx.chorus_depth)
        self.var_chorus_rate = tk.DoubleVar(value=self.fx.chorus_rate)

        self.var_eq_low = tk.DoubleVar(value=self.fx.eq_low)
        self.var_eq_mid = tk.DoubleVar(value=self.fx.eq_mid)
        self.var_eq_high = tk.DoubleVar(value=self.fx.eq_high)

        self.var_delay_enabled = tk.BooleanVar(value=self.fx.delay_enabled)
        self.var_reverb_enabled = tk.BooleanVar(value=self.fx.reverb_enabled)
        self.var_chorus_enabled = tk.BooleanVar(value=self.fx.chorus_enabled)
        self.var_compressor_enabled = tk.BooleanVar(value=self.fx.compressor_enabled)

    def configure_styles(self):
        """Configure les styles personnalises"""
        style = ttk.Style()
        style.theme_use('clam')

        # Style pour les sliders
        style.configure("Horizontal.TScale",
                       background=self.bg_medium,
                       troughcolor=self.bg_light,
                       bordercolor=self.bg_dark,
                       darkcolor=self.bg_dark,
                       lightcolor=self.bg_light)

    def create_interface(self):
        """Cree l'interface principale"""
        # Header
        self.create_header()

        # Container principal
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Colonne gauche - Controles principaux
        left_panel = tk.Frame(main_container, bg=self.bg_dark)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.create_amp_section(left_panel)
        self.create_eq_section(left_panel)
        self.create_effects_section(left_panel)

        # Colonne droite - Presets
        right_panel = tk.Frame(main_container, bg=self.bg_dark)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        self.create_presets_section(right_panel)
        self.create_control_section(right_panel)

    def create_header(self):
        """Cree le header"""
        header = tk.Frame(self.root, bg=self.bg_medium, height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Logo/Titre
        title = tk.Label(header,
                        text="yoTuneToTune",
                        font=("Helvetica", 32, "bold"),
                        bg=self.bg_medium,
                        fg=self.accent_orange)
        title.pack(side=tk.LEFT, padx=30, pady=15)

        subtitle = tk.Label(header,
                           text="PRO STUDIO EDITION",
                           font=("Helvetica", 10, "bold"),
                           bg=self.bg_medium,
                           fg=self.text_gray)
        subtitle.pack(side=tk.LEFT, padx=(0, 30), pady=15)

        # Status indicator
        self.status_label = tk.Label(header,
                                     text="● OFFLINE",
                                     font=("Helvetica", 12, "bold"),
                                     bg=self.bg_medium,
                                     fg=self.text_gray)
        self.status_label.pack(side=tk.RIGHT, padx=30, pady=15)

    def create_amp_section(self, parent):
        """Section amplificateur/distortion"""
        frame = self.create_section_frame(parent, "AMPLIFICATEUR")

        # Type de distortion
        type_frame = tk.Frame(frame, bg=self.bg_medium)
        type_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(type_frame,
                text="Type",
                font=("Helvetica", 10, "bold"),
                bg=self.bg_medium,
                fg=self.text_white).pack(anchor=tk.W)

        types = ["clean", "blues", "crunch", "overdrive", "fuzz", "metal"]
        type_buttons_frame = tk.Frame(type_frame, bg=self.bg_medium)
        type_buttons_frame.pack(fill=tk.X, pady=5)

        self.type_buttons = {}
        for i, dtype in enumerate(types):
            btn = tk.Button(type_buttons_frame,
                           text=dtype.upper(),
                           font=("Helvetica", 9, "bold"),
                           bg=self.bg_light,
                           fg=self.text_white,
                           activebackground=self.accent_orange,
                           activeforeground=self.text_white,
                           relief=tk.FLAT,
                           padx=10,
                           pady=8,
                           command=lambda t=dtype: self.set_distortion_type(t))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
            self.type_buttons[dtype] = btn

        self.set_distortion_type("overdrive")

        # Controles principaux
        self.create_slider(frame, "GAIN", self.var_gain, 1.0, 20.0, self.on_gain_change)
        self.create_slider(frame, "LEVEL", self.var_level, 0.0, 1.0, self.on_level_change)
        self.create_slider(frame, "TONE", self.var_tone, 0.0, 1.0, self.on_tone_change)

    def create_eq_section(self, parent):
        """Section equalizer"""
        frame = self.create_section_frame(parent, "EQUALIZER 3 BANDES")

        self.create_slider(frame, "BASS", self.var_eq_low, 0.0, 1.0, self.on_eq_low_change)
        self.create_slider(frame, "MID", self.var_eq_mid, 0.0, 1.0, self.on_eq_mid_change)
        self.create_slider(frame, "TREBLE", self.var_eq_high, 0.0, 1.0, self.on_eq_high_change)

    def create_effects_section(self, parent):
        """Section effets"""
        # Delay
        delay_frame = self.create_section_frame(parent, "DELAY")

        check_frame = tk.Frame(delay_frame, bg=self.bg_medium)
        check_frame.pack(fill=tk.X, padx=15, pady=(10, 5))

        cb = tk.Checkbutton(check_frame,
                           text="Activer",
                           variable=self.var_delay_enabled,
                           command=self.on_delay_toggle,
                           bg=self.bg_medium,
                           fg=self.text_white,
                           selectcolor=self.bg_dark,
                           activebackground=self.bg_medium,
                           activeforeground=self.accent_orange,
                           font=("Helvetica", 10, "bold"))
        cb.pack(anchor=tk.W)

        self.create_slider(delay_frame, "MIX", self.var_delay_mix, 0.0, 1.0, self.on_delay_mix_change)
        self.create_slider(delay_frame, "TIME", self.var_delay_time, 0.1, 1.0, self.on_delay_time_change)
        self.create_slider(delay_frame, "FEEDBACK", self.var_delay_feedback, 0.0, 0.8, self.on_delay_feedback_change)

        # Reverb
        reverb_frame = self.create_section_frame(parent, "REVERB")

        check_frame = tk.Frame(reverb_frame, bg=self.bg_medium)
        check_frame.pack(fill=tk.X, padx=15, pady=(10, 5))

        cb = tk.Checkbutton(check_frame,
                           text="Activer",
                           variable=self.var_reverb_enabled,
                           command=self.on_reverb_toggle,
                           bg=self.bg_medium,
                           fg=self.text_white,
                           selectcolor=self.bg_dark,
                           activebackground=self.bg_medium,
                           activeforeground=self.accent_orange,
                           font=("Helvetica", 10, "bold"))
        cb.pack(anchor=tk.W)

        self.create_slider(reverb_frame, "MIX", self.var_reverb_mix, 0.0, 1.0, self.on_reverb_mix_change)
        self.create_slider(reverb_frame, "SIZE", self.var_reverb_size, 0.0, 1.0, self.on_reverb_size_change)

        # Chorus
        chorus_frame = self.create_section_frame(parent, "CHORUS")

        check_frame = tk.Frame(chorus_frame, bg=self.bg_medium)
        check_frame.pack(fill=tk.X, padx=15, pady=(10, 5))

        cb = tk.Checkbutton(check_frame,
                           text="Activer",
                           variable=self.var_chorus_enabled,
                           command=self.on_chorus_toggle,
                           bg=self.bg_medium,
                           fg=self.text_white,
                           selectcolor=self.bg_dark,
                           activebackground=self.bg_medium,
                           activeforeground=self.accent_orange,
                           font=("Helvetica", 10, "bold"))
        cb.pack(anchor=tk.W)

        self.create_slider(chorus_frame, "DEPTH", self.var_chorus_depth, 0.0, 1.0, self.on_chorus_depth_change)
        self.create_slider(chorus_frame, "RATE", self.var_chorus_rate, 0.1, 5.0, self.on_chorus_rate_change)

        # Compressor
        comp_frame = self.create_section_frame(parent, "COMPRESSOR")

        check_frame = tk.Frame(comp_frame, bg=self.bg_medium)
        check_frame.pack(fill=tk.X, padx=15, pady=10)

        cb = tk.Checkbutton(check_frame,
                           text="Activer",
                           variable=self.var_compressor_enabled,
                           command=self.on_compressor_toggle,
                           bg=self.bg_medium,
                           fg=self.text_white,
                           selectcolor=self.bg_dark,
                           activebackground=self.bg_medium,
                           activeforeground=self.accent_orange,
                           font=("Helvetica", 10, "bold"))
        cb.pack(anchor=tk.W)

    def create_presets_section(self, parent):
        """Section presets"""
        frame = self.create_section_frame(parent, "PRESETS")

        presets_data = [
            ("CLEAN JAZZ", "clean_jazz"),
            ("BLUES CLASSIC", "blues_classic"),
            ("ROCK CLASSIC", "rock_classic"),
            ("ROCK MODERNE", "rock_moderne"),
            ("METAL MODERNE", "metal_moderne"),
            ("METAL HEAVY", "metal_heavy"),
            ("PUNK ROCK", "punk_rock"),
            ("PSYCHEDELIC", "psychedelic"),
            ("INDIE ROCK", "indie_rock"),
            ("GRUNGE", "grunge"),
            ("HARD ROCK", "hard_rock"),
            ("LEAD SOLO", "lead_solo"),
        ]

        for display_name, preset_name in presets_data:
            btn = tk.Button(frame,
                           text=display_name,
                           font=("Helvetica", 10, "bold"),
                           bg=self.bg_light,
                           fg=self.text_white,
                           activebackground=self.accent_red,
                           activeforeground=self.text_white,
                           relief=tk.FLAT,
                           padx=20,
                           pady=12,
                           command=lambda p=preset_name: self.load_preset(p))
            btn.pack(fill=tk.X, padx=15, pady=3)

    def create_control_section(self, parent):
        """Section controles audio"""
        frame = self.create_section_frame(parent, "CONTROLE AUDIO")

        # Liste des peripheriques
        devices_btn = tk.Button(frame,
                               text="VOIR LES PERIPHERIQUES",
                               font=("Helvetica", 10, "bold"),
                               bg=self.bg_light,
                               fg=self.text_white,
                               activebackground=self.accent_orange,
                               activeforeground=self.text_white,
                               relief=tk.FLAT,
                               padx=20,
                               pady=12,
                               command=self.show_devices)
        devices_btn.pack(fill=tk.X, padx=15, pady=(10, 5))

        # Input device
        input_frame = tk.Frame(frame, bg=self.bg_medium)
        input_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(input_frame,
                text="Device IN:",
                font=("Helvetica", 9),
                bg=self.bg_medium,
                fg=self.text_gray).pack(anchor=tk.W)

        self.input_device_entry = tk.Entry(input_frame,
                                           font=("Helvetica", 10),
                                           bg=self.bg_light,
                                           fg=self.text_white,
                                           insertbackground=self.text_white,
                                           relief=tk.FLAT)
        self.input_device_entry.pack(fill=tk.X, pady=2, ipady=5)

        # Output device
        output_frame = tk.Frame(frame, bg=self.bg_medium)
        output_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(output_frame,
                text="Device OUT:",
                font=("Helvetica", 9),
                bg=self.bg_medium,
                fg=self.text_gray).pack(anchor=tk.W)

        self.output_device_entry = tk.Entry(output_frame,
                                            font=("Helvetica", 10),
                                            bg=self.bg_light,
                                            fg=self.text_white,
                                            insertbackground=self.text_white,
                                            relief=tk.FLAT)
        self.output_device_entry.pack(fill=tk.X, pady=2, ipady=5)

        # Bouton Start/Stop
        self.start_button = tk.Button(frame,
                                      text="▶ START",
                                      font=("Helvetica", 14, "bold"),
                                      bg=self.accent_orange,
                                      fg=self.text_white,
                                      activebackground=self.accent_red,
                                      activeforeground=self.text_white,
                                      relief=tk.FLAT,
                                      padx=20,
                                      pady=15,
                                      command=self.toggle_audio)
        self.start_button.pack(fill=tk.X, padx=15, pady=(15, 10))

    def create_section_frame(self, parent, title):
        """Cree un cadre de section"""
        container = tk.Frame(parent, bg=self.bg_dark)
        container.pack(fill=tk.BOTH, padx=0, pady=(0, 15))

        # Titre
        title_frame = tk.Frame(container, bg=self.bg_light, height=35)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame,
                text=title,
                font=("Helvetica", 11, "bold"),
                bg=self.bg_light,
                fg=self.accent_orange).pack(side=tk.LEFT, padx=15, pady=8)

        # Contenu
        content = tk.Frame(container, bg=self.bg_medium)
        content.pack(fill=tk.BOTH, expand=True)

        return content

    def create_slider(self, parent, label, variable, min_val, max_val, command):
        """Cree un slider personnalise"""
        container = tk.Frame(parent, bg=self.bg_medium)
        container.pack(fill=tk.X, padx=15, pady=5)

        # Label et valeur
        label_frame = tk.Frame(container, bg=self.bg_medium)
        label_frame.pack(fill=tk.X)

        tk.Label(label_frame,
                text=label,
                font=("Helvetica", 9, "bold"),
                bg=self.bg_medium,
                fg=self.text_white).pack(side=tk.LEFT)

        value_label = tk.Label(label_frame,
                              text=f"{variable.get():.2f}",
                              font=("Helvetica", 9),
                              bg=self.bg_medium,
                              fg=self.accent_orange)
        value_label.pack(side=tk.RIGHT)

        # Slider
        slider = ttk.Scale(container,
                          from_=min_val,
                          to=max_val,
                          orient=tk.HORIZONTAL,
                          variable=variable,
                          command=lambda v: self.update_slider_value(value_label, variable, command))
        slider.pack(fill=tk.X, pady=(2, 0))

        return slider

    def update_slider_value(self, label, variable, callback):
        """Met a jour la valeur affichee du slider"""
        label.config(text=f"{variable.get():.2f}")
        if callback:
            callback()

    def set_distortion_type(self, dtype):
        """Change le type de distortion"""
        self.fx.distortion_type = dtype

        # Met a jour l'apparence des boutons
        for name, btn in self.type_buttons.items():
            if name == dtype:
                btn.config(bg=self.accent_orange, fg=self.text_white)
            else:
                btn.config(bg=self.bg_light, fg=self.text_white)

    def load_preset(self, preset_name):
        """Charge un preset"""
        if self.fx.load_preset(preset_name):
            # Met a jour tous les controles
            self.var_gain.set(self.fx.gain)
            self.var_level.set(self.fx.level)
            self.var_tone.set(self.fx.tone)
            self.var_eq_low.set(self.fx.eq_low)
            self.var_eq_mid.set(self.fx.eq_mid)
            self.var_eq_high.set(self.fx.eq_high)
            self.var_delay_enabled.set(self.fx.delay_enabled)
            self.var_delay_mix.set(self.fx.delay_mix)
            self.var_delay_time.set(self.fx.delay_time)
            self.var_delay_feedback.set(self.fx.delay_feedback)
            self.var_reverb_enabled.set(self.fx.reverb_enabled)
            self.var_reverb_mix.set(self.fx.reverb_mix)
            self.var_reverb_size.set(self.fx.reverb_size)
            self.var_chorus_enabled.set(self.fx.chorus_enabled)
            self.var_chorus_depth.set(self.fx.chorus_depth)
            self.var_chorus_rate.set(self.fx.chorus_rate)
            self.var_compressor_enabled.set(self.fx.compressor_enabled)

            self.set_distortion_type(self.fx.distortion_type)

            messagebox.showinfo("Preset", f"Preset '{preset_name}' charge!")

    def show_devices(self):
        """Affiche les peripheriques audio"""
        devices_window = tk.Toplevel(self.root)
        devices_window.title("Peripheriques Audio")
        devices_window.geometry("600x400")
        devices_window.configure(bg=self.bg_dark)

        text = tk.Text(devices_window,
                      bg=self.bg_medium,
                      fg=self.text_white,
                      font=("Courier", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        devices_info = str(sd.query_devices())
        text.insert("1.0", devices_info)
        text.config(state=tk.DISABLED)

    def toggle_audio(self):
        """Demarre/arrete le traitement audio"""
        if not self.is_playing:
            self.start_audio()
        else:
            self.stop_audio()

    def start_audio(self):
        """Demarre le traitement audio"""
        try:
            input_device = self.input_device_entry.get().strip()
            output_device = self.output_device_entry.get().strip()

            input_device = int(input_device) if input_device else None
            output_device = int(output_device) if output_device else None

            self.stream = sd.Stream(
                device=(input_device, output_device),
                samplerate=self.fx.sample_rate,
                blocksize=self.fx.block_size,
                channels=2,
                callback=self.fx.process_audio
            )
            self.stream.start()

            self.is_playing = True
            self.start_button.config(text="■ STOP", bg=self.accent_red)
            self.status_label.config(text="● LIVE", fg=self.accent_orange)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de demarrer:\n{e}")

    def stop_audio(self):
        """Arrete le traitement audio"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.is_playing = False
        self.start_button.config(text="▶ START", bg=self.accent_orange)
        self.status_label.config(text="● OFFLINE", fg=self.text_gray)

    # Callbacks pour les controles
    def on_gain_change(self):
        self.fx.gain = self.var_gain.get()

    def on_level_change(self):
        self.fx.level = self.var_level.get()

    def on_tone_change(self):
        self.fx.tone = self.var_tone.get()

    def on_eq_low_change(self):
        self.fx.eq_low = self.var_eq_low.get()

    def on_eq_mid_change(self):
        self.fx.eq_mid = self.var_eq_mid.get()

    def on_eq_high_change(self):
        self.fx.eq_high = self.var_eq_high.get()

    def on_delay_toggle(self):
        self.fx.delay_enabled = self.var_delay_enabled.get()

    def on_delay_mix_change(self):
        self.fx.delay_mix = self.var_delay_mix.get()

    def on_delay_time_change(self):
        self.fx.delay_time = self.var_delay_time.get()

    def on_delay_feedback_change(self):
        self.fx.delay_feedback = self.var_delay_feedback.get()

    def on_reverb_toggle(self):
        self.fx.reverb_enabled = self.var_reverb_enabled.get()

    def on_reverb_mix_change(self):
        self.fx.reverb_mix = self.var_reverb_mix.get()

    def on_reverb_size_change(self):
        self.fx.reverb_size = self.var_reverb_size.get()

    def on_chorus_toggle(self):
        self.fx.chorus_enabled = self.var_chorus_enabled.get()

    def on_chorus_depth_change(self):
        self.fx.chorus_depth = self.var_chorus_depth.get()

    def on_chorus_rate_change(self):
        self.fx.chorus_rate = self.var_chorus_rate.get()

    def on_compressor_toggle(self):
        self.fx.compressor_enabled = self.var_compressor_enabled.get()

    def run(self):
        """Lance l'interface"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        """Fermeture de l'application"""
        self.stop_audio()
        self.root.destroy()


def main():
    """Point d'entree"""
    app = PremiumGuitarGUI()
    app.run()


if __name__ == "__main__":
    main()
