import os
import sys
import platform

def main():
    print("=" * 50)
    print("🚀 DevOps Environment Checker v1.0")
    print("=" * 50)
    
    print(f"\n🐍 Python version: {sys.version.split()[0]}")
    print(f"📁 Python path: {sys.executable}")
    
    print(f"\n💻 Operating System: {platform.system()} {platform.release()}")
    print(f"🖥️  Machine: {platform.machine()}")
    
    print("\n🔍 Checking required tools:")
    
    tools = ["pip", "git", "docker", "kubectl"]
    for tool in tools:
        if os.system(f"which {tool} > /dev/null 2>&1") == 0:
            print(f"   ✅ {tool} - installed")
        else:
            print(f"   ❌ {tool} - not found (will install later)")
    
    print("\n" + "=" * 50)
    print("✅ Environment is ready for DevOps learning!")
    print("=" * 50)

if __name__ == "__main__":
    main()
