import matplotlib.pyplot as plt
import pandas as pd
import os


CSV_PATH = "REPLACE ME"
CSV_FILENAMES = os.listdir(CSV_PATH)

class CSV: 
    def __init__(self, file_name):
        self.FILE_NAME = file_name
    def getYear(self):
        return self.FILE_NAME.split(" ")[1].split(".")[0]
    def getSemester(self):
        return self.FILE_NAME.split(" ")[0]
    def toDataFrame(self):
        return pd.read_csv(os.path.join(CSV_PATH, self.FILE_NAME))
    

class Parser:
    def __init__(self, CSV_FILE_NAMES):
        self.CSV_FILE_NAMES = CSV_FILE_NAMES
        self.CSVS = [] # array of CSV objects
        self.ALL_DATA = {} # dict of dataframes

    def mount_all_data(self):
        for file in self.CSV_FILE_NAMES:
            csv = CSV(file)
            self.ALL_DATA[file] = csv.toDataFrame()
            self.CSVS.append(csv)
    
    def get_all_data(self):
        return self.ALL_DATA
    
    def get_csvs(self):
        return self.CSVS
    

class Search:
    def __init__(self, PARSER):
        self.CSVS = PARSER.get_csvs()

    def convert_to_courses(self,search_results):
        courses = []
        #collect all courses into one array of course objects
        for i in range(len(search_results)):
            for j in range(len(search_results[i])):
                cur_year = self.CSVS[i].getYear()
                cur_sem = self.CSVS[i].getSemester()
                course = Course(str(search_results[i][0]["CRS TITLE"].values[0]),
                                str(search_results[i][0]["DEPT CD"].values[0]),
                                str(search_results[i][0]["DEPT NAME"].values[0]),
                                str(search_results[i][0]["CRS SUBJ CD"].values[0]),
                                int(search_results[i][0]["CRS NBR"].values[0]),
                                int(self.CSVS[i].getYear()),
                                str(self.CSVS[i].getSemester()),
                                str(search_results[i][0]["Primary Instructor"].values[0]),
                                int(search_results[i][0]["Grade Regs"].values[0]),
                                int(search_results[i][0]["W"].values[0]),
                                int(search_results[i][0]["A"].values[0]),
                                int(search_results[i][0]["B"].values[0]),
                                int(search_results[i][0]["C"].values[0]),
                                int(search_results[i][0]["D"].values[0]),
                                int(search_results[i][0]["F"].values[0]))
                courses.append(course)
        
        return courses

    def search_by_crs_crs_nbr(self, crs, crs_nbr):
        search_results = []
        print(f"Searching for {crs} {crs_nbr}...")
        for i in range(len(self.CSVS)):
            df = self.CSVS[i].toDataFrame()
            df = df.loc[(df['CRS SUBJ CD'] == crs) & (df['CRS NBR'] == int(crs_nbr))]
            search_results.append((df,i))

        return self.convert_to_courses(search_results)

    def search_by_professor(self, professor):
        search_results = []
        print(f"Searching for {professor}...")
        for i in range(len(self.CSVS)): #iterate through all csv files
                #search by column CRS SUBJ CD && CRS NBR
                df = self.CSVS[i].toDataFrame()
                df = df.loc[(df['Primary Instructor'] == professor)]
                search_results.append((df,i))                

        return self.convert_to_courses(search_results)
    
    def search_by_dept(self, dept):
        search_results = []
        print(f"Searching for {dept}...")
        for i in range(len(self.CSVS)):
                #search by column CRS SUBJ CD && CRS NBR
                df = self.CSVS[i].toDataFrame()
                df = df.loc[(df['DEPT CD'] == dept)]
                search_results.append((df,i))

        return self.convert_to_courses(search_results)

    
    
