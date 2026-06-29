import re
from dicts import diamagn_pascal_coeff, mass_dict


class Unit():
    def __init__(self, name, number=1, curr_valence=None):
        self.name = name
        self.number = float(number) if number else 1.0
        self.curr_valence = curr_valence
        self.mass = self.calc_mass()
        self.valence = self.find_valence()
        self.dia_coefs = self.find_dia()
        
    def __str__(self):
        return self.name
    
    def calc_mass(self):
        return mass_dict.get(self.name, 0)
    
    def find_valence(self):
        atoms_from_table = ' '.join(str(key) for key in diamagn_pascal_coeff.keys())
        atom = self.name
        pattern = re.compile(rf"\b{atom}[+/-]\w*\b")
        matches = pattern.findall(atoms_from_table)
        if len(matches) > 1:
            print('Found more than one valence - ', *matches)
        if self.curr_valence is None:
            self.curr_valence = matches[0]
        return matches
    
    def find_dia(self):
        matches = self.valence
        atom_dict = {}
        for one_atom in matches:
            atom_dict[one_atom] = diamagn_pascal_coeff.get(one_atom, "unknow")
        return atom_dict
    
        

class Composition():
    """Type like 'H2O' or 'H+1 2O-2' need space after valence"""
    def __init__(self, formula, atoms=0, mass=0, dia=0, units=0):
        self.formula = formula
        self.atoms = self.find_atoms()
        self.units = self.make_units()
        self.mass_dia = self.find_dia_mass()
        self.mass = self.mass_dia[0]
        self.dia = self.mass_dia[1]

    def __str__(self):
        return f"all atoms - {self.atoms}, molM= {self.mass_dia[0]} g/mol, dia= {self.mass_dia[1]}*10^-6 cm3/mol" 

    def find_atoms(self):
        text = self.formula
        new_text = text.replace(" ", "")
        print(f"Given {new_text}")
        pattern = re.compile(r'([A-Z][a-z]?)(\d*\.?\d*)')
        atoms_list = pattern.findall(new_text)
        new_list = []
        for atom in atoms_list:
            patt = re.compile(rf'({atom[0]}[+/-][0-9])(\d*\.?\d*)')
            matches = patt.findall(new_text)
            if matches:
                fds = (atom[0], matches[0][1], matches[0][0])
                new_list.append(fds)
            else:
                new_list.append(atom)
        return new_list
    
    def make_units(self):
        return [Unit(*a) for a in self.atoms]
                
    def find_dia_mass(self):
        atoms = self.units
        mass = 0
        dia = 0
        for atom in atoms:
            mass += atom.mass * atom.number
            dia += atom.dia_coefs[atom.curr_valence] * atom.number
        return mass, dia



# formula = "Y 2  Fe+2  Ta O   7   "
# formula2 = "Y 2  Fe+3  Ta O   7   "

# com = Composition(formula)
# print(com)
# print(com.mass)
# print(com.dia)
