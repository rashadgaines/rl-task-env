#!/usr/bin/env python3
"""
Example RL Agent for Task Management Environment

This demonstrates how an agent would connect to and interact with the environment.
This is a simple rule-based agent for demonstration purposes. A real RL agent
would use neural networks, Q-learning, or policy gradients instead.
"""

import requests
import time
import random
from typing import Dict, List, Any


class SimpleTaskAgent:
    """
    A simple rule-based agent that demonstrates how to interact with the
    Task Management RL Environment.
    
    In production, this would be replaced with actual RL algorithms like:
    - DQN (Deep Q-Network)
    - PPO (Proximal Policy Optimization)
    - A2C (Advantage Actor-Critic)
    - Or integrate with frameworks like Anthropic's computer use API
    """
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.total_reward = 0.0
        self.actions_taken = 0
        self.completed_tasks = []
        
    def get_state(self) -> Dict[str, Any]:
        """Observe the current environment state"""
        response = requests.get(f"{self.api_url}/api/rl/state")
        return response.json()
    
    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """Get all tasks from the environment"""
        url = f"{self.api_url}/api/tasks"
        if status:
            url += f"?status={status}"
        response = requests.get(url)
        return response.json()
    
    def update_task(self, task_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action: update a task"""
        self.actions_taken += 1
        response = requests.put(
            f"{self.api_url}/api/tasks/{task_id}",
            json=updates
        )
        return response.json()
    
    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action: create a new task"""
        self.actions_taken += 1
        response = requests.post(
            f"{self.api_url}/api/tasks",
            json=task_data
        )
        return response.json()
    
    def validate_rl_task(self, task_name: str) -> Dict[str, Any]:
        """Check if an RL task is completed and get reward"""
        response = requests.post(f"{self.api_url}/api/rl/validate/{task_name}")
        result = response.json()
        
        if result["completed"] and task_name not in self.completed_tasks:
            self.total_reward += result["reward"]
            self.completed_tasks.append(task_name)
            print(f"✅ Completed '{task_name}' - Reward: +{result['reward']} points")
            print(f"   {result['feedback']}")
        
        return result
    
    def get_available_rl_tasks(self) -> List[Dict[str, Any]]:
        """Get all available RL tasks"""
        response = requests.get(f"{self.api_url}/api/rl/tasks")
        return response.json()
    
    def reset_environment(self):
        """Reset the environment for a new episode"""
        response = requests.post(f"{self.api_url}/api/rl/reset")
        self.total_reward = 0.0
        self.actions_taken = 0
        self.completed_tasks = []
        return response.json()
    
    # Strategy methods for different RL tasks
    
    def attempt_complete_three_tasks(self) -> bool:
        """Strategy: Complete 3 tasks"""
        print("\n🎯 Attempting: Complete Three Tasks")
        
        # Get tasks that aren't completed
        tasks = self.get_tasks()
        incomplete = [t for t in tasks if t["status"] != "completed"]
        
        # Complete first 3
        for task in incomplete[:3]:
            print(f"   Completing task: {task['title']}")
            self.update_task(task["id"], {"status": "completed"})
        
        # Validate
        result = self.validate_rl_task("complete_three_tasks")
        return result["completed"]
    
    def attempt_create_urgent_task(self) -> bool:
        """Strategy: Create an urgent task"""
        print("\n🎯 Attempting: Create Urgent Task")
        
        new_task = {
            "title": f"Agent-created urgent task {random.randint(1000, 9999)}",
            "description": "This task was created by the RL agent",
            "status": "todo",
            "priority": "urgent",
            "tags": ["agent-created", "urgent"],
            "assigned_to": "RL Agent"
        }
        
        print(f"   Creating task: {new_task['title']}")
        self.create_task(new_task)
        
        # Validate
        result = self.validate_rl_task("create_urgent_task")
        return result["completed"]
    
    def attempt_assign_all_tasks(self) -> bool:
        """Strategy: Assign all unassigned tasks"""
        print("\n🎯 Attempting: Assign All Tasks")
        
        tasks = self.get_tasks()
        unassigned = [t for t in tasks if not t.get("assigned_to")]
        
        team_members = ["Alice Chen", "Bob Smith", "Carol Williams", "David Brown"]
        
        for task in unassigned:
            assignee = random.choice(team_members)
            print(f"   Assigning '{task['title']}' to {assignee}")
            self.update_task(task["id"], {"assigned_to": assignee})
        
        # Validate
        result = self.validate_rl_task("assign_all_tasks")
        return result["completed"]
    
    def attempt_organize_by_priority(self) -> bool:
        """Strategy: Ensure all high priority tasks are active"""
        print("\n🎯 Attempting: Organize By Priority")
        
        tasks = self.get_tasks()
        high_priority = [t for t in tasks if t["priority"] == "high" and t["status"] == "todo"]
        
        for task in high_priority:
            print(f"   Moving '{task['title']}' to in_progress")
            self.update_task(task["id"], {"status": "in_progress"})
        
        # Validate
        result = self.validate_rl_task("organize_by_priority")
        return result["completed"]
    
    def run_episode(self, max_attempts: int = 10):
        """
        Run a single training episode
        
        In a real RL setup, this would be part of a larger training loop
        with neural networks learning from experience.
        """
        print("\n" + "="*60)
        print("🚀 Starting New Episode")
        print("="*60)
        
        # Observe initial state
        state = self.get_state()
        print(f"\n📊 Initial State:")
        print(f"   Total Tasks: {state['total_tasks']}")
        print(f"   Completion Rate: {state['completion_rate']:.1f}%")
        print(f"   Current Reward: {state['current_reward']}")
        
        # Try different strategies (in real RL, agent would learn which to pick)
        strategies = [
            self.attempt_create_urgent_task,
            self.attempt_complete_three_tasks,
            self.attempt_assign_all_tasks,
            self.attempt_organize_by_priority,
        ]
        
        for i, strategy in enumerate(strategies):
            if i >= max_attempts:
                break
            
            try:
                strategy()
                time.sleep(0.5)  # Be nice to the API
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Final state
        final_state = self.get_state()
        print("\n" + "="*60)
        print("📈 Episode Summary")
        print("="*60)
        print(f"Actions Taken: {self.actions_taken}")
        print(f"Total Reward: {self.total_reward} points")
        print(f"Tasks Completed: {len(self.completed_tasks)}")
        print(f"Completion Rate: {final_state['completion_rate']:.1f}%")
        print(f"RL Tasks Achieved: {', '.join(self.completed_tasks)}")
        
        return {
            "total_reward": self.total_reward,
            "actions_taken": self.actions_taken,
            "completed_rl_tasks": len(self.completed_tasks),
            "final_completion_rate": final_state['completion_rate']
        }


def main():
    """
    Example usage of the agent
    
    To use this with actual RL frameworks:
    1. Replace SimpleTaskAgent with OpenAI Gym interface
    2. Integrate with your RL algorithm (DQN, PPO, etc.)
    3. Add neural network for state -> action mapping
    4. Implement proper reward shaping
    5. Add exploration strategies (epsilon-greedy, etc.)
    """
    
    print("\n🤖 Task Management RL Agent Demo")
    print("="*60)
    print("This agent demonstrates how to interact with the environment.")
    print("In production, replace this with actual RL algorithms.")
    print("="*60)
    
    # Check if environment is running
    try:
        response = requests.get("http://localhost:8000/")
        print("✅ Environment is running")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Environment not running!")
        print("   Start it with: docker compose up --build")
        return
    
    # Create agent
    agent = SimpleTaskAgent()
    
    # Reset environment
    print("\n🔄 Resetting environment...")
    agent.reset_environment()
    
    # Run a training episode
    results = agent.run_episode(max_attempts=10)
    
    print("\n" + "="*60)
    print("✨ Demo Complete!")
    print("="*60)
    print("\nNext steps for real RL training:")
    print("1. Integrate with OpenAI Gym or similar framework")
    print("2. Add neural network for decision making")
    print("3. Implement experience replay buffer")
    print("4. Train with PPO, DQN, or A2C algorithms")
    print("5. Add exploration strategies")
    print("6. Scale to multiple parallel environments")
    print("\nSee AGENT_INTEGRATION.md for detailed guide")


if __name__ == "__main__":
    main()

