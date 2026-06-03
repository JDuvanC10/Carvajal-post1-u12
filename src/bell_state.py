# src/bell_state.py
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

def bell_state_experiment(shots=1024):
    """Prepara el estado de Bell |Φ+> y mide."""
    qc = QuantumCircuit(2, 2)  # 2 qubits, 2 bits clásicos

    # Paso 1: Hadamard en qubit 0 → superposición
    qc.h(0)
    # Paso 2: CNOT (control=0, target=1) → entrelazamiento
    qc.cx(0, 1)
    # Paso 3: medir ambos qubits
    qc.measure([0, 1], [0, 1])

    # Simular con AerSimulator
    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()

    print(f"Resultados Bell |Φ+> ({shots} shots):")
    for state, count in sorted(counts.items()):
        pct = count / shots * 100
        print(f"  |{state}> : {count:4d} ({pct:.1f}%)")

    # Verificar: solo deben aparecer |00> y |11>
    assert "01" not in counts and "10" not in counts, \
        "ERROR: aparecieron estados no entrelazados"
    print("OK: correlacion perfecta verificada")

    # Mostrar diagrama del circuito
    print("\nDiagrama del circuito:")
    print(qc.draw())

    # Guardar histograma
    os.makedirs("capturas", exist_ok=True)
    fig = plot_histogram(counts)
    fig.savefig("capturas/bell_histogram.png", dpi=150)
    plt.close(fig)
    print("Histograma guardado en capturas/bell_histogram.png")

    return counts

if __name__ == "__main__":
    bell_state_experiment()
