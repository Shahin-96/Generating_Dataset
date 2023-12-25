import pandas as pd
import random
import string
from faker import Faker

fake = Faker()

class StudentDataset:
    def __init__(self, num_students=1000):
        self.num_students = num_students
        self.uni_data = self.load_uni_data()  # Load university data
        self.shuffled_indexes = self.shuffle_indexes()  # Shuffled indexes for random access
        self.data = self.generate_random_data()

    def load_uni_data(self):
        df_uni = pd.read_csv('uni_with_ranking.csv', encoding='latin-1')
        return df_uni

    def shuffle_indexes(self):
        indexes = list(range(len(self.uni_data)))
        random.shuffle(indexes)
        return indexes

    def generate_random_data(self):
        # Load real names from the 'FakeNameGenerator.csv' file
        real_names = self.load_real_names()
        uni_names, country_names, uni_ranking = self.load_uni_names()
        course_code, course_name, department = self.load_course_details()

        data = {
            'StudentName': [self.generate_random_real_name(real_names) for _ in range(self.num_students)],
            'StudentNumber': [self.generate_random_number() for _ in range(self.num_students)],
            'CourseName': [self.generate_random_real_name(course_name) for _ in range(self.num_students)],
            'CourseCode': [self.generate_random_uni_ranking(course_code) for _ in range(self.num_students)],
            'Grades': [random.randint(0, 100) for _ in range(self.num_students)],
            'CourseWeight': [random.choice([0.5, 1.0]) for _ in range(self.num_students)],
            'Instructor': [self.generate_random_real_name(real_names) for _ in range(self.num_students)],
            'Department': [self.generate_random_real_name(department) for _ in range(self.num_students)],
            'UniversityName': [],
            'Location': [],
            'Ranking': []
            # 'NumCoursesTaken': [random.randint(1, 10) for _ in range(self.num_students)],
        }
        # for i in range(self.num_students):
        #
        #     uni_index = i % len(self.uni_data)  # Ensures looping over university data
        #     uni_row = self.uni_data.iloc[uni_index]
        #     data['UniversityName'].append(uni_row['school_name'])
        #     data['Location'].append(uni_row['country'])
        #     data['Ranking'].append(uni_row['ranking'])
        for i in range(self.num_students):
            uni_index = self.shuffled_indexes[i % len(self.shuffled_indexes)]
            uni_row = self.uni_data.iloc[uni_index]
            data['UniversityName'].append(uni_row['school_name'])
            data['Location'].append(uni_row['country'])
            data['Ranking'].append(uni_row['ranking'])

        return pd.DataFrame(data)

    def generate_random_real_name(self, real_names):
        return random.choice(real_names)

    # def generate_random_name(self):
    #     unicode_letters = string.ascii_letters + 'à, á, â, ã, ä, å, æ, ç, è, é, ê, ë, ì, í, î, ï, ð, ñ, ò, ó, ô, õ, ö, ÷, ø, ù, ú, û, ü, ý, þ, ÿ'
    #     unicode_uppercase = string.ascii_uppercase + 'À, Á, Â, Ã, Ä, Å, Æ, Ç, È, É, Ê, Ë, Ì, Í, Î, Ï, Ð, Ñ, Ò, Ó, Ô, Õ, Ö, ×, Ø, Ù, Ú, Û, Ü, Ý, Þ, ÿ'
    #     return ''.join(random.choice(unicode_letters) for _ in range(8)), ''.join(random.choice(unicode_uppercase) for _ in range(8))

    # def generate_random_course_name(self, course_name):
    #     course_names = course_name for _ in len
    #     return course_names

    def generate_random_uni_name(self, uni_name):
        return random.choice(uni_name)

    def generate_random_uni_ranking(self, uni_ranking):
        return random.choice(uni_ranking)

    def generate_random_number(self):
        return random.randint(100000, 999999)

    # def generate_random_code(self):
    #     unicode_uppercase = string.ascii_uppercase + 'À, Á, Â, Ã, Ä, Å, Æ, Ç, È, É, Ê, Ë, Ì, Í, Î, Ï, Ð, Ñ, Ò, Ó, Ô, Õ, Ö, ×, Ø, Ù, Ú, Û, Ü, Ý, Þ, ÿ'
    #     return ''.join(random.choice(unicode_uppercase) for _ in range(4))

    def generate_random_uni_location(self, country_names, uni_names):
        uni_location_dict = dict(zip(uni_names, country_names))
        uni_name = random.choice(uni_names)
        return uni_location_dict[uni_names]

    def load_real_names(self):
        df_real_names = pd.read_csv('FakeNameGenerator.csv')
        real_names = df_real_names['GivenName'] + ' ' + df_real_names['Surname']
        return real_names.tolist()

    def load_uni_names(self):
        df_uni_names = pd.read_csv('school_and_country_table.csv')
        uni_ranking = list(range(1, 807))
        random.shuffle(uni_ranking)  # Shuffling the ranking list
        uni_names = df_uni_names['school_name']
        country_names = df_uni_names['country']
        df = pd.DataFrame({'school_name': uni_names, 'country': country_names, 'ranking': uni_ranking})
        df.to_csv('uni_with_ranking.csv', index = False)
        df_uni_w_ranking = pd.read_csv('uni_with_ranking.csv', encoding='latin-1')
        uni_names = df_uni_w_ranking['school_name']
        country_names = df_uni_w_ranking['country']
        uni_ranking = df_uni_w_ranking['ranking']
        return uni_names.tolist(), country_names.tolist(), uni_ranking.tolist()

    def load_course_details(self):
        df_course_det = pd.read_csv('majors-list.csv')
        course_code = df_course_det['Course_Code']
        course_name = df_course_det['Course_Name']
        department = df_course_det['Department']
        print(type(course_name))
        return course_code.tolist(), course_name.tolist(), department.tolist()

    def save_to_csv(self, filename='student_dataset.csv'):
        self.data.to_csv(filename, index=False, encoding='latin-1')
        print(f'Data saved to {filename}')

# Store university rankings in 'school_and_country_table.csv'
dataset = StudentDataset()
dataset.save_to_csv()

# Example Usage:
student_dataset = dataset.data
