"""Analyze ExactSample.csv from MU5735 FDR data and generate plots.

Usage (from repository root):
    python3 Investigation_Report/scripts/analyze.py

The script loads ExactSample.csv from the repository root and writes
PNG figures into Investigation_Report/figures/ next to this script.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CSV = os.path.join(REPO_ROOT, "ExactSample.csv")
OUT = os.path.join(HERE, "..", "figures")
OUT = os.path.abspath(OUT)
os.makedirs(OUT, exist_ok=True)

# Header line is at line 11 (1-based); units row and encoding row follow.
# Use pandas to read with skiprows for the metadata.
HEADER_ROW = 11  # 0-indexed line containing column names ("Time,...")

df = pd.read_csv(CSV, header=HEADER_ROW, skiprows=[HEADER_ROW + 1, HEADER_ROW + 2],
                 low_memory=False, na_values=[""])
print("rows:", len(df), "cols:", len(df.columns))

# Convert Time
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
t0 = df["Time"].min()
df["t"] = df["Time"] - t0  # seconds from start of sample

# Normalize relative time so that descent starts identifiable. The full
# sample is roughly 13 minutes; the upset begins near t≈730s (288930 abs).

NUM_COLS = [
    "Altitude Press", "Airspeed Comp", "Pitch Angle", "Roll Angle",
    "Eng1 N1", "Eng2 N1", "Eng1 TRA", "Eng2 TRA",
    "Ctrl Col Pos-L", "Ctrl Col Pos-R", "Ctrl Whl Pos-L", "Ctrl Whl Pos-R",
    "Rudder", "Rudder Ped Pos", "Elevator-L", "Elevator-R",
    "Aileron-L", "Aileron-R",
    "Accel Vert", "Accel Long", "Accel Lat",
    "Heading", "Ground Spd", "Eng1 Fuel Flow", "Eng2 Fuel Flow",
    "Hyd Oil Press - A", "Hyd Oil Press - B",
    "Selected Altitude FCC", "Altitude Radio-1",
    "Flap Handle Pos", "Eng1 EGT", "Eng2 EGT",
]
for c in NUM_COLS:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# helper: per-parameter cleaned series (drop NaN)
def series(col):
    s = df[["t", col]].dropna()
    return s["t"].values, s[col].values

def plot_one(col, ylabel, title, fname, color="tab:blue", ylim=None):
    if col not in df.columns:
        print("skip", col); return
    t, v = series(col)
    if len(t) == 0:
        print("empty", col); return
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(t, v, color=color, lw=0.8)
    ax.set_xlabel("Time from start of sample (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    if ylim:
        ax.set_ylim(*ylim)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=120)
    plt.close(fig)
    print("wrote", fname)

# 1. Altitude
plot_one("Altitude Press", "Pressure Altitude (ft)",
         "MU5735 Pressure Altitude — Final ~13 minutes",
         "01_altitude.png", color="tab:blue")

# 2. Airspeed
plot_one("Airspeed Comp", "Computed Airspeed (kts)",
         "MU5735 Computed Airspeed",
         "02_airspeed.png", color="tab:red")

# 3. Pitch
plot_one("Pitch Angle", "Pitch Angle (deg)",
         "MU5735 Pitch Angle",
         "03_pitch.png", color="tab:green")

# 4. Roll
plot_one("Roll Angle", "Roll Angle (deg)",
         "MU5735 Roll (Bank) Angle",
         "04_roll.png", color="tab:purple")

# 5. Engine N1 (both engines on same plot)
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Eng1 N1", "tab:blue", "Eng1 N1"),
                          ("Eng2 N1", "tab:orange", "Eng2 N1")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("N1 (% RPM)")
ax.set_title("MU5735 Engine N1 (both engines)")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "05_engine_n1.png"), dpi=120)
plt.close(fig)

# 6. Throttle TRA
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Eng1 TRA", "tab:blue", "Eng1 TRA"),
                          ("Eng2 TRA", "tab:orange", "Eng2 TRA")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Throttle Resolver Angle (deg)")
ax.set_title("MU5735 Throttle Lever Position (TRA)")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "06_throttle.png"), dpi=120)
plt.close(fig)

# 7. Control column position
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Ctrl Col Pos-L", "tab:blue", "Capt Col"),
                          ("Ctrl Col Pos-R", "tab:orange", "F/O Col")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Control Column Position (deg)")
ax.set_title("MU5735 Control Column Positions")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "07_ctrl_col.png"), dpi=120)
plt.close(fig)

# 8. Elevator
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Elevator-L", "tab:blue", "Elevator-L"),
                          ("Elevator-R", "tab:orange", "Elevator-R")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Elevator Surface Position (deg)")
ax.set_title("MU5735 Elevator Surface Positions")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "08_elevator.png"), dpi=120)
plt.close(fig)

# 9. Vertical / longitudinal accelerations
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Accel Vert", "tab:blue", "Vertical (g)"),
                          ("Accel Long", "tab:green", "Longitudinal (g)"),
                          ("Accel Lat", "tab:red", "Lateral (g)")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.6, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Acceleration (g)")
ax.set_title("MU5735 Body-axis Accelerations")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "09_accel.png"), dpi=120)
plt.close(fig)

# 10. Hydraulics
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Hyd Oil Press - A", "tab:blue", "System A"),
                          ("Hyd Oil Press - B", "tab:orange", "System B")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Hydraulic Pressure (psi)")
ax.set_title("MU5735 Hydraulic System Pressures")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "10_hydraulics.png"), dpi=120)
plt.close(fig)

# 11. Rudder & rudder pedal
fig, ax = plt.subplots(figsize=(11, 4))
for col, color, label in [("Rudder", "tab:blue", "Rudder Surface"),
                          ("Rudder Ped Pos", "tab:orange", "Rudder Pedal")]:
    if col in df.columns:
        t, v = series(col)
        ax.plot(t, v, lw=0.8, color=color, label=label)
ax.set_xlabel("Time from start of sample (s)")
ax.set_ylabel("Position (deg)")
ax.set_title("MU5735 Rudder Surface and Pedal Position")
ax.grid(True, alpha=0.3); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(OUT, "11_rudder.png"), dpi=120)
plt.close(fig)

# 12. Combined dashboard around upset event (last 60s)
t_end = df["t"].max()
t_start_zoom = t_end - 90  # last 90s
fig, axes = plt.subplots(4, 1, figsize=(11, 10), sharex=True)
plot_pairs = [
    ("Altitude Press", "Altitude (ft)", "tab:blue"),
    ("Airspeed Comp", "Airspeed (kts)", "tab:red"),
    ("Pitch Angle", "Pitch (deg)", "tab:green"),
    ("Eng1 N1", "Eng N1 (%)", "tab:blue"),
]
for ax, (col, ylabel, color) in zip(axes, plot_pairs):
    if col in df.columns:
        t, v = series(col)
        m = t >= t_start_zoom
        ax.plot(t[m], v[m], color=color, lw=0.9, label=col)
        if col == "Eng1 N1" and "Eng2 N1" in df.columns:
            t2, v2 = series("Eng2 N1")
            m2 = t2 >= t_start_zoom
            ax.plot(t2[m2], v2[m2], color="tab:orange", lw=0.9, label="Eng2 N1")
            ax.legend()
        ax.set_ylabel(ylabel); ax.grid(True, alpha=0.3)
axes[-1].set_xlabel("Time from start of sample (s)")
fig.suptitle("MU5735 Final ~90 seconds — Upset & Descent", y=1.0)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "12_final90s_dashboard.png"), dpi=120)
plt.close(fig)

# Print key numerical findings
def stat(col):
    if col not in df.columns: return None
    t, v = series(col)
    return t, v

print("\n=== KEY FINDINGS ===")
if "Altitude Press" in df.columns:
    t, v = series("Altitude Press")
    print(f"Altitude: max={v.max():.0f} ft at t={t[v.argmax()]:.1f}s, "
          f"min={v.min():.0f} ft at t={t[v.argmin()]:.1f}s")
if "Airspeed Comp" in df.columns:
    t, v = series("Airspeed Comp")
    print(f"Airspeed: max={v.max():.0f} kt at t={t[v.argmax()]:.1f}s, "
          f"final={v[-1]:.0f} kt")
if "Pitch Angle" in df.columns:
    t, v = series("Pitch Angle")
    print(f"Pitch: max={v.max():.1f}°, min={v.min():.1f}° at t={t[v.argmin()]:.1f}s")
if "Roll Angle" in df.columns:
    t, v = series("Roll Angle")
    print(f"Roll: max={v.max():.1f}°, min={v.min():.1f}°, "
          f"|max|={np.abs(v).max():.1f}°")
if "Eng1 N1" in df.columns:
    t, v = series("Eng1 N1")
    print(f"Eng1 N1: cruise≈{np.median(v[t < 600]):.1f}%, final={v[-1]:.1f}%")
if "Eng2 N1" in df.columns:
    t, v = series("Eng2 N1")
    print(f"Eng2 N1: cruise≈{np.median(v[t < 600]):.1f}%, final={v[-1]:.1f}%")
if "Accel Vert" in df.columns:
    t, v = series("Accel Vert")
    print(f"Vertical g: min={v.min():.2f}, max={v.max():.2f}")
print(f"Sample duration: {df['t'].max():.1f} s ({df['t'].max()/60:.2f} min)")
print(f"Absolute time range: {df['Time'].min():.1f} – {df['Time'].max():.1f} s")
