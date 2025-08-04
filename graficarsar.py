import pandas as pd
import matplotlib.pyplot as plt

# Archivos CSV
cpu_file = "cpupowersmt8.csv"
mem_file = "memoriapowersmt8.csv"
#cpu_file = "cpux86hp.csv"
#mem_file = "memoriax86hp.csv"

# Total de memoria física (en MB) detectada con free -m
mem_total_MB = 31881

# ============ CPU =============
cpu_df = pd.read_csv(cpu_file)
cpu_df = cpu_df.drop(columns=cpu_df.columns[:2])  # quitar fecha y hora

# Seleccionar columnas con porcentaje y excluir %nice, %steal, %idle
exclude_cpu = ["%nice", "%steal", "%idle"]
percent_cols = [col for col in cpu_df.columns if '%' in col and col not in exclude_cpu]
cpu_data = cpu_df[percent_cols].astype(float)

# Agrupar cada 3 filas (iteraciones)
cpu_grouped = cpu_data.groupby(cpu_data.index // 3).mean()

# Graficar CPU
plt.figure(figsize=(14, 6))
bottom = None
for col in percent_cols:
    plt.bar(range(len(cpu_grouped)), cpu_grouped[col], bottom=bottom, label=col)
    bottom = cpu_grouped[col] if bottom is None else bottom + cpu_grouped[col]

plt.xlabel("Grupo de Iteraciones (cada 3)")
plt.ylabel("Uso de CPU (%)")
plt.title("Uso de CPU apilado por iteración (promedio cada 3)")
plt.legend()
plt.tight_layout()
plt.grid(axis="y")
plt.show()

# ============ MEMORIA =============
mem_df = pd.read_csv(mem_file)
mem_df = mem_df.drop(columns=mem_df.columns[:2])  # quitar fecha y hora

# Convertir columnas clave a MB
mem_df["kbmemused_MB"] = mem_df["kbmemused"].astype(float) / 1024
mem_df["kbbuffers_MB"] = mem_df["kbbuffers"].astype(float) / 1024
mem_df["kbcached_MB"] = mem_df["kbcached"].astype(float) / 1024

# Calcular memoria usada efectiva: RAM + buffers + cache
mem_df["mem_efectiva_MB"] = mem_df["kbmemused_MB"] + mem_df["kbbuffers_MB"] + mem_df["kbcached_MB"]

# Convertir a porcentaje del total físico
mem_df["mem_efectiva_%"] = (mem_df["mem_efectiva_MB"] / mem_total_MB) * 100

# Agrupar cada 3 filas
mem_grouped = mem_df["mem_efectiva_%"].groupby(mem_df.index // 3).mean()

# Graficar uso de memoria como porcentaje
plt.figure(figsize=(14, 6))
plt.bar(range(len(mem_grouped)), mem_grouped, width=0.6, color="steelblue", label="Memoria Usada (RAM + Buffers + Cache)")

plt.xlabel("Grupo de Iteraciones (cada 3)")
plt.ylabel("Uso de Memoria (%)")
plt.title("Uso de Memoria (porcentaje del total de 31881 MB)")
plt.ylim(0, 100)
plt.legend()
plt.tight_layout()
plt.grid(axis="y")
plt.show()
