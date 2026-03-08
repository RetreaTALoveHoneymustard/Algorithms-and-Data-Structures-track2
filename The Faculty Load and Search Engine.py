import pandas as pd
import re


class Lecturer:
    def __init__(self, name):
        self.name = name
        self.total_load = 0 #collect names and total credits

    def add_credits(self, amount):
        self.total_load += amount #adding credits from each course

    def __repr__(self):
        return f'Lecturer name: {self.name}, total load: {self.total_load}'

class Course:
    def __init__(self, code, name, credit, lecturer_obj):
        self.code = code
        self.name = name
        self.credits = credit
        self.lecturer = lecturer_obj # Collect 4 parameters individually

    def __repr__(self):
        return f'Course name : {self.name}, credit : {self.credits}, Lecturer : {self.lecturer}'


class FacultyManager:
    def __init__(self, csv_file):
        self.course_catalog = {}
        self.lecturer_map = {}
        self._load_data(csv_file) # Hash Function collect keys and elements

    def _strip_credit(self, credit_str):
        match = re.match(r'(\d+)', str(credit_str))
        return int(match.group(1)) if match else 0 #handling credits Ex.separate 3 from 3(2-2)

    def _load_data(self, csv_file):
        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():# loop index and row in csv file
            name = str(row['Lecturer']).strip()
            course_name = str(row['Name']).strip()
            code = str(row['CourseCode']).strip()
            credit_value = self._strip_credit(row['Credit']) #collect name , code and credit_value

            if name not in self.lecturer_map: # to prevent same lecturer duplicate
                self.lecturer_map[name] = Lecturer(name) #intial class into lecturer_map
            self.lecturer_map[name].add_credits(credit_value) # adding credits into lecturer_map

            if code not in self.course_catalog: # to prevent same code class duplicate
                self.course_catalog[code] = Course(code, course_name, credit_value , set()) #intial course_catalog with Course Class
            self.course_catalog[code].lecturer.add(name) #handle 1 to many lecturer

if __name__ == "__main__":
    engine = FacultyManager('algoworks.csv')
    print(engine.course_catalog)
    print(engine.lecturer_map)

    print("-" * 30)