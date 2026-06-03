# src/grover.py
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

def grover_2qubits(target="11", shots=1024):
    """Grover para n=2 qubits buscando el estado target."""
    qc = QuantumCircuit(2, 2)

    # Paso 1: superposicion uniforme
    qc.h([0, 1])

    # Paso 2: oraculo de fase — marca el estado target invirtiendo su fase
    # Usa puertas X para convertir el target a |11>, aplica CZ, luego deshace las X
    if target == "11":
        qc.cz(0, 1)
    elif target == "00":
        qc.x([0, 1]); qc.cz(0, 1); qc.x([0, 1])
    elif target == "01":
        qc.x(0); qc.cz(0, 1); qc.x(0)
    elif target == "10":
        qc.x(1); qc.cz(0, 1); qc.x(1)

    # Paso 3: difusor (inversion alrededor de la media)
    # Amplifica la probabilidad del estado marcado
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])

    # Medicion
    qc.measure([0, 1], [0, 1])

    # Mostrar circuito
    print(f"\nCircuito Grover — target |{target}>:")
    print(qc.draw())

    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()

    print(f"Grover buscando |{target}> ({shots} shots):")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        print(f"  |{state}>: {count:4d} ({pct:.1f}%)")

    top = max(counts, key=counts.get)
    resultado = "CORRECTO" if top == target else "ERROR"
    print(f"Estado mas probable: |{top}> — {resultado}")

    # Guardar histograma
    os.makedirs("capturas", exist_ok=True)
    fig = plot_histogram(counts, title=f"Grover — Buscando |{target}>")
    fig.savefig(f"capturas/grover_{target}.png", dpi=150)
    plt.close(fig)
    print(f"Histograma guardado en capturas/grover_{target}.png")

    return counts

if __name__ == "__main__":
    resultados = {}
    for t in ["00", "01", "10", "11"]:
        resultados[t] = grover_2qubits(target=t)
        print()

    # Resumen final
    print("=" * 50)
    print("RESUMEN — Algoritmo de Grover (n=2 qubits)")
    print("=" * 50)
    print(f"{'Target':<10} {'Mas probable':<15} {'Probabilidad':>12}")
    print("-" * 40)
    for t, counts in resultados.items():
        top = max(counts, key=counts.get)
        prob = counts[top] / 1024 * 100
        ok = "OK" if top == t else "ERROR"
        print(f"|{t}>     {ok}  |{top}>          {prob:>10.1f}%")
