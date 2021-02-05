import numpy as np
from typing import *
from enum import Enum
from fractions import Fraction



class PauliOperator(Enum):
    """
    Representation of a Pauli operator inside of a rotation block 

    """

    I = "I"
    X = "X"
    Y = "Y"
    Z = "Z"

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)



class PauliProduct(object):

    qubit_num:  int = None
    ops_list:   List[PauliOperator] = None

    def __str__(self) -> str:
        pass


    def __repr__(self) -> str:
        return str(self)

    
    def change_single_op(self, qubit: int, new_op: str) -> None:
        """
        Modify a Pauli Operator

        Args:
            qubit (int): Targeted qubit
            new_op (int): New operator type (I, X, Z, Y)
        """
        self.ops_list[qubit] = PauliOperator(new_op)

    
    def return_operator(self, qubit: int) -> PauliOperator:
        """
        Return the current operator of qubit i. 

        Args:
            qubit (int): Targeted qubit

        Returns:
            PauliOperator: Pauli operator of targeted qubit.
        """
        return self.ops_list[qubit]


    def get_ops_map(self) -> Dict[int,PauliOperator]:
        """"
        Return a map of qubit_n -> operator
        """
        return dict([(qn, self.ops_list[qn]) for qn in range(self.qubit_num) if self.ops_list[qn] != PauliOperator.I])


    
class Rotation(PauliProduct):
    """
    Class for representing a Pauli Product Rotation Block 

    """
    def __init__(self, no_of_qubit: int, rotation_amount: Fraction) -> None:
        """
        Creating a Pauli Product Rotation Block. All operators are set to I (Identity). 
        A Pauli Product Rotation Block MUST span all qubits on the circuit. 

        Args:
            no_of_qubit (int): Number of qubits on the circuit
            rotation_amount (Fraction): Rotation amount (e.g. 1/4, 1/8). Implicitly multiplied by pi.
        """

        self.qubit_num = no_of_qubit
        self.rotation_amount = rotation_amount
        self.ops_list = [PauliOperator("I") for i in range(no_of_qubit)]
    
    
    def __str__(self) -> str:
        return '{}: {}'.format(self.rotation_amount, self.ops_list) 
            
        
    @staticmethod
    def from_list(pauli_ops: List[PauliOperator], rotation: Fraction) -> 'Rotation':
        r = Rotation(len(pauli_ops), rotation)
        for i,op in enumerate(pauli_ops):
            r.change_single_op(i,op)
        return r



class Measurement(PauliProduct):
    """
    Representing a Pauli Product Measurement Block

    """
    def __init__(self, no_of_qubit: int, isNegative: bool = False) -> None:
        """
        Generate a Pauli Product Measurement Block. All operators are set to I (Identity). 
        A Pauli Product Measurement Block MUST span all qubits in the circuit

        Args:
            no_of_qubit (int): Number of qubits in the circuit
            isNegative (bool, optional): Set to negative. Defaults to False.
        """
        self.qubit_num = no_of_qubit
        self.isNegative = isNegative
        self.ops_list = [PauliOperator("I") for i in range(no_of_qubit)]
        

    def __str__(self) -> str:
        return '{}M: {}'.format('-' if self.isNegative else '', self.ops_list) 


    @staticmethod
    def from_list(pauli_ops: List[PauliOperator], isNegative: bool = False) -> 'Measurement':
        m = Measurement(len(pauli_ops), isNegative)
        for i,op in enumerate(pauli_ops):
            m.change_single_op(i,op)
        return m