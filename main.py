import pandas as pd


class OrgUnit:
    def __init__(self, OrganizationUnitID: str, HierarchyLevel: int, HierarchyString: str):
        self.id = OrganizationUnitID
        self.h_level = HierarchyLevel
        self.h_string = HierarchyString
        self._levels = []

    def get_levels(self):
        # get individual hierarchy levels by spliting the string by '/'
        # then using 'Falsy' value to remove empty strings
        if not self._levels:
            self._levels = [level for level in self.h_string.split("/") if level]

        return self._levels

    def __repr__(self):
        return f"<OrgUnit Id: {self.id} HierarchyLevel: {self.h_level} HierarchyString: {self.h_string} />"


# def org_comparer(org1: OrgUnit, org2: OrgUnit):
#     # need 'highest' common level


def orgs_are_in_same_branch(org1, org2):
    # Get the 'highest' common level between the 2 objects
    org1_h_level = org1.h_level
    org2_h_level = org2.h_level

    highest_common_level = 1

    # if orgs are root level, then they aren't related
    if org1_h_level == 1 and org2_h_level == 1:
        return False
    # If orgs are not roots and are on the same level
    # Get one level above for comparison
    elif org1_h_level == org2_h_level:
        highest_common_level = org1_h_level - 1
    # Orgs are on different levels
    else:
        highest_common_level = (
            org1.hierarchy_level
            if org1.hierarchy_level >= org2.hierarchy_level
            else org2.hierarchy_level
        )

    print("Highest Common Hierarchy Level between Orgs: ", highest_common_level)
    # slice lists to common length
    org1_levels = org1.get_levels()[:highest_common_level]
    org2_levels = org2.get_levels()[:highest_common_level]
    print(org1_levels)
    print(org2_levels)

    # check if the lists are the same, to see if objects are in the same hierarchy
    return org1_levels == org2_levels


if __name__ == "__main__":
    df = pd.read_csv("org-units-poc1.csv")
    _org_list = df["HierarchyString", "OrganizationUnitID", "HierarchyLevel"].to_dict("records")
    org_list = [OrgUnit(**kwargs) for kwargs in _org_list]

    org1 = org_list[3]
    org2 = org_list[4]
    print(f"Org 1: ", org1)
    print(f"Org 2: ", org2)

    print("Are Orgs related: ", orgs_are_in_same_branch(org1, org2))
