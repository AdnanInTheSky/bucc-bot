def role_gen(department: str, designation: str) -> list[str]:
    """
    Generates a list of role names based on the user's department and designation.

    Args:
        department: The user's department.
        designation: The user's designation.

    Returns:
        A list of role names.
    """
    # Mapping for specific designations to their corresponding role names
    role_map = {
        "Senior Executive": "Senior Executive",
        "Governing Body": "Governing Body",
        "Executive Body": "Executive Body",
        "Alumni": "Alumni",
        "Faculty": "Faculty"
    }

    # Mapping for departments to their corresponding role names
    department_map = {
        "Communication and Marketing": "C&M",
        "Creative": "Creative",
        "Event Management": "Event",
        "Finance": "Finance",
        "Human Resources": "HR",
        "Press Release and Publications": "Press Release",
        "Research and Development": "R&D",
    }

    # Determine roles based on designation
    if designation in ["Governing Body", "Executive Body", "Alumni"]:
        # For these designations, only the designation role is assigned
        return [role_map[designation]]
    else:
        # For other designations, department role is assigned
        if designation == "Senior Executive":
            # Senior Executives get both department and designation roles
            return [department_map[department], role_map[designation]]
        else:
            # General members & executives get only the department role
            return [department_map[department]]
