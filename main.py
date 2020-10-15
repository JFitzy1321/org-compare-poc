import pandas as pd

# Represents OrganizationUnit Class from Cayuse Data Models
class OrgUnit:
    def __init__(self, OrganizationUnitID: str, HierarchyLevel: int, HierarchyString: str):
        self.id = OrganizationUnitID
        self.h_level = HierarchyLevel
        self.h_string = HierarchyString
        self._levels = []  # Hierarchical Levels in list form

    def get_levels(self):
        # get individual hierarchy levels by spliting the string by '/'
        # then using 'Falsy' value to remove empty strings
        if not self._levels:
            self._levels = [int(level) for level in self.h_string.split("/") if level]

        return self._levels

    def __repr__(self):
        return f"<OrgUnit Id: '{self.id}'  HierarchyLevel: {self.h_level}  HierarchyString: '{self.h_string}' />"


def orgs_are_in_same_branch(org1, org2):
    # if comparing the same object, return true
    if org1.id == org2.id:
        return True

    org1_level = org1.h_level
    org2_level = org2.h_level

    # if orgs are root level, then they aren't related
    if org1_level == 1 and org2_level == 1:
        return False
    # If orgs are not roots and are on the same level
    # Get one level above for comparing Parents
    elif org1_level == org2_level:
        lowest_common_level = org1_level - 1
    # Orgs are on different levels
    else:
        lowest_common_level = org1_level if org1_level < org2_level else org2_level

    print("Lowest Common Hierarchy Level between Orgs: ", lowest_common_level)

    # slice lists to common length to compare parent relationship
    print(level_list_1 := org1.get_levels()[:lowest_common_level])
    print(level_list_2 := org2.get_levels()[:lowest_common_level])

    # check if the lists are the same
    return level_list_1 == level_list_2


if __name__ == "__main__":
    # Import csv file with pandas for easy of use
    df = pd.read_csv("org-units-poc1.csv")

    # get the fields we care about into a workable list of dict objects
    _org_list = df[["HierarchyString", "OrganizationUnitID", "HierarchyLevel"]].to_dict("records")

    # get a list of OrgUnit class from object above
    org_list = [OrgUnit(**kwargs) for kwargs in _org_list]

    size_org_list = len(org_list)
    while True:
        try:
            index1 = int(input(f"Enter number between 0 and {size_org_list} for Org 1: "))
            if index1 > size_org_list:
                raise Exception

            index2 = int(input(f"Enter number between 0 and {size_org_list} for Org 2: "))
            if index2 > size_org_list:
                raise Exception

        except KeyboardInterrupt as kie:
            raise kie
        except:
            print("Invalid input, try again")
            continue
        finally:
            print()  # new line

        # Get and Show orgs from list, provided by user entered indexes
        org1 = org_list[index1]
        org2 = org_list[index2]
        print(f"OrgUnit @ Index {index1}: {org1}")
        print(f"OrgUnit @ Index {index2}: {org2}")

        print("Are Orgs in the same Hierarchy: ", orgs_are_in_same_branch(org1, org2))
        print("\n")

        if input("Again? y/n : ").lower() in ("y", ""):
            continue
        else:
            break