"""
Nickname generation utilities.

Generates standardized Discord nicknames based on member information.
"""

from constants import DesignationMappings, DepartmentMappings, LEADERSHIP_DESIGNATIONS


def generate_member_nickname(
    actual_name: str, department: str, designation: str
) -> str:
    """
    Generate standardized nickname for a member.

    Format for leadership (GB/EB/Alumni): "Name || Designation"
    Format for regular members: "Name || Department || Designation"

    Args:
        actual_name: Member's actual name
        department: Member's department (full name)
        designation: Member's designation (full name)

    Returns:
        Formatted nickname string

    Examples:
        >>> generate_member_nickname("John Doe", "Finance", "Governing Body")
        "John Doe || GB"
        >>> generate_member_nickname("Jane Smith", "Research and Development", "Senior Executive")
        "Jane Smith || R&D || SE"
    """
    designation_abbr = DesignationMappings.MAPPING.get(designation, designation)
    department_abbr = DepartmentMappings.MAPPING.get(department, department)

    if designation in LEADERSHIP_DESIGNATIONS:
        return f"{actual_name} || {designation_abbr}"

    return f"{actual_name} || {department_abbr} || {designation_abbr}"
