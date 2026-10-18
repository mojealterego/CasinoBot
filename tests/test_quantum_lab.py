import unittest
from casinobot.quantum_lab import (
    qubo_energy, solve_qubo_classically, qasm_sampling_template,
    quantum_candidate_assessment, validate_qubo,
)

class QuantumLabTests(unittest.TestCase):
    def test_energy(self):
        self.assertEqual(qubo_energy([[1, -2], [-2, 1]], [1, 1]), -2)

    def test_exact_solution(self):
        result = solve_qubo_classically([[1, -2], [-2, 1]])
        self.assertEqual(result["bits"], [1, 1])
        self.assertEqual(result["energy"], -2)

    def test_single_variable(self):
        self.assertEqual(solve_qubo_classically([[-3]])["bits"], [1])

    def test_qasm_is_sampling_only(self):
        code = qasm_sampling_template([[1, 0], [0, 1]])
        self.assertIn("OPENQASM 2.0;", code)
        self.assertEqual(code.count("measure"), 2)

    def test_no_qpu_claim(self):
        result = quantum_candidate_assessment([[1]])
        self.assertFalse(result["qpu_dispatch"])

    def test_invalid_matrix(self):
        with self.assertRaises(ValueError):
            validate_qubo([[1, 2]])
        with self.assertRaises(ValueError):
            validate_qubo([[float("nan")]])

if __name__ == "__main__":
    unittest.main()
