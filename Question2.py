from collections import deque, defaultdict

class FriendGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_friendship(self, person1, person2):
        self.graph[person1].append(person2)
        self.graph[person2].append(person1)

    def find_friends(self, person):
        return self.graph[person]

    def find_common_friends(self, person1, person2):
        return set(self.graph[person1]).intersection(self.graph[person2])

    def find_nth_connection(self, person1, person2):
        if person1 == person2:
            return 0
        
        visited = set()
        queue = deque([(person1, 0)])
        
        while queue:
            current_person, depth = queue.popleft()
            
            if current_person == person2:
                return depth
            
            if current_person not in visited:
                visited.add(current_person)
                for friend in self.graph[current_person]:
                    if friend not in visited:
                        queue.append((friend, depth + 1))
        
        return -1

def main():
    fg = FriendGraph()
    
    while True:
        print("\nOptions:")
        print("1. Add friendship")
        print("2. Find friends of a person")
        print("3. Find common friends between two people")
        print("4. Find nth connection between two people")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            person1 = input("Enter the name of the first person: ")
            person2 = input("Enter the name of the second person: ")
            fg.add_friendship(person1, person2)
          
        
        elif choice == "2":
            person = input("Enter the name of the person: ")
            friends = fg.find_friends(person)
            
        
        elif choice == "3":
            person1 = input("Enter the name of the first person: ")
            person2 = input("Enter the name of the second person: ")
            common_friends = fg.find_common_friends(person1, person2)
            
        
        elif choice == "4":
            person1 = input("Enter the name of the first person: ")
            person2 = input("Enter the name of the second person: ")
            connection = fg.find_nth_connection(person1, person2)
            if connection == -1:
                print("-1)
            else:
                print(f"{connection}")
        
        elif choice == "5":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


"""Time Complexity:
add_friendship: O(E)
find_common_friends: O(min(F1,F2)) per query
find_nth_connection: O(V+E) per query

Space Complexity:
Adjacency List: O(V+E)
find_friends: O(1) per query
find_common_friends: O(min(F1,F2)) per query
find_nth_connection: O(V) per query """
