"""
Role generation utilities.

Determines which Discord roles should be assigned to members based on
their department and designation.
"""

from constants import DepartmentRoleMappings, LEADERSHIP_DESIGNATIONS, RoleNames


def generate_member_roles(department: str, designation: str) -> list[str]:
    """
    Generate list of role names to assign to a member.

    Leadership (GB/EB/Alumni) get only their designation role.
    Senior Executives get both department and designation roles.
    Regular members get only their department role.

    Args:
        department: Member's department (full name)
        designation: Member's designation (full name)

    Returns:
        List of role names to assign

    Examples:
        >>> generate_member_roles("Finance", "Governing Body")
        ["Governing Body"]
        >>> generate_member_roles("Research and Development", "Senior Executive")
        ["R&D", "Senior Executive"]
        >>> generate_member_roles("Creative", "Executive")
        ["Creative"]
    """
    if designation in LEADERSHIP_DESIGNATIONS:
        return [designation]

    department_role = DepartmentRoleMappings.MAPPING.get(department, department)

    if designation == RoleNames.SENIOR_EXECUTIVE:
        return [department_role, RoleNames.SENIOR_EXECUTIVE]

    return [department_role]
