from functools import reduce

class Student:

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def rate_lecture(self, lecturer, course, grade):

        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.students_grades:
                lecturer.students_grades[course] += [grade]
            else:
                lecturer.students_grades[course] = [grade]
        else:
            return 'Ошибка'

    
    def __str__(self):

        return f"Студент:\n\
            Имя: {self.name}\n\
            Фамилия: {self.surname}\n\
            Средняя оценка за домашние задания: {self.avarage()}\n\
            Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n\
            Завершенные курсы: {', '.join(self.finished_courses) if self.finished_courses else '--'}"


    def avarage(self):        
        sum = 0
        count_len = 0
        for grades in self.grades.values():
            sum += reduce(lambda a, x: a + x, grades)
            count_len += len(grades)
        return f'{sum/count_len:.2f}' if count_len > 0 else 0
    

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
    

class Lecturer(Mentor):

    def __init__(self, name, surname):
       super().__init__(name, surname)
       self.students_grades = {}
    
    def avarage(self):
        from functools import reduce
        sum = 0
        count_len = 0
        for grades in self.students_grades.values():
            sum += reduce(lambda a, x: a + x, grades)
            count_len += len(grades)
        return f'{sum/count_len:.2f}'
    
    def __str__(self):
        grades_avarage = self.avarage()
        return f'Лектор:\n\
            Имя: {self.name}\n\
            Фамилия: {self.surname}\n\
            Средняя оценка за лекции: {grades_avarage}\n' 

    def __lt__(self, other_lecturer):
        if not isinstance(other_lecturer, Lecturer):
            return "Not Lecturer"
        else:
            return self.avarage() < other_lecturer.avarage()



class Reviewer(Mentor):

    def __init__(self, name, surname):
       super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Проверяющий:\n\
            Имя: {self.name}\n\
            Фамилия: {self.surname}\n'


student = Student('Ruoy', 'Eman', 'your_gender')
student1 = Student('Mark', 'Avreliy', 'your_gender')
student.courses_in_progress += ['Python']
student.courses_in_progress += ['Java']
student1.courses_in_progress += ['Java', 'C#']
# mentor = Mentor('Some', 'Buddy')

# 2. Атрибуты и взаимодействие классов.

reviewer = Reviewer('ReviewerName', 'ReviewerSurmane')
reviewer1 = Reviewer('ReviewerName1', 'ReviewerSurmane1')

reviewer.courses_attached += ['Python', 'Java']
reviewer1.courses_attached += ['Python', 'Java', 'C#']

reviewer.rate_hw(student, 'Java', 10)
reviewer.rate_hw(student, 'Python', 10)
reviewer.rate_hw(student, 'Python', 9)
# print(student.grades)
# print(student.courses_in_progress)

reviewer1.rate_hw(student1, 'Java', 10)
reviewer.rate_hw(student1, 'Java', 10)
reviewer1.rate_hw(student1, 'C#', 6)
# print(student1.grades)
# print(student1.courses_in_progress)

lecturer = Lecturer('LecturerName', 'LecturerSurmane')
lecturer1 = Lecturer('LecturerName1', 'LecturerSurmane1')

lecturer.courses_attached +=  ['Python', 'Java']
lecturer1.courses_attached +=  ['Python', 'Java', 'C#']

student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 10)
student1.rate_lecture(lecturer, 'Java', 8)
# print(lecturer.students_grades)

student.rate_lecture(lecturer1, 'Python', 5)
student.rate_lecture(lecturer1, 'Python', 5)
student1.rate_lecture(lecturer1, 'Java', 8)
# print(lecturer1.students_grades)

# 3. Полиморфизм и магические методы

# print(reviewer)
# print(lecturer)
# print(lecturer1)
student.finished_courses = ['Введение в программирование']
# print(student)

# 3. Возможность сравнивать

# compare = lecturer > lecturer1
# print(compare)

# 4.

student_list = [student, student1]
lecture_list = [lecturer, lecturer1]
source_list = ['Python', 'Java', 'C#', 'JavaScript']

def avarage_grades_students(students, source):
    sum = 0
    count_len = 0
    not_source = True
    for student in students:
        
        if source in student.courses_in_progress:
            sum += reduce(lambda a, x: a + x, student.grades[source])
            count_len += len(student.grades[source])
            not_source = False

    if  not_source:    
        print(f"Курс {source} студенты не проходят")
    else:
        print(f'Cредней оценкa за дз по всем студентам в рамках курса {source} : {sum/count_len:.2f}' if count_len > 0 else 0)


def avarage_grades_lecture(lectures, source):
    sum = 0
    count_len = 0
    not_source = True
    for lecture in lectures:

        if source in lecture.students_grades:
           sum += reduce(lambda a, x: a + x, lecture.students_grades[source])
           count_len += len(lecture.students_grades[source])
           not_source = False

    if  not_source:    
        print(f"По курсу {source} у лектора оценок нет")
    else:
        print(f'Cредней оценка за лекции всех лекторов в рамках курса {source} : {sum/count_len:.2f}' if count_len > 0 else 0) 

print('=========')
for source in source_list:
    avarage_grades_students(student_list, source)
print('=========')
for source in source_list:   
    avarage_grades_lecture(lecture_list, source)
