from typing import List, Dict
from sotrans_fastapi_keycloak.role import Role


def _get_highest_role(user_roles: List[str], role_hierarchy: Dict[str, Role]) -> str:
    """
    Get the highest role in the hierarchy from a list of SotransRole enums.

    Args:
        user_roles (List[SotransRole]): List of SotransRole enums.

    Returns:
        SotransRole: The highest SotransRole enum in the hierarchy.
    """
    if not role_hierarchy or not user_roles:
        return
    # Function to calculate the depth of a role in the hierarchy
    def role_depth(role: Role) -> int:
        depth = 0
        while role.ancestors:
            depth += 1
            role = role.ancestors[0]  # assuming one ancestor for simplicity
        return depth

    # Convert SotransRole enums to Role objects
    role_objects = [role_hierarchy[role] for role in user_roles]

    # Sort the Role objects based on their depth in the hierarchy
    sorted_roles = sorted(role_objects, key=role_depth, reverse=True)

    # Find the corresponding SotransRole for the highest Role object
    if sorted_roles:
        for key, value in role_hierarchy.items():
            if value == sorted_roles[0]:
                return key

    return ""
