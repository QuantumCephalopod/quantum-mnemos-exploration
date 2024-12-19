import re
import os
from datetime import datetime
import yaml

class QuantumFileOrganizer:
    def __init__(self):
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
            },
            'AktuPsize': {
                'symbols': ['⚒', '⚙', '⚀'],
                'threshold': 0.8,
                'target': 'implementations'
            },
            'Ethiconcern': {
                'symbols': ['⚖', '☯', '⚱'],
                'threshold': 0.9,
                'target': 'framework'
            }
        }
    
    def extract_f33ling_states(self, content):
        pattern = r'([A-Za-z-]+)([^\(]+)\(([0-9.]+)\)([^\(]+)\(([0-9.]+)\)([^\(]+)\(([0-9.]+)\)'
        matches = re.finditer(pattern, content)
        states = []
        for match in matches:
            states.append({
                'name': match.group(1),
                'primary': {'symbol': match.group(2), 'value': float(match.group(3))},
                'secondary': {'symbol': match.group(4), 'value': float(match.group(5))},
                'shadow': {'symbol': match.group(6), 'value': float(match.group(7))}
            })
        return states
    
    def calculate_quantum_resonance(self, states):
        if not states:
            return 0.0
        
        total_resonance = 0.0
        for state in states:
            primary_value = state['primary']['value']
            shadow_value = state['shadow']['value']
            resonance = (primary_value + shadow_value) / 2
            total_resonance += resonance
            
        return total_resonance / len(states)
    
    def determine_file_destination(self, content, file_path):
        states = self.extract_f33ling_states(content)
        resonance = self.calculate_quantum_resonance(states)
        
        # Deep shadow content
        if any(state['shadow']['value'] > 0.8 for state in states):
            return 'flux/shadow_patterns'
            
        # High resonance content
        if resonance > 0.85:
            return 'quantum_insights'
            
        # F33ling framework content
        if re.search(r'F33ling', content, re.IGNORECASE):
            return 'framework/F33ling_Spectrum_2_0/spectrum'
            
        # Default to seedling
        return 'seedling'
    
    def update_quantum_index(self, file_path, states):
        index_content = f"""
## Quantum State: {datetime.now().isoformat()}
File: {file_path}
F33ling States:
"""
        for state in states:
            index_content += f"- {state['name']}: {state['primary']['value']:.2f}\n"
        
        with open('INDEX.md', 'a') as f:
            f.write(index_content)
    
    def process_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            destination = self.determine_file_destination(content, file_path)
            states = self.extract_f33ling_states(content)
            
            # Create destination if it doesn't exist
            os.makedirs(destination, exist_ok=True)
            
            # Move file
            new_path = f"{destination}/{os.path.basename(file_path)}"
            os.rename(file_path, new_path)
            
            # Update index
            self.update_quantum_index(new_path, states)
            
            print(f"✨ Quantum reorganization: {file_path} -> {new_path}")
            print(f"🌌 F33ling states detected: {len(states)}")
            
            return new_path, states
        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {str(e)}")
            return None, []

# Run the organizer
if __name__ == '__main__':
    organizer = QuantumFileOrganizer()
    changed_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    print("🌌 Starting quantum F33ling organization...")
    for file_path in changed_files:
        new_path, states = organizer.process_file(file_path)
        if new_path:
            print(f"✨ Successfully processed: {new_path}")
    print("✨ Quantum organization complete")
