import sys
import os
inkscape_extensions_path = os.path.join(os.getenv('INKSCAPE_PATH', '/usr/share/inkscape'), 'extensions')
sys.path.append(inkscape_extensions_path)

try:
    import inkex  # type: ignore
except ImportError as e:
    print("The extension found an error when trying to import inkex")
    print(f"ERROR: {str(e)}")
    sys.exit(1)

import re
import unicodedata
from collections import defaultdict

class SetIdToLabel(inkex.EffectExtension):
    def add_arguments(self, pars):
        # Add tab parameter to handle the one passed by Inkscape
        pars.add_argument("--tab", type=str, dest="tab")
    
    def effect(self):
        if self.svg is None or len(self.svg.selected) == 0:
            self.msg("ERROR: No elements selected. Select one or more elements before running the extension.")
            return 

        # Collect all existing IDs in the document and count labels occurrences
        existing_ids = set()
        label_count = defaultdict(int)

        labelURI = '{http://www.inkscape.org/namespaces/inkscape}label'

        # Process all document elements to collect IDs
        for elem in self.document.getroot().iter():
            elem_id = elem.get('id')
            if elem_id:
                existing_ids.add(elem_id)

            # If this is a selected element, count its label
            if elem in self.svg.selected.values():
                label = elem.get(labelURI)

                if label:
                    label_count[label] += 1
        
        processed = 0 # Count elements that were successfully processed

        errors = {} # Store skipped elements with errors
        skipped = {} # Store skipped elements with NO errors
        labels_updated = {} # Store elements that had their labels updated


        # Iterate over selected elements and set IDs based on labels
        for elem in self.svg.selected.values():
            label = elem.get(labelURI)
            id = elem.get('id') or ''

            ## CHECKS ##

            # Check if the element has a label
            if not label:
                skipped[id] = "Element doesn't have a label or has the default Inkscape label."
                continue

            # Check if the label is the same as the ID
            if id == label:
                skipped[label] = "Element already has the same label as its ID."
                continue

            if not label_count[label]: continue
            
            # Check if this label is unique among selected elements
            if label_count[label] > 1:
                label_count.pop(label)
                errors[label] = "Label appears in multiple selected elements."
                continue
            
            ## PROCESSING ##

            # Handle accented characters by converting them to their base form
            normalized = unicodedata.normalize('NFKD', label)
            without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
            
            # Ensure ID is valid by replacing remaining invalid characters and convert to lowercase
            valid_id = re.sub(r'[^a-zA-Z0-9_-]', '_', without_accents).lower()
            
            # Check if this ID already exists in the document
            if valid_id in existing_ids and valid_id != id:
                errors[label] = "ID already exists in the document."
                continue
            
            # Set the element's ID to the new validated ID and add it to existing_ids
            elem.set('id', valid_id)
            existing_ids.add(valid_id)
            
            # Update label to match ID if they're different
            if valid_id != label:
                elem.set(labelURI, valid_id)
                labels_updated[label] = f"Contains invalid symbols and/or uppercase letters. Using '{valid_id}' as label instead."

            processed += 1

        # Output messages to the user
        self.msg(f"== Summary ======================================== \n")

        self.msg(f"{processed} elements were successfully processed. \n")

        if errors:
            self.msg(f"== Errors ========================================= \n")
            
            for key in errors.keys():
                self.msg(f"{key}: {errors[key]}. \n")
        
        if skipped:
            self.msg(f"== Skipped ======================================== \n")

            for key in skipped.keys():
                self.msg(f"{key}: {skipped[key]} \n")
        
        if labels_updated:
            self.msg(f"== Label Updates ================================== \n")

            for key in labels_updated.keys():
                self.msg(f"{key}: {labels_updated[key]} \n")
        

if __name__ == '__main__':
    SetIdToLabel().run()