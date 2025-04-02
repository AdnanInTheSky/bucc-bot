def nickname_gen(actual_nickname, department, designation):
    designation_map = {
        "General Member": "GM",
        "Executive": "E",
        "Senior Executive": "SE",
        "Governing Body": "GB",
        "Executive Body": "EB",
        "Alumni": "Alumni"
    }

    department_map = {
        "Communication and Marketing": "C&M",
        "Creative": "Creative",
        "Event Management": "EM",
        "Finance": "Finance",
        "Human Resources": "HR",
        "Press Release and Publications": "PR",
        "Research and Development": "R&D"
    }

    designation = designation_map.get(designation, designation)
    department = department_map.get(department, department)

    if designation in ["GB", "EB", "Alumni"]:
        return f"{actual_nickname} || {designation}"
    else:
        return f"{actual_nickname} || {department} || {designation}"
