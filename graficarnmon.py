import pandas as pd
import matplotlib.pyplot as plt
import re

# Ruta al archivo .nmon
nmon_path = "x86_250725_1921.nmon"

# Leer todas las líneas
with open(nmon_path, "r") as f:
    nmon_lines = f.readlines()

# Extraer secciones CPU_ALL, MEM y hilos CPU individuales (CPU001, CPU002, ...)
cpu_all_data = []
mem_data = []
cpu_cores_data = {}  # Diccionario {CPU_ID: lista de (Time, %User)}

for line in nmon_lines:
    if line.startswith("CPU_ALL,T"):
        parts = line.strip().split(",")
        timestamp = parts[1]
        user, sys, wait = map(float, parts[2:5])
        cpu_all_data.append((timestamp, user, sys, wait))
    elif line.startswith("MEM,T"):
        parts = line.strip().split(",")
        timestamp = parts[1]
        memtotal = float(parts[2])
        memfree = float(parts[6])
        cached = float(parts[11])
        buffers = float(parts[14])
        mem_data.append((timestamp, memtotal, memfree, cached, buffers))
    elif re.match(r"CPU\d{3},T", line):
        parts = line.strip().split(",")
        cpu_id = parts[0]  # ejemplo: CPU001
        timestamp = parts[1]
        try:
            user = float(parts[2])
        except ValueError:
            continue  # salta si hay datos inválidos
        if cpu_id not in cpu_cores_data:
            cpu_cores_data[cpu_id] = []
        cpu_cores_data[cpu_id].append((timestamp, user))

# Convertir a DataFrame
cpu_df = pd.DataFrame(cpu_all_data, columns=["Time", "%User", "%System", "%IOWait"])
mem_df = pd.DataFrame(mem_data, columns=["Time", "Total", "Free", "Cached", "Buffers"])

# Procesar campo Time (quitar T y ordenar)
cpu_df["Time"] = cpu_df["Time"].str.extract(r"T(\d+)").astype(int)
mem_df["Time"] = mem_df["Time"].str.extract(r"T(\d+)").astype(int)
cpu_df.sort_values("Time", inplace=True)
mem_df.sort_values("Time", inplace=True)

# Calcular uso de memoria en porcentaje
mem_df["Used_MB"] = mem_df["Total"] - mem_df["Free"] - mem_df["Cached"] - mem_df["Buffers"]
mem_df["Used_%"] = (mem_df["Used_MB"] / mem_df["Total"]) * 100

# Graficar uso de CPU (total)
plt.figure(figsize=(14, 5))
plt.plot(cpu_df["Time"], cpu_df["%User"], label="%User", color="blue")
plt.plot(cpu_df["Time"], cpu_df["%System"], label="%System", color="green")
plt.plot(cpu_df["Time"], cpu_df["%IOWait"], label="%IOWait", color="red")
plt.xlabel("Snapshot")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Graficar uso de memoria
plt.figure(figsize=(14, 5))
plt.plot(mem_df["Time"], mem_df["Used_%"], label="Memory Used %", color="purple")
plt.xlabel("Snapshot")
plt.ylabel("Memory Usage (%)")
plt.title("Memory Usage Over Time")
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()
plt.show()

# Graficar uso de hilos (%User por CPU individual)
plt.figure(figsize=(16, 6))
for cpu_id, data in cpu_cores_data.items():
    core_df = pd.DataFrame(data, columns=["Time", "%User"])
    core_df["Time"] = core_df["Time"].str.extract(r"T(\d+)").astype(int)
    core_df.sort_values("Time", inplace=True)
    plt.plot(core_df["Time"], core_df["%User"], label=cpu_id, alpha=0.6)

plt.xlabel("Snapshot")
plt.ylabel("CPU %User por hilo")
plt.title("Uso de CPU por hilo individual")
plt.legend(loc='upper right', ncol=4, fontsize="small")
plt.grid(True)
plt.tight_layout()
plt.show()
