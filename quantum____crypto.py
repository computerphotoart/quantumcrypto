import hashlib
from qiskit import QuantumCircuit, Aer, transpile, assemble

class QuantumHash:
    def __init__(self, input_string):
        self.input_string = input_string

    def run(self):
        # Define the quantum circuit
        qc = QuantumCircuit(len(self.input_string), len(self.input_string))

        # Apply Hadamard gates to all qubits
        qc.h(range(len(self.input_string)))

        # Apply X gates according to the input string
        for i, char in enumerate(self.input_string):
            if char == '1':
                qc.x(i)

        # Apply the oracle
        self.__apply_oracle(qc)

        # Apply Grover diffusion operator
        self.__apply_diffusion(qc)

        # Measure all qubits
        qc.measure(range(len(self.input_string)), range(len(self.input_string)))

        # Run the circuit on a quantum simulator
        simulator = Aer.get_backend('qasm_simulator')
        tqc = transpile(qc, simulator)
        qobj = assemble(tqc)
        result = simulator.run(qobj).result()

        # Get the measurement results
        counts = result.get_counts(qc)
        hash_value = max(counts, key=counts.get)

        return hash_value

    def __apply_oracle(self, qc):
        for i in range(len(self.input_string)):
            qc.h(i)
        qc.barrier()
        for i in range(len(self.input_string)):
            qc.x(i)
        qc.cz(0, len(self.input_string)-1)
        for i in range(len(self.input_string)):
            qc.x(i)
        for i in range(len(self.input_string)):
            qc.h(i)
        qc.barrier()

    def __apply_diffusion(self, qc):
        for i in range(len(self.input_string)):
            qc.h(i)
        for i in range(len(self.input_string)):
            qc.x(i)
        qc.cz(0, len(self.input_string)-1)
        for i in range(len(self.input_string)):
            qc.x(i)
        for i in range(len(self.input_string)):
            qc.h(i)
        qc.barrier()

class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        input_string = str(self.index) + self.previous_hash + str(self.data) + str(self.timestamp) + str(self.nonce)
        return hashlib.sha256(input_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", "01/01/2022")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

# Testing the blockchain
my_coin = Blockchain()
my_coin.add_block(Block(1, "", "First transaction", "02/01/2022"))
my_coin.add_block(Block(2, "", "Second transaction", "03/01/2022"))

# Printing the blockchain
for block in my_coin.chain:
    print("Block Index:", block.index)
    print("Block Data:", block.data)
    print("Block Hash:", block.hash)
    print()