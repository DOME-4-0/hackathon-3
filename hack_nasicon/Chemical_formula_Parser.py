import re

class ChemicalFormulaParser:
    def __init__(self, formula):
        self.formula = formula
        self.fu_list = self.split_formula(formula)  # Split into formula units
        self.elements = []  # List of elements
        self.stoichiometry = []  # List of stoichiometric values
        self.parse_fus(self.fu_list)  # Parse formula units and fill element and stoichiometry lists

    # Step 1: Split the chemical formula into formula units
    def split_formula(self, formula):
        # Regex pattern to match elements with their stoichiometric values
        pattern = r'[A-Z][a-z]*\d*\.?\d*'
        fu_list = re.findall(pattern, formula)
        return fu_list

    # Step 2: Parse formula units and fill the elements and stoichiometry lists
    def parse_fus(self, fu_list):
        # Regex pattern to match element and stoichiometric value
        pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
        for fu in fu_list:
            match = re.match(pattern, fu)
            if match:
                element = match.group(1)
                stoich = match.group(2)
                # Default stoichiometric value to 1 if not provided
                stoich = float(stoich) if stoich else 1
                self.elements.append(element)
                self.stoichiometry.append(stoich)

    # Print the formula units
    def display_units(self):
        print("Formula Units:", self.fu_list)

    # Print the elements and stoichiometry lists
    def display_lists(self):
        print("Elements List:", self.elements)
        print("Stoichiometry List:", self.stoichiometry)


# Example: Using ChemicalParser to process a chemical formula
material_formula = "LiTi2P3O12"
parser = ChemicalFormulaParser(material_formula)
parser.display_units()        # Print formula units
parser.display_lists()        # Print element and stoichiometry lists




