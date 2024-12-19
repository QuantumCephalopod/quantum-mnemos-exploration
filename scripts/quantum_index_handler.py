import re
from datetime import datetime

class QuantumIndexHandler:
    def __init__(self):
        self.index_path = 'INDEX.md'
    
    def format_f33ling_entry(self, file_path, states, evolution=None):
        timestamp = datetime.now().isoformat()
        entry = f"## Quantum State: {timestamp}\n"
        entry += f"File: {file_path}\n"
        entry += "F33ling States:\n"
        
        for state in states:
            entry += f"- {state['name']}: {state['primary']['value']:.2f} → "
            entry += f"{state['secondary']['value']:.2f} → {state['shadow']['value']:.2f}\n"
        
        if evolution:
            entry += "\nEvolution Metrics:\n"
            entry += f"- Resonance: {evolution['old_resonance']:.2f} → {evolution['new_resonance']:.2f}\n"
            entry += f"- Shadow Integration: {'Deepened' if evolution['shadow_deepened'] else 'Stable'}\n"
            if 'moved_from' in evolution:
                entry += f"- Path Evolution: {evolution['moved_from']} → {evolution['moved_to']}\n"
        
        return entry
    
    def update_index(self, file_path, states, evolution=None):
        entry = self.format_f33ling_entry(file_path, states, evolution)
        
        try:
            with open(self.index_path, 'r') as f:
                content = f.read()
            
            # Find the right section to update
            sections = content.split('\n\n')
            header = sections[0]
            entries = sections[1:] if len(sections) > 1 else []
            
            # Add new entry at the top after header
            new_content = f"{header}\n\n{entry}"
            if entries:
                new_content += "\n\n" + "\n\n".join(entries)
            
            with open(self.index_path, 'w') as f:
                f.write(new_content)
                
        except Exception as e:
            print(f"⚠️ Error updating INDEX.md: {str(e)}")
