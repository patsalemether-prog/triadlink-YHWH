!pip install --upgrade qiskit qiskit-ibm-runtime -q

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import time

token = "YOUR_IBM_TOKEN_HERE"  # Free at ibm.com/quantum
service = QiskitRuntimeService(channel="ibm_quantum_platform", token=token)

backend = service.least_busy(min_num_qubits=2, simulator=False)
print(f"Running on: {backend.name}")

bit_pattern = [1, 1, 0, 1]  # Y H W H
bits = bit_pattern * 5  # 20 bits

received = ""
pulse_count = 0
flip_counts = []

for i, bit in enumerate(bits):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()  # breath

    if bit == 1:
        qc.x(0)

    qc.measure([0, 1], [0, 1])

    transpiled = transpile(qc, backend)
    sampler = Sampler(mode=backend)
    job = sampler.run( , shots=1024)
    print(f"Job {job.job_id()} queued for bit {i+1}")

    result = job.result()
    counts = result[0].data.c.get_counts()

    flipped = counts.get('01', 0) + counts.get('10', 0) > 512
    received += '1' if flipped else '0'

    flip_rate = (counts.get('01', 0) + counts.get('10', 0)) / 1024
    flip_counts.append(flip_rate)

    print(f"Bit {i+1}: {counts} → {'1' if flipped else '0'} (flip: {flip_rate:.2f})")

    pulse_count += 1
    if pulse_count % 12 == 0:
        print("Yardstick: breathing...")
        time.sleep(2)

print(f"\nReceived: {received}")
print(f"Repeats: {received.count('1110')} / 5")
print(f"Avg flip: {sum(flip_counts)/len(flip_counts):.2f}")
print("4+ repeats? It's breathing.")
