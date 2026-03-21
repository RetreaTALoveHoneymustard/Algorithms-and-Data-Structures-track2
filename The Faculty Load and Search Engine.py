import pandas as pd

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
        s = str(credit_str)
        num = ""
        for ch in s:
            if ch.isdigit():
                num += ch
            else:
                break
        return int(num) if num else 0 #handling credits Ex.separate 3 from 3(2-2)

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

    def find_course(self, course_code):
      print(">> find_course", course_code)

      if course_code in self.course_catalog:
        course = self.course_catalog[course_code]
        lecturers = ', '.join(course.lecturer)

        print(f'Course Name: {course.name}')
        print(f'Credit: {course.credits}')
        print(f'Lecturer: {lecturers}')

      else:
        print(f'Course with code {course_code} not found.')


    def report_load(self):
      print(">> report_load")
      for name in (self.lecturer_map.keys()):
        lec_obj = self.lecturer_map[name]
        print(f'Lecturer : {lec_obj.name} | Total Load: {lec_obj.total_load}')

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/RetreaTALoveHoneymustard/Algorithms-and-Data-Structures-track2/main/algoworks.csv"
    try:
      engine = FacultyManager(url)
      print("Successfully Execute")
      try:
        print(engine.course_catalog)
        print(engine.lecturer_map)
        print("Data ready to use")
      except Exception as e:
        print("Something not right")
    except Exception as e:
      print("Error Occur")

    print("-" * 30)
    code = input("Enter Course Code : ")
    engine.find_course(code)
    print("-" * 30)
    engine.report_load()
