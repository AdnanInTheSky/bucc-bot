def nickname_gen(actual_nickname: str, department: str, designation: str) -> str:
    """
    Generates a standardized nickname based on the user's actual nickname,
    department, and designation.

    Args:
        actual_nickname: The user's original nickname.
        department: The user's department.
        designation: The user's designation.

    Returns:
        A formatted nickname string.
    """
    designation_map = {
        "General Member": "GM",
        "Executive": "E",
        "Senior Executive": "SE",
        "Governing Body": "GB",
        "Executive Body": "EB",
        "Alumni": "Alumni",
    }

    department_map = {
        "Communication and Marketing": "C&M",
        "Creative": "Creative",
        "Event Management": "EM",
        "Finance": "Finance",
        "Human Resources": "HR",
        "Press Release and Publications": "PR",
        "Research and Development": "R&D",
    }

    # Get the abbreviated designation and department, or use the original if not found
    designation_abbr = designation_map.get(designation, designation)
    department_abbr = department_map.get(department, department)

    # Format the nickname based on designation
    if designation_abbr in ["GB", "EB", "Alumni"]:
        return f"{actual_nickname} || {designation_abbr}"
    else:
        return f"{actual_nickname} || {department_abbr} || {designation_abbr}"
