from typing import Tuple


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        #Da li je posledji karakter u reci 
        self.word_finished = False
        self.counter = 1
        self.statusi = []
        

    def add(root, word: str, status_id):

        node = root
        for char in word:
            found_in_child = False

            for child in node.children:
                if child.char == char:

                    child.counter += 1

                    node = child
                    found_in_child = True
                    break

            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)

                node = new_node

        node.word_finished = True
        node.statusi.append(status_id)


    def find_prefix(root, prefix: str) -> Tuple[bool, int]:
        #isto kao funkcija broj_pojavljivanja samo sto je druga povratna vrednost 
        #umesto broja pojavljivanja lista id-jeva svih statusa u kojima se pojavljuje prefiks
        node = root

        if not root.children:
            return False, []
        for char in prefix:
            char_not_found = True

            for child in node.children:
                if child.char == char:

                    char_not_found = False

                    node = child
                    break

            if char_not_found:
                return False, []

        return True, node.statusi
    
    def broj_pojavljivanja(root, prefix: str) -> Tuple[bool, int]:
        """
        Povratna vrednost
        1. Da li prefiks postoji u reci
        2. Ako postoji koliko reci ga sadrzi
        """
        node = root

        if not root.children:
            return False, 0
        for char in prefix:
            char_not_found = True

            for child in node.children:
                if child.char == char:

                    char_not_found = False

                    node = child
                    break
            # ukoliko ne pronadje vraca False
            if char_not_found:
                return False, 0

        return True, node.counter

    def autocomplete(root, prefix):
        
        results = []
        node = root

        for char in prefix:
            char_not_found = True
            for child in node.children:
                if child.char == char:
                    char_not_found = False
                    node = child
                    break
            if char_not_found:
                return results

        def dfs(node, prefix):
            if node.word_finished:
                results.append(prefix)
            for child in node.children:
                dfs(child, prefix + child.char)

        dfs(node, prefix)
        return results
    
    
def napravi_trie(sviStatusi):
    tr=TrieNode("")
    for id in sviStatusi:
        for rec in sviStatusi[id]["tekst"].split(" "):
            tr.add(rec, id)
            
    return tr