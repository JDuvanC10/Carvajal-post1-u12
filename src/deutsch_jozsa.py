# src/deutsch_jozsa.py
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

def oracle_constante(n):
    """Oraculo constante f(x)=0: no hace nada."""
    return QuantumCircuit(n + 1)  # ancilla qubit incluido

def oracle_balanceada(n):
    """Oraculo balanceado: aplica CNOT del qubit i al ancilla."""
    qc = QuantumCircuit(n + 1)
    for i in range(n):
        qc.cx(i, n)  # CNOT qubit_i → ancilla
    return qc

def deutsch_jozsa(oracle_qc, n, shots=1024):
    """Ejecuta el algoritmo Deutsch-Jozsa con el oraculo dado."""
    qc = QuantumCircuit(n + 1, n)

    # Inicializar ancilla en |-> = H|1>
    qc.x(n)
    qc.h(range(n + 1))  # H en todos los qubits

    # Aplicar oraculo
    qc.compose(oracle_qc, inplace=True)

    # Interferencia: H en qubits de entrada
    qc.h(range(n))

    # Medir solo los qubits de entrada (no el ancilla)
    qc.measure(range(n), range(n))

    # Mostrar circuito
    print(qc.draw())

    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()
    return counts

if __name__ == "__main__":
    n = 2

    # --- Oraculo constante: todos los resultados deben ser "00" ---
    print("=== Oraculo CONSTANTE ===")
    counts_c = deutsch_jozsa(oracle_constante(n), n)
    print(f"Resultados: {counts_c}")  # esperado: {"00": 1024}

    # --- Oraculo balanceado: ningun resultado debe ser "00" ---
    print("\n=== Oraculo BALANCEADO ===")
    counts_b = deutsch_jozsa(oracle_balanceada(n), n)
    print(f"Resultados: {counts_b}")  # esperado: sin "00"

    # Verificaciones
    assert "00" in counts_c, "Error: oraculo constante no retorno 00"
    assert "00" not in counts_b, "Error: oraculo balanceado retorno 00"
    print("\nOK: Deutsch-Jozsa verifica correctamente")

    # Guardar histogramas
    os.makedirs("capturas", exist_ok=True)

    fig_c = plot_histogram(counts_c, title="Deutsch-Jozsa: Oraculo Constante")
    fig_c.savefig("capturas/dj_constante.png", dpi=150)
    plt.close(fig_c)

    fig_b = plot_histogram(counts_b, title="Deutsch-Jozsa: Oraculo Balanceado")
    fig_b.savefig("capturas/dj_balanceado.png", dpi=150)
    plt.close(fig_b)

    print("Histogramas guardados en capturas/")
