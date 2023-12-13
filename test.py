import collections
import itertools

class splifydebts():
  def minTransfers(self, transactions):
    balances = collections.defaultdict(int)
    people = set()
    for giver, receiver, amount in transactions:
      balances[giver] -= amount
      balances[receiver] += amount
      people |= {giver, receiver}
    for person, balance in balances.items():
      if balance == 0:
        people.discard(person)
        del balances[person]
    people_list = list(people)
    print(people_list)
    def dfs(people_list):
      if not people_list:
        return 0
      people = set(people_list)
      for i in range(2, len(people_list) + 1):
        for persons in itertools.combinations(people_list, i):
          if sum(balances[p] for p in persons) == 0:
            people -= set(persons)
            return dfs(list(people)) + len(persons) - 1

    return dfs(people_list)

list_transaction = [['G','T',25],['G','K',10],['B','T',25],['B','K',10]]
print(splifydebts().minTransfers(list_transaction))