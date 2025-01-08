
import string
import math
import random
import matplotlib.pyplot as plt

class Distribution(dict):
    
    def __init__(self):
        self.clear()
        self._total = 0
    
    def __missing__(self, key):
        return 0  # Return 0 probability for missing keys
    
    def __setitem__(self, key, value):
        self._total += value - self.get(key, 0)
        super().__setitem__(key, value)
    
    def renormalize(self):
      
        self._total = float(sum(self.values()))
        if self._total <= 0:
            raise ValueError("Sum of probabilities must be positive")
        for key in self:
            self[key] /= self._total

def clean_document(document):
   
    return document.translate(str.maketrans("", "", string.punctuation)).lower()

def build_letter_transition_dist(text):
    
    charset = string.ascii_lowercase + " "
    dist = {key: Distribution() for key in charset}
    doc = clean_document(text)
    
    
    for a in charset:
        for b in charset:
            dist[a][b] += 1

    for i in range(1, len(doc)):
        first_letter = doc[i-1] if doc[i-1].isalpha() else " "
        second_letter = doc[i] if doc[i].isalpha() else " "
        dist[first_letter][second_letter] += 1

    for k in dist:
        dist[k].renormalize()

    return dist

def compute_log_likelihood(document, expected_letter_distribution):
   
    log_likelihood = 0
    for i in range(1, len(document)):
        first_letter = document[i-1].lower() if document[i-1].isalpha() else " "
        second_letter = document[i].lower() if document[i].isalpha() else " "
        log_likelihood += math.log(expected_letter_distribution[first_letter][second_letter])
    return log_likelihood

def decrypt_document(encrypted_document, cipher):
   
    mapping = create_mapping_from_cipher(cipher)
    decrypted = "".join(mapping.get(c.lower(), " ") if c.isalpha() else " " for c in encrypted_document)
    return decrypted

def create_mapping_from_cipher(cipher):
   
    charset = list(string.ascii_lowercase)
    return {charset[i]: cipher[i] for i in range(len(charset))}

def propose_cipher(current_cipher):
  
    charset = list(current_cipher)
    first_letter, second_letter = random.sample(charset, 2)
    new_cipher = "".join(second_letter if c == first_letter else first_letter if c == second_letter else c for c in current_cipher)
    return new_cipher

def generate_random_cipher():
    
    charset = list(string.ascii_lowercase)
    random.shuffle(charset)
    return "".join(charset)

def acceptance_criteria(log_proposal, log_current):
   
    return random.random() < math.exp(log_proposal - log_current)

def run_metropolis_hastings(encrypted_document, expected_letter_distribution, max_acceptance_iter=4000):
  
    encrypted_document = clean_document(encrypted_document)
    current_cipher = generate_random_cipher()
    best_document = ("", float("-inf"))
    number_accepted = 0
    i = 0

    while number_accepted < max_acceptance_iter:
        i += 1
        proposal_cipher = propose_cipher(current_cipher)
        proposal_document = decrypt_document(encrypted_document, proposal_cipher)
        current_document = decrypt_document(encrypted_document, current_cipher)

        log_likelihood_proposal = compute_log_likelihood(proposal_document, expected_letter_distribution)
        log_likelihood_current = compute_log_likelihood(current_document, expected_letter_distribution)

        if log_likelihood_proposal > best_document[1]:
            best_document = (proposal_document, log_likelihood_proposal)

        if acceptance_criteria(log_likelihood_proposal, log_likelihood_current):
            number_accepted += 1
            current_cipher = proposal_cipher

        if i % 100 == 0:
            print(f"Progress: {number_accepted}/{max_acceptance_iter} accepted moves ({i} total attempts)")

    return best_document[0]

def main():
  
    print("Paste your reference text (e.g., a paragraph of normal English text):")
    reference_text = input()
    print("\nPaste your encrypted text:")
    encrypted_text = input()

    print("\nBuilding letter transition distribution...")
    letter_dist = build_letter_transition_dist(reference_text)

    print("\nDecrypting (this may take a few minutes)...")
    decrypted_text = run_metropolis_hastings(encrypted_text, letter_dist)

    print("\nDecrypted text:")
    print("-" * 50)
    print(decrypted_text)
    print("-" * 50)

if __name__ == '__main__':
    main()


### Credits: Josh Hellerstein
