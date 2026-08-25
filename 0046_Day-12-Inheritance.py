#13/07/2026
#30 DAYS OF CODE IN PYTHON [DAY 12]
#INHERITANCE 
# HackerRank: Implement a Student class using basic Python inheritance and conditional logic.

class Person:
	def __init__(self, firstName, lastName, idNumber):
		self.firstName = firstName
		self.lastName = lastName
		self.idNumber = idNumber
	def printPerson(self):
		print("Name:", self.lastName + ",", self.firstName)
		print("ID:", self.idNumber)

class Student(Person):
    
    # Class constructor
    def __init__(self, firstName, lastName, idNumber, scores):
        # Call the parent class constructor to handle the basic info
        super().__init__(firstName, lastName, idNumber)
        
        # Save the scores list specific to the Student class
        self.scores = scores
        
    # Method to calculate the average and return a grade
    def calculate(self):
        # Step 1: Add up all the scores using a basic loop
        total_sum = 0
        for score in self.scores:
            total_sum += score
            
        # Step 2: Divide by the number of scores to find the average
        number_of_scores = len(self.scores)
        average = total_sum / number_of_scores
        
        # Step 3: Determine the letter grade using explicit if/elif checks
        if average >= 90 and average <= 100:
            return 'O'
        elif average >= 80 and average < 90:
            return 'E'
        elif average >= 70 and average < 80:
            return 'A'
        elif average >= 55 and average < 70:
            return 'P'
        elif average >= 40 and average < 55:
            return 'D'
        else:
            return 'T'

line = input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(input()) # not needed for Python
scores = list( map(int, input().split()) )
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())