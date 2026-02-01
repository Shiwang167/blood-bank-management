import psycopg2
from psycopg2 import pool, extras
from psycopg2.extensions import AsIs
from config import Config
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class RDSService:
    """Service for PostgreSQL RDS operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # min and max connections
                self.config.DATABASE_URL
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        return self.connection_pool.getconn()
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        self.connection_pool.putconn(conn)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
    
    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            user_id = str(uuid.uuid4())
            query = """
                INSERT INTO users (user_id, name, email, password_hash, role, blood_type, phone, last_donation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id
            """
            cursor.execute(query, (
                user_id,
                user_data.get('name'),
                user_data.get('email'),
                user_data.get('password_hash'),
                user_data.get('role'),
                user_data.get('blood_type'),
                user_data.get('phone'),
                user_data.get('last_donation')
            ))
            
            conn.commit()
            cursor.close()
            return user_id
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error creating user: {e}")
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            
            cursor.close()
            return dict(user) if user else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            cursor.close()
            return dict(user) if user else None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def update_user(self, user_id, update_data):
        """Update user data"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic UPDATE query
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(user_id)
            
            query = f"UPDATE users SET {set_clause} WHERE user_id = %s"
            cursor.execute(query, values)
            
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error updating user: {e}")
            return False
        finally:
            if conn:
                self.return_connection(conn)
    
    # Blood request operations
    def create_request(self, request_data):
        """Create a new blood request"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            request_id = str(uuid.uuid4())
            query = """
                INSERT INTO blood_requests 
                (request_id, blood_type, quantity, urgency, status, hospital_name, 
                 patient_name, contact_number, notes, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING request_id
            """
            cursor.execute(query, (
                request_id,
                request_data.get('blood_type'),
                request_data.get('quantity'),
                request_data.get('urgency', 'normal'),
                request_data.get('status', 'open'),
                request_data.get('hospital_name'),
                request_data.get('patient_name'),
                request_data.get('contact_number'),
                request_data.get('notes'),
                request_data.get('created_by')
            ))
            
            conn.commit()
            cursor.close()
            return request_id
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error creating request: {e}")
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_request_by_id(self, request_id):
        """Get request by ID"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            query = """
                SELECT r.*, u.name as created_by_name 
                FROM blood_requests r
                LEFT JOIN users u ON r.created_by = u.user_id
                WHERE r.request_id = %s
            """
            cursor.execute(query, (request_id,))
            request = cursor.fetchone()
            
            cursor.close()
            return dict(request) if request else None
        except Exception as e:
            logger.error(f"Error getting request by ID: {e}")
            return None
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_requests_by_blood_type(self, blood_type, status=None):
        """Get requests by blood type"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            if status:
                query = """
                    SELECT r.*, u.name as created_by_name 
                    FROM blood_requests r
                    LEFT JOIN users u ON r.created_by = u.user_id
                    WHERE r.blood_type = %s AND r.status = %s
                    ORDER BY r.urgency DESC, r.created_at DESC
                """
                cursor.execute(query, (blood_type, status))
            else:
                query = """
                    SELECT r.*, u.name as created_by_name 
                    FROM blood_requests r
                    LEFT JOIN users u ON r.created_by = u.user_id
                    WHERE r.blood_type = %s
                    ORDER BY r.urgency DESC, r.created_at DESC
                """
                cursor.execute(query, (blood_type,))
            
            requests = cursor.fetchall()
            cursor.close()
            return [dict(req) for req in requests]
        except Exception as e:
            logger.error(f"Error getting requests by blood type: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_all_requests(self, status=None):
        """Get all requests, optionally filtered by status"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            if status:
                query = """
                    SELECT r.*, u.name as created_by_name 
                    FROM blood_requests r
                    LEFT JOIN users u ON r.created_by = u.user_id
                    WHERE r.status = %s
                    ORDER BY r.urgency DESC, r.created_at DESC
                """
                cursor.execute(query, (status,))
            else:
                query = """
                    SELECT r.*, u.name as created_by_name 
                    FROM blood_requests r
                    LEFT JOIN users u ON r.created_by = u.user_id
                    ORDER BY r.urgency DESC, r.created_at DESC
                """
                cursor.execute(query)
            
            requests = cursor.fetchall()
            cursor.close()
            return [dict(req) for req in requests]
        except Exception as e:
            logger.error(f"Error getting all requests: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    def update_request(self, request_id, update_data):
        """Update request data"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build dynamic UPDATE query
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(request_id)
            
            query = f"UPDATE blood_requests SET {set_clause} WHERE request_id = %s"
            cursor.execute(query, values)
            
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error updating request: {e}")
            return False
        finally:
            if conn:
                self.return_connection(conn)
    
    # Inventory operations
    def get_inventory(self, blood_type=None):
        """Get inventory for specific blood type or all"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            if blood_type:
                query = "SELECT * FROM inventory WHERE blood_type = %s"
                cursor.execute(query, (blood_type,))
                inventory = cursor.fetchone()
                result = dict(inventory) if inventory else None
            else:
                query = "SELECT * FROM inventory ORDER BY blood_type"
                cursor.execute(query)
                inventory = cursor.fetchall()
                result = [dict(item) for item in inventory]
            
            cursor.close()
            return result
        except Exception as e:
            logger.error(f"Error getting inventory: {e}")
            return None if blood_type else []
        finally:
            if conn:
                self.return_connection(conn)
    
    def update_inventory(self, blood_type, units_available, updated_by):
        """Update inventory for a blood type"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE inventory 
                SET units_available = %s, last_updated = CURRENT_TIMESTAMP, updated_by = %s
                WHERE blood_type = %s
            """
            cursor.execute(query, (units_available, updated_by, blood_type))
            
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error updating inventory: {e}")
            return False
        finally:
            if conn:
                self.return_connection(conn)
    
    def get_low_stock_items(self, threshold=5):
        """Get blood types with low stock"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            
            query = "SELECT * FROM inventory WHERE units_available < %s ORDER BY units_available ASC"
            cursor.execute(query, (threshold,))
            items = cursor.fetchall()
            
            cursor.close()
            return [dict(item) for item in items]
        except Exception as e:
            logger.error(f"Error getting low stock items: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    # Health check
    def health_check(self):
        """Check database connection health"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
        finally:
            if conn:
                self.return_connection(conn)
