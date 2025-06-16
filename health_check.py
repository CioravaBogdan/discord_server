#!/usr/bin/env python3
"""
Health check script for Discord Bot
Validates configuration, dependencies, and connectivity
"""

import os
import sys
import requests
import importlib.util
from pathlib import Path
from config import Config

def check_environment():
    """Check if environment variables are properly configured"""
    print("🔧 Checking Environment Configuration...")
    
    issues = []
    
    # Check required environment variables
    required_vars = {
        'BOT_TOKEN': 'Discord bot token',
        'CHANNEL_ID': 'Discord channel ID',
        'N8N_WEBHOOK': 'n8n webhook URL'
    }
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            issues.append(f"❌ Missing {var} ({description})")
        else:
            # Mask sensitive values
            if 'token' in var.lower():
                display_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            else:
                display_value = value
            print(f"   ✅ {var}: {display_value}")
    
    # Check optional variables
    optional_vars = {
        'WEBHOOK_PORT': Config.WEBHOOK_PORT,
        'LOG_LEVEL': Config.LOG_LEVEL,
        'DOCKER_ENV': Config.IS_DOCKER
    }
    
    for var, default in optional_vars.items():
        value = os.getenv(var, default)
        print(f"   ✅ {var}: {value}")
    
    return issues

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n📦 Checking Dependencies...")
    
    issues = []
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
    except FileNotFoundError:
        issues.append("❌ requirements.txt not found")
        return issues
    
    for requirement in requirements:
        if not requirement.strip() or requirement.startswith('#'):
            continue
            
        # Parse package name (remove version specs)
        package = requirement.split('>=')[0].split('==')[0].split('<')[0].strip()
        
        # Special handling for some packages
        if package == 'discord.py':
            package = 'discord'
        
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            issues.append(f"❌ Missing package: {package}")
    
    return issues

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking Required Files...")
    
    issues = []
    
    required_files = [
        'main.py',
        'bot.py',
        'webhook_server.py',
        'message_filters.py',
        'config.py',
        'requirements.txt'
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            issues.append(f"❌ Missing file: {file}")
    
    # Check for .env file
    if Path('.env').exists():
        print("   ✅ .env")
    else:
        print("   ⚠️  .env not found (using .env.example as reference)")
    
    return issues

def check_webhook_server():
    """Check if webhook server is accessible"""
    print("\n🌐 Checking Webhook Server...")
    
    issues = []
    
    try:
        url = f"http://{Config.WEBHOOK_HOST}:{Config.WEBHOOK_PORT}/health"
        
        # Try to connect to health endpoint
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Webhook server: {url}")
            print(f"   ✅ Status: {data.get('status', 'unknown')}")
            print(f"   ✅ Bot status: {data.get('bot_status', 'unknown')}")
        else:
            issues.append(f"❌ Webhook server returned {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"   ⚠️  Webhook server not running on {Config.WEBHOOK_HOST}:{Config.WEBHOOK_PORT}")
        print("   💡 This is normal if the bot is not currently running")
    except Exception as e:
        issues.append(f"❌ Webhook check failed: {str(e)}")
    
    return issues

def check_n8n_connectivity():
    """Check if n8n webhook is accessible"""
    print("\n🔗 Checking n8n Connectivity...")
    
    issues = []
    
    try:
        # Try to ping n8n webhook (with OPTIONS or HEAD request)
        webhook_url = Config.N8N_WEBHOOK
        
        if not webhook_url:
            issues.append("❌ N8N_WEBHOOK not configured")
            return issues
        
        # Try HEAD request first (less intrusive)
        try:
            response = requests.head(webhook_url, timeout=10)
            status = response.status_code
        except:
            # If HEAD fails, try OPTIONS
            response = requests.options(webhook_url, timeout=10)
            status = response.status_code
        
        if status in [200, 404, 405]:  # 404 is OK if webhook is not active
            print(f"   ✅ n8n webhook accessible: {webhook_url}")
            if status == 404:
                print("   ⚠️  Webhook returns 404 (webhook may not be active)")
        else:
            issues.append(f"❌ n8n webhook returned {status}")
            
    except requests.exceptions.Timeout:
        issues.append("❌ n8n webhook timeout (>10s)")
    except requests.exceptions.ConnectionError:
        issues.append("❌ Cannot connect to n8n webhook")
    except Exception as e:
        issues.append(f"❌ n8n connectivity check failed: {str(e)}")
    
    return issues

def run_filter_tests():
    """Run message filter tests"""
    print("\n🧪 Running Filter Tests...")
    
    issues = []
    
    try:
        from message_filters import MessageFilter
        
        filter = MessageFilter()
        
        # Quick test cases
        test_cases = [
            {
                'name': 'Normal message',
                'data': {'content': 'Hello world', 'author': {'username': 'user', 'is_bot': False}},
                'should_ignore': False
            },
            {
                'name': 'Bot message',
                'data': {'content': 'Automated message', 'author': {'username': 'bot', 'is_bot': True}},
                'should_ignore': True
            },
            {
                'name': 'Anti-loop prefix',
                'data': {'content': '🤖🔒 Test message', 'author': {'username': 'user', 'is_bot': False}},
                'should_ignore': True
            }
        ]
        
        passed = 0
        for test in test_cases:
            result = filter.should_ignore_message(test['data'])
            if result == test['should_ignore']:
                passed += 1
                print(f"   ✅ {test['name']}")
            else:
                print(f"   ❌ {test['name']}")
                issues.append(f"Filter test failed: {test['name']}")
        
        print(f"   📊 Tests passed: {passed}/{len(test_cases)}")
        
    except Exception as e:
        issues.append(f"❌ Filter test failed: {str(e)}")
    
    return issues

def main():
    """Main health check function"""
    print("🏥 Discord Bot Health Check")
    print("=" * 50)
    
    all_issues = []
    
    # Run all checks
    all_issues.extend(check_environment())
    all_issues.extend(check_dependencies())
    all_issues.extend(check_files())
    all_issues.extend(check_webhook_server())
    all_issues.extend(check_n8n_connectivity())
    all_issues.extend(run_filter_tests())
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Health Check Summary")
    print("=" * 50)
    
    if not all_issues:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Bot is ready for deployment")
        return True
    else:
        print(f"⚠️  Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"   {issue}")
        
        print("\n💡 Next Steps:")
        print("   1. Fix the issues listed above")
        print("   2. Run this health check again")
        print("   3. Check DEPLOYMENT_GUIDE.md for detailed setup instructions")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Health check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Health check failed with error: {str(e)}")
        sys.exit(1)
