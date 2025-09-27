"""
Test semplice per verificare il funzionamento del login senza Supabase
"""

class MockAuthService:
    """Servizio di autenticazione mock per test"""
    
    def __init__(self):
        self.authenticated = False
        self.current_user_role = None
        
    def login(self, username: str, password: str):
        """Mock login che accetta sempre admin/admin"""
        print(f"Mock login: {username}/{password}")
        
        if username == "admin" and password == "admin":
            self.authenticated = True
            self.current_user_role = "admin"
            return {
                "success": True,
                "user": {"email": "admin@test.com"},
                "role": "admin",
                "message": "Login test riuscito!"
            }
        else:
            return {
                "success": False,
                "user": None,
                "role": None,
                "message": "Credenziali di test errate. Usa admin/admin"
            }
    
    def is_authenticated(self):
        return self.authenticated
    
    def is_admin(self):
        return self.authenticated and self.current_user_role == "admin"
    
    def is_user(self):
        return self.authenticated and self.current_user_role == "user"
    
    def get_current_user_info(self):
        if self.authenticated:
            return {
                "id": "test-user",
                "email": "admin@test.com",
                "role": self.current_user_role,
                "full_name": "Test Admin"
            }
        return None

''