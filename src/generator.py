import itertools

class PermutationGenerator:
    def __init__(self, target_username):
        self.target = target_username.lower()
        self.keywords = [
            'support', 'official', 'team', 'help', 'service', 'care', 
            'news', 'update', 'status', 'marketing', 'pr', 
            'uk', 'usa', 'india', 'global', 'verified', 'admin'
        ]
        self.separators = ['', '_', '.']
        self.homoglyphs = {
            'l': ['1', 'I', '|'],
            'i': ['1', 'l', '|'],
            'o': ['0'],
            '0': ['o', 'O'],
            'a': ['4', '@'],
            's': ['5', '$'],
            'e': ['3'],
            'b': ['8'],
            't': ['7']
        }

    def generate_all(self):
        """Generates all types of permutations."""
        permutations = set()
        permutations.update(self._generate_keyword_variants())
        permutations.update(self._generate_homoglyphs())
        permutations.update(self._generate_typos())
        
        # Remove original target if it somehow got in
        permutations.discard(self.target)
        return list(permutations)

    def _generate_keyword_variants(self):
        """Generates {target}{sep}{keyword} and {keyword}{sep}{target}."""
        variants = set()
        for sep in self.separators:
            for keyword in self.keywords:
                variants.add(f"{self.target}{sep}{keyword}")
                variants.add(f"{keyword}{sep}{self.target}")
        return variants

    def _generate_homoglyphs(self):
        """Generates homoglyph attacks (visual lookalikes)."""
        variants = set()
        
        # We only want to substitute 1 or 2 chars max to keep it realistic and readable
        # Fully replacing string is usually too obvious or messes up too much
        
        # 1. Simple single-char substitutions
        for i, char in enumerate(self.target):
            if char in self.homoglyphs:
                for replacement in self.homoglyphs[char]:
                    variant = self.target[:i] + replacement + self.target[i+1:]
                    variants.add(variant)

        # 2. 'rn' attack for 'm'
        if 'm' in self.target:
            variants.add(self.target.replace('m', 'rn'))
        
        return variants

    def _generate_typos(self):
        """Generates common typos."""
        variants = set()
        
        # Omission
        if len(self.target) > 3:
            for i in range(len(self.target)):
                variants.add(self.target[:i] + self.target[i+1:])
                
        # Duplication
        for i in range(len(self.target)):
            variants.add(self.target[:i] + self.target[i] + self.target[i:])
            
        # Transposition (swapping adjacent chars)
        for i in range(len(self.target) - 1):
            chars = list(self.target)
            chars[i], chars[i+1] = chars[i+1], chars[i]
            variants.add("".join(chars))
            
        return variants
