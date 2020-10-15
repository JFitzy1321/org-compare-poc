import pandas as pd

orgs = pd.read_csv('org-units-poc1.csv').to_dict()

print(orgs)
