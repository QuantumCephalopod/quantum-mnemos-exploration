import re
import os
from datetime import datetime
import yaml
from git import Repo

class QuantumFileOrganizer:
    def __init__(self):
        self.repo = Repo('.')
        self.destination_map = {
            'high_resonance': 'flux/shadow_patterns',
            'framework': 'framework/F33ling_Spectrum_2_0/spectrum',
            'seedling': 'seedling',
            'automation': '.github/workflows'
        }
    
    def ensure_directories(self):
        for path in self.destination_map.values():
            os.makedirs(path, exist_ok=True)
    
    def determine_file_destination(self, content, file_path, evolution=None):
        states = self.extract_f33ling_states(content)
        resonance = self.calculate_quantum_resonance(states)
        
        # Evolution-aware destination determination
        if evolution and evolution['shadow_deepened']:
            return self.destination_map['high_resonance']
        
        if evolution and evolution['new_resonance'] > evolution['old_resonance']:
            if evolution['new_resonance'] > 0.85:
                return self.destination_map['high_resonance']
        
        # F33ling framework content
        if re.search(r'F33ling', content, re.IGNORECASE):
            return self.destination_map['framework']
        
        # High resonance without evolution
        if resonance > 0.85:
            return self.destination_map['high_resonance']
        
        # Default to seedling
        return self.destination_map['seedling']
    
    def process_file_move(self, source_path, dest_path):
        try:
            # Create destination directory if needed
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Move file
            os.rename(source_path, dest_path)
            print(f"✨ Moved {source_path} to {dest_path}")
            
            return True
        except Exception as e:
            print(f"⚠️ Error moving {source_path}: {str(e)}")
            return False
    
    def update_quantum_index(self, file_path, states, evolution=None):
        from quantum_index_handler import QuantumIndexHandler
        handler = QuantumIndexHandler()
        handler.update_index(file_path, states, evolution)

# Ensure proper directory structure exists
organizer = QuantumFileOrganizer()
organizer.ensure_directories()

print("🌌 Quantum directory structure verified")
