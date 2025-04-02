from dotenv import load_dotenv
import os

def role_gen(department, designation):
    role_map = { 
        "Senior Executive": '770620368649715714',
        "Governing Body": '749603683976740945',
        "Executive Body": '749603528216936479',
        "Alumni": '772079823765110784',
    }

    department_map = {
        "Communication and Marketing": '749608792257200160',
        "Creative": '749608742802423929',
        "Event Management": '749608676565713006',
        "Finance": '749608711076708382',
        "Human Resources": '749608865988870254',
        "Press Release and Publications": '749608844019236884',
        "Research and Development": '1213918388070391899'
    }

    if designation == "Governing Body" or designation == "Executive Body" or designation == "Alumni":
        return [role_map[designation]]
    else:
        if designation == "Senior Executive":
            return [department_map[department], role_map[designation]]
        else:
            return [department_map[department]]