#!/bin/bash
# Quick Reference - Common Deployment Commands

echo "BloodBridge Deployment - Quick Reference"
echo "========================================"
echo ""

# Check if we're on EC2
if [ ! -d "/home/ubuntu/bloodbank" ]; then
    echo "⚠️  This script should be run on the EC2 instance"
    exit 1
fi

cd /home/ubuntu/bloodbank/backend

# Function to show menu
show_menu() {
    echo ""
    echo "Select an option:"
    echo "1. Check application status"
    echo "2. View application logs"
    echo "3. Restart application"
    echo "4. Run database migrations"
    echo "5. Test database connection"
    echo "6. Test API health"
    echo "7. Restart Nginx"
    echo "8. View Nginx logs"
    echo "9. Exit"
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Enter choice [1-9]: " choice
    
    case $choice in
        1)
            echo "📊 Application Status:"
            sudo systemctl status bloodbank --no-pager
            ;;
        2)
            echo "📋 Application Logs (Ctrl+C to exit):"
            sudo journalctl -u bloodbank -f
            ;;
        3)
            echo "🔄 Restarting application..."
            sudo systemctl restart bloodbank
            sleep 2
            sudo systemctl status bloodbank --no-pager
            ;;
        4)
            echo "🗄️  Running database migrations..."
            source venv/bin/activate
            python scripts/migrate_db.py
            ;;
        5)
            echo "🔌 Testing database connection..."
            source venv/bin/activate
            python -c "from services.rds_service import RDSService; from config import config; db = RDSService(config['production']()); print('✅ Connected!' if db.health_check() else '❌ Failed')"
            ;;
        6)
            echo "🏥 Testing API health..."
            curl -s http://localhost:5000/health | python3 -m json.tool
            ;;
        7)
            echo "🔄 Restarting Nginx..."
            sudo systemctl restart nginx
            sudo systemctl status nginx --no-pager
            ;;
        8)
            echo "📋 Nginx Error Logs:"
            sudo tail -n 50 /var/log/nginx/error.log
            ;;
        9)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid option. Please try again."
            ;;
    esac
done
