import random #To make the random string given to the player
import pandas as pd # type: ignore #This will be used for making a dataframe and with it calculate how common letters are
import unicodedata #For the string manipulation to change accented to unaccented
from collections import Counter
from itertools import permutations #For obtaining all permutations for a 10 letter set
# Define the file path
file_path = 'palabras.txt'

#Dictionary with accented letters and their unaccented counterparts to be replaced by
accented_to_unaccented = {
    'é': 'e', 'í': 'i', 'ú': 'u', 'á': 'a', 'ó': 'o', 'ü': 'u', 'è': 'e'
}

# Initialize an empty list to store the filtered words
filtered_words = []

#Function to replace accents in how common the letters are
def replace_accented_letters(word):
    return ''.join(accented_to_unaccented.get(char, char) for char in word) #This will parse all the words in the file and replace the first char in the dict (the accented one) with the solution

# Open and read the file
with open(file_path, 'r', encoding='utf-8') as file:
    # Read each line (word) in the file
    for line in file:
        # Strip any leading/trailing whitespace, force lowercase and check the word length
        word = line.strip().lower()
        word = replace_accented_letters(word) #Call function to replace accents
        if len(word) <= 10:
            filtered_words.append(word)

#This will join every single word below 10 letters
all_letters = ''.join(filtered_words)

#Count the number of letters in the enormous string
letter_counts = Counter(all_letters)

#With this we count the total amount of letters
total_letters = sum(letter_counts.values())

#Dictionary where we the Normalize the letter counts by dividing them by the total amount of letters, this is dict comprehension the syntax is :{key_expression: value_expression for item in iterable}
normalized_counts = {letter: count / total_letters for letter, count in letter_counts.items()}

#Convert the list to a dataframe, where the first parameter is the data, the second means that the keys of the data (this case the letters) are in the rows and then we specify that the column name is normalized
#Then with reset the letters become a regular column
letter_counts_df = pd.DataFrame.from_dict(normalized_counts, orient='index', columns=['normalized']).reset_index()

#then with rename we rename the column
letter_counts_df = letter_counts_df.rename(columns={'index': 'letter'})

#Sort dataframe 
letter_counts_df = letter_counts_df.sort_values(by='normalized', ascending=False)

#We generate a string of 10 letters (in this case we use the dataframe and take the column)
random_string = ''.join(random.choices(letter_counts_df['letter'], weights=letter_counts_df['normalized'], k=10))

#We print the random weighted string
print("Estas son tus 10 letras con las que hacer una palabra: ", random_string)

#Now we need to find the longest word that can be made with those letters

def find_longest_word(letters, word_list):
    # Sort word_list by length (longest to shortest)
    word_list.sort(key=len, reverse=True)
    
    # Convert word_list to a set for fast lookup
    word_set = set(word_list)
    
    longest_word = ''
    max_length = 0
    
    # Iterate over lengths from len(letters) down to 1
    for length in range(len(letters), 0, -1):
        # Filter word_list to include only words of current length
        filtered_words = [word for word in word_list if len(word) == length]
        # Generate permutations of current length
        for perm in permutations(letters, length): #permutations() given letter set and length gives all permutations
            #the outer for loop will make it so that we start by 10 letter words and after obtaining all permutations of that length we go to 9
            perm_word = ''.join(perm)
            if perm_word in filtered_words:
               if length > max_length:
                    max_length = length
                    longest_word = perm_word
                    # Exit the loop once the longest word is found
                    return longest_word
    
    return longest_word
#Use the longest word function
longest_word = find_longest_word(random_string, filtered_words)


# Ask the user for input
user_input = input("Introduzca la palabra mas larga que haya encontrado: ")

user_input = replace_accented_letters(user_input)#Change accents to compare with list that we have

valid_letters = ['abcdefghijklmnñopqrstuvwxyz'] #All the allowed characters for the words

def validate_user_input(user_input, allowed_letters, word_list):
    if not (1 <= len(user_input) <= 10):
        return False, "La palabra debe tener entre 1 y 10 letras."
    
    if not all(char in allowed_letters for char in user_input):
        return False, "La palabra contiene caracters inválidos."
    
    if user_input not in word_list:
        return False, "La palabra no pertenece al español."
    
    return True, "Respuesta válida."

is_valid, message = validate_user_input(user_input, valid_letters, filtered_words)

if is_valid:
    print("Respuesta válida.", user_input)
else:
    print("La respuesta no es válida.")


print("La palabra mas larga posible era:", longest_word)

