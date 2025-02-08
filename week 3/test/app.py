import sys
import csv
import matplotlib.pyplot as plt
from pyhtml import html, body, h1, table, tr, td, th

def read_csv():
    data = []
    try:
        with open("data.csv", mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                data.append({
                    "student_id": row[0],
                    "course_id": row[1],
                    "marks": int(row[2])
                })
    except FileNotFoundError:
        print("CSV file not found!")
        sys.exit(1)
    return data

def generate_student_html(student_data):
    rows = [tr(td(student["student_id"]), td(student["course_id"]), td(student["marks"])) for student in student_data]
    total_marks = sum([student["marks"] for student in student_data])
    rows.append(tr(td("Total Marks"), td(""), td(str(total_marks))))

    return html(
        body(
            h1("Student Details"),
            table(*rows)
        )
    )

def generate_course_html(course_data, avg_marks, max_marks):
    return html(
        body(
            h1("Course Details"),
            table(
                tr(th("Average Marks"), td(str(avg_marks))),
                tr(th("Maximum Marks"), td(str(max_marks)))
            )
        )
    )

def generate_histogram(course_data):
    marks = [student["marks"] for student in course_data]
    plt.hist(marks, bins=10, color='skyblue', edgecolor='black')
    plt.title("Marks Distribution")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("histogram.png")

def main():
    if len(sys.argv) != 3:
        print("Invalid arguments")
        return
    
    param_type = sys.argv[1]
    param_value = sys.argv[2]

    data = read_csv()

    if param_type == "-s":
        student_id = param_value
        student_data = [d for d in data if d["student_id"] == student_id]
        if not student_data:
            print("Invalid student ID")
            return
        html_output = generate_student_html(student_data)
        with open("output.html", "w") as f:
            f.write(str(html_output))
    
    elif param_type == "-c":
        course_id = param_value
        print("Available course IDs:", set(d["course_id"] for d in data))
        
        course_data = [d for d in data if d["course_id"] == course_id]
        if not course_data:
            print("Invalid course ID")
            return
        
        avg_marks = sum([d["marks"] for d in course_data]) / len(course_data)
        max_marks = max([d["marks"] for d in course_data])
        html_output = generate_course_html(course_data, avg_marks, max_marks)
        
        with open("output.html", "w") as f:
            f.write(str(html_output))
        
        generate_histogram(course_data)
    
    else:
        print("Invalid parameter")
        return

if __name__ == "__main__":
    main()

