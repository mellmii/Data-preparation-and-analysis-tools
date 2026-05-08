import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
import scipy.signal as signal
import tkinter as tk
from tkinter import messagebox

# Початкові налаштування та параметри

fs = 500  # Частота дискретизації
t = np.linspace(0, 10, fs * 10)  # Вектор часу 

INIT_AMP = 1.0
INIT_FREQ = 1.0
INIT_PHASE = 0.0
INIT_NOISE_MEAN = 0.0
INIT_NOISE_COV = 0.5
INIT_CUTOFF = 2.0  # Частота зрізу для фільтра

current_noise = None
prev_noise_mean = None
prev_noise_cov = None

# Основні функції
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global current_noise, prev_noise_mean, prev_noise_cov
    
    if current_noise is None or noise_mean != prev_noise_mean or noise_covariance != prev_noise_cov:
        current_noise = np.random.normal(noise_mean, np.sqrt(max(0, noise_covariance)), len(t))
        prev_noise_mean = noise_mean
        prev_noise_cov = noise_covariance

    clean_harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    if show_noise:
        return clean_harmonic + current_noise
    return clean_harmonic

def apply_filter(noisy_signal, cutoff_freq):
    nyquist = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyquist
    b, a = signal.butter(4, normalized_cutoff, btype='low', analog=False)
    filtered_signal = signal.filtfilt(b, a, noisy_signal)
    return filtered_signal

# Налаштування графічного інтерфейсу

fig, ax = plt.subplots(figsize=(12, 8))

# Кольори фону
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

plt.subplots_adjust(left=0.1, bottom=0.5) 
ax.set_title("Гармоніка з шумом та фільтрацією", color='white')
ax.set_xlabel("Час (t)", color='white')
ax.set_ylabel("Амплітуда (y)", color='white')

# Кольори осей та значень на чорному фоні
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

y_clean = harmonic_with_noise(INIT_AMP, INIT_FREQ, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_COV, show_noise=False)
y_noisy = harmonic_with_noise(INIT_AMP, INIT_FREQ, INIT_PHASE, INIT_NOISE_MEAN, INIT_NOISE_COV, show_noise=True)
y_filtered = apply_filter(y_noisy, INIT_CUTOFF)

# Кольори графіків
line_noisy, = ax.plot(t, y_noisy, label="Зашумлений сигнал", color='pink', alpha=0.7)
line_clean, = ax.plot(t, y_clean, label="Чиста гармоніка", color='grey', linestyle='--')
line_filtered, = ax.plot(t, y_filtered, label="Відфільтрований сигнал", color='yellow', linewidth=2)

legend = ax.legend(loc='upper right', facecolor='black', edgecolor='white')
for text in legend.get_texts():
    text.set_color('white')
    
ax.grid(True, color='gray', linestyle=':', alpha=0.5)

# Кольори слайдерів
slider_bg_color = 'white'     
slider_active_color = 'pink'  

ax_amp = plt.axes([0.15, 0.40, 0.65, 0.03], facecolor=slider_bg_color)
ax_freq = plt.axes([0.15, 0.35, 0.65, 0.03], facecolor=slider_bg_color)
ax_phase = plt.axes([0.15, 0.30, 0.65, 0.03], facecolor=slider_bg_color)
ax_nmean = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor=slider_bg_color)
ax_ncov = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=slider_bg_color)
ax_cutoff = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=slider_bg_color)

samp = Slider(ax_amp, 'Amplitude', 0.1, 5.0, valinit=INIT_AMP, color=slider_active_color)
sfreq = Slider(ax_freq, 'Frequency', 0.1, 10.0, valinit=INIT_FREQ, color=slider_active_color)
sphase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=INIT_PHASE, color=slider_active_color)
snmean = Slider(ax_nmean, 'Noise Mean', -2.0, 2.0, valinit=INIT_NOISE_MEAN, color=slider_active_color)
sncov = Slider(ax_ncov, 'Noise Covariance', 0.0, 5.0, valinit=INIT_NOISE_COV, color=slider_active_color)
scutoff = Slider(ax_cutoff, 'Filter Cutoff (Hz)', 0.1, 50.0, valinit=INIT_CUTOFF, color=slider_active_color)

