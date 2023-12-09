class Formula:
	def __init__(self): pass

	def modus_ponens(self, form):
		# This method represents the Modus Ponens inference rule, returning the result of applying
		# Modus Ponens to formulas 'a' and 'b'.
		# self, FORM = a -> b ===> b
		# FORM has here always the form Implies(a, b)
		if isinstance(form, Implies) and self == form.get_left():
			return form.get_right()
		else:
			None

	def is_axiom1(self):
		# This method checks whether the formula is derived from axiom scheme 1
		if isinstance(self, Implies):
			left = self.get_left()
			right = self.get_right()
			if isinstance(right, Implies):
				return left == right.get_right()
		else:
			return False
		
	def is_axiom2(self):
		# This method checks whether the formula is derived from axiom scheme 2
		if isinstance(self, Implies):
			left = self.get_left()
			right = self.get_right()
			if isinstance(left, Implies) and isinstance(left.get_right(), Implies):
				return isinstance(right.get_left(), Implies) and isinstance(right.get_right(), Implies)
			else:
				return False
		else: 
			return False
		
	def is_axiom3(self):
		# This method checks whether the formula is derived from axiom scheme 3
		if isinstance(self, Implies):
			left = self.get_left()
			right = self.get_right()
			impl = isinstance(right, Implies)
			if isinstance(left, Implies):
				return impl and isinstance(left.get_left(), Not) and isinstance(left.get_right(), Not)
			else:
				return False
		else: 
			return False

	
	def is_and(self):
		# This method checks whether the given logical formula is an instance of the logical AND operation.
		return isinstance(self, And)
	
	def is_or(self):
		# This method checks whether the given logical formula is an instance of the logical OR operation.
		return isinstance(self, Or)
		
	def is_axiom(self):
		# This method checks whether the formula is derived from any axiom scheme
		return self.is_axiom1() or self.is_axiom2() or self.is_axiom3()
  		
	def is_equal(self, formula, environment):
		# This method checks whether the formula is equal to another formula.
		return self.evaluate(environment) == formula.evaluate(environment)
	
	def evaluate(self, environment):
		# This method recursively evaluates a logical formula represented by the object based on the given environment.
		if isinstance(self, Variable):
			return dict.get(environment, self.name)
		
		if isinstance(self, Not):
			return not self.evaluate(self.form)
		
		# If the formula involves binary operations (And, Or, Implies), recursively evaluate the left and right operands
		left = (self.get_left()).evaluate(environment)
		right = (self.get_right()).evaluate(environment)

		if isinstance(self, And): return left and right
		if isinstance(self, Or): return left or right
		if isinstance(self, Implies): return (not left) or right



class Variable(Formula):
	def __init__(self,name):
		self.name = name
		
	def __str__(self):
		return self.to_string()
	
	def to_string(self):
		# This method returns a string representation of the variable.
		return self.name
	

class Implies(Formula):
	def __init__(self,form1, form2):
		self.form1 = form1
		self.form2 = form2
		
	def __str__(self):
		# String representation of the Implies object. Calls the to_string method.
		return self.to_string()
	
	def to_string(self):
		 # Generates a string representation of the Implies object in the form "(form1 => form2)".
		return f"({self.form1.to_string()} => {self.form2.to_string()})"
		
	def get_left(self):
		return self.form1
		
	def get_right(self):
		return self.form2
	
	
class And(Formula):
	def __init__(self, form1, form2):
		self.form1 = form1
		self.form2 = form2

	def to_string(self):
		# Generates a string representation of the And object in the form "(form1 and form2)".
		return f"({self.form1.to_string()} and {self.form2.to_string()})"
	
	def is_and(self):
		return True
	
	def get_left(self):
		return self.form1
				
	def get_right(self):
		return self.form2
	
	
class Or(Formula):
	def __init__(self, form1, form2):
		self.form1 = form1
		self.form2 = form2

	def to_string(self):
		# Generates a string representation of the Or object in the form "(form1 or form2)".
		return f"({self.form1.to_string()} and {self.form2.to_string()})"
	
	def is_and(self):
		return True
	
	def get_left(self):
		return self.form1
				
	def get_right(self):
		return self.form2
	

class Not(Formula):
	def __init__(self, form):
		self.form = form
	
	def __str__(self):
		return self.to_string()
	
	def to_string(self):
		# Generates a string representation of the Not object in the form "(not form)".
		return f"({self.form.to_string()})"
	
	def get_form(self):
		return self.form
		


class Proof:
	def __init__(self, assumptions, proof):
		# Constructor for the Proof class. Initializes a proof with a set of assumptions and a list of logical formulas.
		self.assumptions = assumptions
		self.proof = proof
		
		
	def verify(self):
		# This method verifies the validity of a proof using a modified version of the modus ponens rule.

        # Create a duplicate of the proof to avoid modifying the original
		proof_dup = [p for p in self.proof]
		
		applied = self.apply_modus_ponens(self.assumptions) # extended assumptions
		whole = applied + proof_dup

		for index in range(len(applied), len(whole)):
			phi = whole[index]
			print(phi.is_axiom())
			# Check if the formula is an axiom or part of the original assumptions
			if not (phi.is_axiom() or phi in self.assumptions):
				found = False
				# Iterate over previous formulas in the proof to find potential modus ponens applications
				for j in range(0, index):
					for k in range(j + 1, index):
						MP1 = whole[j].modus_ponens(whole[k]) # may be None
						MP2 = whole[k].modus_ponens(whole[j]) # may be None
						if MP1 != None and phi == MP1:
							found = True
						
						if MP2 != None and phi == MP2:
							found = True

				if not found: return False

		return True


	def apply_modus_ponens(self, formulas):
		# Helper method to apply modus ponens to a set of assumptions.
        # It returns a list of formulas that can be derived using modus ponens from the given assumptions.
		flist = [f for f in formulas]
		for f1 in formulas:
			for f2 in formulas:
				F = f1.modus_ponens(f2)
				if None != F:
					flist.append(F)
		return flist

def test_case_1():
	# This test case should return False
	a = Variable("a")
	b = Variable("b")
	test = Proof([a,b],[a,b, Implies(a,b)])
	return test.verify()

def test_case_2():
	# This test case should return True	
	a = Variable("a")
	b = Variable("b")
	assumptions = [a,b]
	proof = [a,b, Implies(a,Implies(b,a))]
	test = Proof(assumptions, proof)
	return test.verify()

def test_case_3():
	#our test
	a = Variable("a")
	b = Variable("b")
	Ax1 = Implies(a,Implies(b,a))
	Ax11 = Implies(Ax1, Implies(a, Ax1))
	assumptions = []
	proof = [Ax1, Ax11, Implies(a, Ax1), Ax1, a]
	test = Proof(assumptions, proof)
	return test.verify() # false

def test_evaulation():
	a = Variable("a")
	b = Variable("b")
	c = Variable("c")
	implies_formula = Implies(a, And(b, c))
	d = {"a": True, "b": False, "c": True}
	result = implies_formula.evaluate(d)
	print(f"The result if {implies_formula.to_string()} with assignment {d} is: {result}")


if __name__ == "__main__":
	# test_evaulation()
	pass

print("Test case1: ", test_case_1())
print("Test case2: ", test_case_2())
print("Test case3: ", test_case_3())