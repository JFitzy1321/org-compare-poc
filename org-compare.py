"""Organization Unit Hierarchical Comparer Proof of Concept."""

from functools import lru_cache
from typing import Optional

import pandas as pd

# Org Keys (so i don't misspell anything)
ORG_ID = "OrganizationUnitID"
H_LEVEL = "HierarchyLevel"
H_STRING = "HierarchyString"

# Represents OrganizationUnit Class from Cayuse Data Models
class OrgUnit:
    """
    A Representation of the FM OrganizationUnit in Python.

    For this POC, I only care about these fields:

            OrganizationUnitID
            Hierarchy Level
            Hierarchy String
    """

    def __init__(self, **kwargs):
        """Init method."""
        self.id: str = kwargs[ORG_ID]
        self.h_level: int = kwargs[H_LEVEL]
        self.h_string: str = kwargs[H_STRING]
        self._levels: list[int] = []

    def get_levels(self, upper_bound: Optional[int]) -> list[int]:
        """Get a list of Hierarchy Levels by splitting Hierarchy String into ints."""
        if not self._levels:
            # get / 1 / 2 / 3 levels by splitting string, using falsy check to remove whitespace
            # then casting to int, all in a list comprehension
            self._levels = [int(level) for level in self.h_string.split("/") if level]

        return (
            self._levels[:upper_bound]
            if upper_bound and upper_bound < len(self._levels)
            else self._levels
        )

    def __repr__(self):
        """Get string representation method."""
        return f"OrgUnit {ORG_ID}: '{self.id}'  {H_LEVEL}: {self.h_level}  {H_STRING}: '{self.h_string}'"


@lru_cache
def compare_adjacent_orgs(org1: OrgUnit, org2: OrgUnit) -> bool:
    """Algorithmic MacDaddy of this POC.

    This algorithm should only compare Org Units that are adjacent (as in above or below in tree)
    to each other in the Tree Hierarchy.

    IF: Orgs have same id -> True

    IF: Org levels are not 1 level apart -> False

    IF: Sliced Level Lists are equal -> TRUE

    ELSE: FALSE

    Org Level Lists are sliced based on the lowest level org.
    """
    print("Now inside compare function!\n")
    # if comparing the same object, return true
    if org1.id == org2.id:
        print("Comparing the same Org Unit!")
        return True
    # Only compare 'adjacent' Org Units
    elif abs(org1.h_level - org2.h_level) != 1:
        print("Orgs are not in adjacent levels!")
        return False
    # Orgs should be one level above / below each other
    else:
        lowest_common_level = org1.h_level if org1.h_level < org2.h_level else org2.h_level

    # slice lists to common length to compare parent relationship
    parent_list1, parent_list2 = org1.get_levels(lowest_common_level), org2.get_levels(
        lowest_common_level
    )
    print(f"Parent Hierarchy of Org 1: {parent_list1}")
    print(f"Parent Hierarchy of Org 2: {parent_list2}")

    # check if the lists are the same
    return parent_list1 == parent_list2


if __name__ == "__main__":
    # Import csv file with pandas for easy of use
    df = pd.read_csv("org-units-poc1.csv")

    # get a list of OrgUnit class from object above
    org_list = [OrgUnit(**kvpair) for kvpair in df.to_dict("records")]
    list_size = len(org_list)

    while True:
        print()  # new line
        # Get indexes from user to compare org objects
        index1 = int(input(f"Enter number between 0 and {list_size} for Org 1: "))

        index2 = int(input(f"Enter number between 0 and {list_size} for Org 2: "))

        # Get and Show orgs from list, provided by user entered indexes
        org1, org2 = org_list[index1], org_list[index2]
        print(f"\nOrgUnit @ Index {index1}: {org1}")
        print(f"OrgUnit @ Index {index2}: {org2}\n")

        # Do the comparison and display results
        print(f"\nAre Orgs Hierarchical Related: {compare_adjacent_orgs(org1, org2)}\n")

        # Loop again or exit?
        loop_again = input("Again? y/n : ")
        if not loop_again or loop_again.lower()[0] == "y":
            continue
        else:
            break
