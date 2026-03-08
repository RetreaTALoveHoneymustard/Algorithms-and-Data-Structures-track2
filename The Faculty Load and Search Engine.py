import pandas as pd
import re


class Lecturer:
    def __init__(self, name):
        self.name = name
        self.total_load = 0

    def add_credits(self, amount):
        self.total_load += amount

    def __repr__(self):
        return f'Lecturer name: {self.name}, total load: {self.total_load}'

class Course:
    def __init__(self, code, name, credit, lecturer_obj):
        self.code = code
        self.name = name
        self.credits = credit
        self.lecturer = lecturer_obj


class FacultyManager:
    def __init__(self, csv_file):
        self.course_catalog = {}
        self.lecturer_map = {}
        self._load_data(csv_file)

    def _strip_credit(self, credit_str):
        match = re.match(r'(\d+)', str(credit_str))
        return int(match.group(1)) if match else 0

    def _load_data(self, csv_file):
        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():
            name = str(row['Lecturer']).strip()
            code = str(row['CourseCode']).strip()
            credit_value = self._strip_credit(row['Credit'])

            if name not in self.lecturer_map:
                self.lecturer_map[name] = Lecturer(name)
            self.lecturer_map[name].add_credits(credit_value)

            if code not in self.course_catalog:
                self.course_catalog[code] = {
                    "name": row['Name'],
                    "credits": credit_value,
                    "lecturers": set()
                }
            self.course_catalog[code]["lecturers"].add(name)


if __name__ == "__main__":
    engine = FacultyManager('algoworks.csv')
    print(engine.course_catalog)
    print(engine.lecturer_map)

    print("-" * 30)