# Роблю текст слайдерів білим, щоб його було видно на чорному фоні
for slider in [samp, sfreq, sphase, snmean, sncov, scutoff]:
    slider.label.set_color('white')
    slider.valtext.set_color('white')

# Чекбокси
ax_check = plt.axes([0.85, 0.25, 0.12, 0.15], facecolor='white')
labels = ['Show Noise', 'Show Filtered', 'Show Clean']
visibility = [True, True, True]
check = CheckButtons(ax_check, labels, visibility)

# Кнопка Reset
ax_reset = plt.axes([0.85, 0.16, 0.12, 0.05])
button_reset = Button(ax_reset, 'Reset', color='white', hovercolor='0.975')

# Кнопка Help (Інструкція)
ax_help = plt.axes([0.85, 0.09, 0.12, 0.05])
button_help = Button(ax_help, 'Help', color='lightblue', hovercolor='0.9')

# Логіка оновлення інтерфейсу

def update(val):
    show_noise = check.get_status()[0]
    show_filtered = check.get_status()[1]
    show_clean = check.get_status()[2]

    y_clean_current = harmonic_with_noise(samp.val, sfreq.val, sphase.val, snmean.val, sncov.val, show_noise=False)
    y_noisy_current = harmonic_with_noise(samp.val, sfreq.val, sphase.val, snmean.val, sncov.val, show_noise=True)
    y_filtered_current = apply_filter(y_noisy_current, scutoff.val)

    if show_noise:
        line_noisy.set_ydata(y_noisy_current)
        line_noisy.set_visible(True)
    else:
        line_noisy.set_visible(False)

    line_clean.set_ydata(y_clean_current)
    line_clean.set_visible(show_clean)
    line_filtered.set_ydata(y_filtered_current)
    line_filtered.set_visible(show_filtered)

    ax.relim()
    ax.autoscale_view(scalex=False, scaley=True)
    fig.canvas.draw_idle()

samp.on_changed(update)
sfreq.on_changed(update)
sphase.on_changed(update)
snmean.on_changed(update)
sncov.on_changed(update)
scutoff.on_changed(update)

def toggle_lines(label):
    update(None)
check.on_clicked(toggle_lines)

def reset(event):
    samp.reset()
    sfreq.reset()
    sphase.reset()
    snmean.reset()
    sncov.reset()
    scutoff.reset()
    for i, state in enumerate(check.get_status()):
        if not state:
            check.set_active(i)
button_reset.on_clicked(reset)

# Функція для виклику вікна інструкції 
def show_instructions(event):

    root = tk.Tk()
    root.withdraw() 
    
    instruction_text = (
        "ІНСТРУКЦІЯ КОРИСТУВАЧА:\n\n"
        "1. Повзунки 'Amplitude', 'Frequency', 'Phase' змінюють параметри "
        " гармоніки. Малюнок шуму при цьому не генерується наново.\n\n"
        "2. Повзунки 'Noise Mean' та 'Noise Covariance' змінюють шум "
        "(генерується новий масив).\n\n"
        "3. 'Filter Cutoff' керує частотою зрізу IIR-фільтра Баттерворта. "
        "Зменшуйте значення для більш гладкого графіка.\n\n"
        "4. Чекбокси дозволяють приховувати або показувати відповідні графіки(лінії).\n\n"
        "5. Кнопка 'Reset' повертає всі параметри до початкового стану."
    )
    
    # Виклик системного віконця
    messagebox.showinfo("Як користуватися програмою", instruction_text)
    root.destroy()

button_help.on_clicked(show_instructions)

plt.show()