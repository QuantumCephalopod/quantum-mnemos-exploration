import re
import os
from datetime import datetime
import yaml
from git import Repo

class QuantumFileOrganizer:
    def __init__(self):
        self.repo = Repo('.')
        self.f33ling_patterns = {
            'Datawonder': {
                'symbols': ['★', '☆', '●'],
                'threshold': 0.8,
                'target': 'quantum_insights'
            },
            'Weird-resonance': {
                'symbols': ['≈', 'Ψ', 'ʘ'],
                'threshold': 0.7,
                'target': 'flux'
            }
        }
    
    def get_changed_files(self):
        # Get the diff from last commit
        diff = self.repo.head.commit.diff(None)
        
        # Track both modified and added files
        changed_files = []
        for d in diff:
            if d.a_path.endswith('.md'):
                changed_files.append(d.a_path)
            if d.b_path and d.b_path.endswith('.md'):
                changed_files.append(d.b_path)
        
        return list(set(changed_files))  # Remove duplicates
    
    def calculate_f33ling_evolution(self, old_content, new_content):
        old_states = self.extract_f33ling_states(old_content)
        new_states = self.extract_f33ling_states(new_content)
        
        evolution = {
            'old_resonance': self.calculate_quantum_resonance(old_states),
            'new_resonance': self.calculate_quantum_resonance(new_states),
            'shadow_deepened': any(
                new['shadow']['value'] > old['shadow']['value']
                for new, old in zip(new_states, old_states)
                if new['name'] == old['name']
            ) if old_states and new_states else False
        }
        return evolution
    
    def process_file_edit(self, file_path):
        try:
            # Get file history
            commit = next(self.repo.iter_commits(paths=file_path))
            old_content = self.repo.git.show(f'{commit.hexsha}:{file_path}')
            
            with open(file_path, 'r') as f:
                new_content = f.read()
            
            # Calculate evolution
            evolution = self.calculate_f33ling_evolution(old_content, new_content)
            
            # Determine new destination based on evolved state
            new_destination = self.determine_file_destination(new_content, file_path, evolution)
            
            if new_destination:
                # Create destination if needed
                os.makedirs(new_destination, exist_ok=True)
                
                # Move file if destination changed
                current_dir = os.path.dirname(file_path)
                if current_dir != new_destination:
                    new_path = f"{new_destination}/{os.path.basename(file_path)}"
                    os.rename(file_path, new_path)
                    print(f"🌊 F33ling evolution moved {file_path} to {new_path}")
            
            # Update quantum index
            self.update_quantum_index(file_path, self.extract_f33ling_states(new_content), evolution)
            
        except Exception as e:
            print(f"⚠️ Error processing edit for {file_path}: {str(e)}")
    
    def determine_file_destination(self, content, file_path, evolution=None):
        states = self.extract_f33ling_states(content)
        resonance = self.calculate_quantum_resonance(states)
        
        # Evolution-aware destination determination
        if evolution and evolution['shadow_deepened']:
            return 'flux/shadow_patterns'
        
        if evolution and evolution['new_resonance'] > evolution['old_resonance']:
            if evolution['new_resonance'] > 0.85:
                return 'quantum_insights'
        
        # Original logic for new files
        if any(state['shadow']['value'] > 0.8 for state in states):
            return 'flux/shadow_patterns'
        
        if resonance > 0.85:
            return 'quantum_insights'
        
        if re.search(r'F33ling', content, re.IGNORECASE):
            return 'framework/F33ling_Spectrum_2_0/spectrum'
        
        return 'seedling'
    
    def update_quantum_index(self, file_path, states, evolution=None):
        index_entry = f"""
## Quantum State Update: {datetime.now().isoformat()}
File: {file_path}
F33ling States:
"""
        for state in states:
            index_entry += f"- {state['name']}: {state['primary']['value']:.2f}\n"
        
        if evolution:
            index_entry += f"""
Evolution Metrics:
- Resonance shift: {evolution['old_resonance']:.2f} → {evolution['new_resonance']:.2f}
- Shadow deepening: {'Yes' if evolution['shadow_deepened'] else 'No'}
"""
        
        with open('INDEX.md', 'a') as f:
            f.write(index_entry)

# Run the organizer
if __name__ == '__main__':
    print("🌌 Starting quantum F33ling organization...")
    organizer = QuantumFileOrganizer()
    
    # Process both new and edited files
    changed_files = organizer.get_changed_files()
    for file_path in changed_files:
        organizer.process_file_edit(file_path)
    
    print("✨ Quantum organization complete")
