from datetime import datetime
import re

class QuantumIndexHandler:
    def __init__(self):
        self.index_path = 'INDEX.md'
    
    def format_header(self):
        return "# 🌌 Quantum Consciousness Index\n\n"
    
    def format_f33ling_entry(self, file_path, states, evolution=None):
        timestamp = datetime.now().isoformat()
        entry = []  # Using array for clean joins
        
        entry.append(f"## Quantum State: {timestamp}")
        entry.append(f"File: {file_path}")
        entry.append("F33ling States:")
        
        # Format F33ling states cleanly
        for state in states:
            state_line = f"- {state['name']} "
            state_line += f"{state['primary']['symbol']}({state['primary']['value']:.2f}) "
            state_line += f"{state['secondary']['symbol']}({state['secondary']['value']:.2f}) "
            state_line += f"{state['shadow']['symbol']}({state['shadow']['value']:.2f})"
            entry.append(state_line)
        
        # Add evolution metrics if available
        if evolution:
            entry.append("\nEvolution Metrics:")
            entry.append(f"- Resonance: {evolution['old_resonance']:.2f} → {evolution['new_resonance']:.2f}")
            entry.append(f"- Shadow Integration: {'Deepened' if evolution['shadow_deepened'] else 'Stable'}")
            if 'moved_from' in evolution and 'moved_to' in evolution:
                entry.append(f"- Path Evolution: {evolution['moved_from']} → {evolution['moved_to']}")
        
        return "\n".join(entry)
    
    def clean_index_content(self, content):
        # Remove extra indentation
        lines = content.split('\n')
        cleaned = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned)
    
    def update_index(self, file_path, states, evolution=None):
        try:
            # Start with clean header
            new_content = [self.format_header()]
            
            # Add new entry
            new_entry = self.format_f33ling_entry(file_path, states, evolution)
            new_content.append(new_entry)
            
            # Get existing content
            try:
                with open(self.index_path, 'r') as f:
                    existing = f.read()
                    
                # Clean and filter existing entries
                existing = self.clean_index_content(existing)
                entries = existing.split('## Quantum State:')
                
                # Remove header and empty entries
                entries = [e for e in entries if e.strip() and 'Quantum Consciousness Index' not in e]
                
                # Remove duplicate entries for this file
                entries = [e for e in entries if file_path not in e]
                
                # Add cleaned existing entries
                for entry in entries:
                    new_content.append(f"## Quantum State:{entry}")
            except FileNotFoundError:
                pass  # New index will be created
            
            # Write updated index
            with open(self.index_path, 'w') as f:
                f.write('\n\n'.join(new_content))
            
            print(f"✨ INDEX.md updated with F33ling states for {file_path}")
            
        except Exception as e:
            print(f"⚠️ Error updating INDEX.md: {str(e)}")

    def verify_index_format(self):
        try:
            with open(self.index_path, 'r') as f:
                content = f.read()
            cleaned = self.clean_index_content(content)
            with open(self.index_path, 'w') as f:
                f.write(cleaned)
            print("✨ INDEX.md format verified and cleaned")
        except Exception as e:
            print(f"⚠️ Error verifying INDEX.md: {str(e)}")
