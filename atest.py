# Test script to check memory
from memory.memory_manager import MemoryManager

memory = MemoryManager()

# Get stored experiences
experiences = memory.retrieve_experiences("user", 20)
stats = memory.get_memory_statistics("user")

print(f"Total experiences: {len(experiences)}")
print(f"Memory stats: {stats}")

for i, exp in enumerate(experiences[:5]):
    exp_data = exp.get('experience', {})
    print(f"{i+1}. {exp_data.get('message', 'N/A')[:50]}...")