class Course:

    def __init__(self, crs_title, dept_cd, dept_name, crs_subj_cd, crs_nbr, session_year, session_semester, professor, registrants, withdrawals, grades_a, grades_b, grades_c, grades_d, grades_f):

        # Dept and class info
        self.CRS_TITLE = crs_title
        self.DEPT_CD = dept_cd
        self.DEPT_NAME = dept_name
        self.CRS_SUBJ_CD = crs_subj_cd
        self.DEPT_NAME = dept_name
        self.CRS_NBR = crs_nbr

        # Session info
        self.SESSION_YEAR = session_year
        self.SESSION_SEMESTER = session_semester
        self.PROFFESOR = professor
        self.REGISTRANTS = registrants
        self.WITHDRAWALS = withdrawals

        # Grade info
        self.GRADES_A = grades_a
        self.GRADES_B = grades_b
        self.GRADES_C = grades_c
        self.GRADES_D = grades_d
        self.GRADES_F = grades_f


    @staticmethod
    def is_same_course(c1, c2):
        return (c1.CRS_TITLE == c2.CRS_TITLE) and (c1.DEPT_CD == c2.DEPT_CD) and (c1.CRS_SUBJ_CD == c2.CRS_SUBJ_CD)
    
    @staticmethod
    def is_same_professor(c1, c2):
        return c1.PROFFESOR == c2.PROFFESOR

    def calculate_average_letter_grade(self):
        decimal = (self.GRADES_A * 4 + self.GRADES_B * 3 + self.GRADES_C * 2 + self.GRADES_D * 1) / (self.REGISTRANTS - self.WITHDRAWALS)
        # caclulate + and - grades and assign a letter grade
        if (decimal >= 3.85):
            return "A+"
        elif (decimal >= 3.5):
            return "A"
        elif (decimal >= 3.15):
            return "A-"
        elif (decimal >= 2.85):
            return "B+"
        elif (decimal >= 2.5):
            return "B"
        elif (decimal >= 2.15):
            return "B-"
        elif (decimal >= 1.85):
            return "C+"
        elif (decimal >= 1.5):
            return "C"
        elif (decimal >= 1.15):
            return "C-"
        elif (decimal >= 0.85):
            return "D+"
        elif (decimal >= 0.5):
            return "D"
        elif (decimal >= 0.15):
            return "D-"
        else:
            return "F"

    def calculate_pass_rate(self):
        return (self.GRADES_A + self.GRADES_B + self.GRADES_C + self.GRADES_D) / (self.REGISTRANTS - self.WITHDRAWALS)
    
    def calculate_fail_rate(self):
        return self.GRADES_F / (self.REGISTRANTS - self.WITHDRAWALS)
    
    def calculate_withdrawal_rate(self):
        return self.WITHDRAWALS / self.REGISTRANTS

    def generate_grade_distribution_image(self, output_path):
        x = ["A", "B", "C", "D", "F"]

        plt.style.use("ggplot")
        plt.size = (10, 10)
        plt.title(f"{self.CRS_SUBJ_CD} {self.CRS_NBR} {self.SESSION_SEMESTER} {self.SESSION_YEAR} Grade Distribution - {self.PROFFESOR}")
        plt.xlabel("Grade")
        plt.ylabel("Number of Students")
        plt.bar(x, [self.GRADES_A, self.GRADES_B, self.GRADES_C, self.GRADES_D, self.GRADES_F])

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
        plt.savefig(output_path,bbox_inches='tight',dpi=100)
        plt.close()


    def __str__(self) -> str:
        return f"{self.CRS_TITLE} {self.DEPT_CD} {self.CRS_SUBJ_CD}"
    

def main():
    parser = Parser(CSV_FILENAMES)
    parser.mount_all_data()
    search = Search(parser)
    search_results = search.search_by_crs_crs_nbr(input("Enter Course Subject Code: "), input("Enter Course Number: "))
    for course in search_results:
        print(course.PROFFESOR + " " + course.CRS_TITLE)
        print("Average Letter Grade: ")
        print(course.calculate_average_letter_grade())
        print("Pass Rate: ")
        print(course.calculate_pass_rate())
        print("Fail Rate: ")
        print(course.calculate_fail_rate())
        print("Withdrawal Rate: ")
        print(course.calculate_withdrawal_rate())
        print()
        course.generate_grade_distribution_image(f"{course.CRS_SUBJ_CD}_{course.CRS_NBR}/{course.CRS_SUBJ_CD}_{course.CRS_NBR}_{course.SESSION_SEMESTER}_{course.SESSION_YEAR}_{course.PROFFESOR}.png")
        



if __name__ == "__main__":
    main()
