import copy
import json

def gen(num):
    temp_course = {
        "model": "rateMyCourse.course",
        "pk": 5,
        "fields": {
            "name": "1",
            "website": "",
            "course_ID": "08081",
            "description": "",
            "course_type": "",
            "credit": 1.0
        }
    }

    temp_teachcourse = {
        "model": "rateMyCourse.teachcourse",
        "pk": 5,
        "fields": {
            "course": 5,
            "department": 3,
            "teachers": [
                3
            ]
        }
    }

    course_list = []
    teachcourse_list = []

    for i in range(num):
        course = copy.deepcopy(temp_course)
        course["pk"] = 5+i
        course["fields"]["name"] = str(i+1)
        course["fields"]["course_ID"] = "0808" + str(i+1)
        course_list.append(course)

        teachcourse = copy.deepcopy(temp_teachcourse)
        teachcourse["pk"] = 5+i
        teachcourse["fields"]["course"] = 5+i
        teachcourse_list.append(teachcourse)

    course_str = json.dumps(course_list, indent=2)
    teachcourse_list = json.dumps(teachcourse_list, indent=2)

    return course_str, teachcourse_list


if __name__ == "__main__":
    cs, ts = gen(50)   
    with open("cs.json", "w") as fd:
        fd.write(cs)
    with open("ts.json", "w") as fd:
        fd.write(ts)
    print("Done")
     