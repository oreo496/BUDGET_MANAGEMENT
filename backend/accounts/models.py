from django.db import models
import uuid
import bcrypt
from django.utils import timezone


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)  # TOTP secret
    backup_codes = models.TextField(blank=True, null=True)  # JSON array of backup codes
    sms_otp_enabled = models.BooleanField(default=False)
    sms_phone = models.CharField(max_length=20, blank=True, null=True)  # Phone for SMS OTP
    status = models.CharField(
        max_length=10,
        choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')],
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def get_uuid_string(self):
        """Return UUID string for the user id."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Always return True for authenticated users."""
        return True
    
    @property
    def is_active(self):
        """Check if user status is active."""
        return self.status == 'ACTIVE'
    
    @property
    def is_anonymous(self):
        """Always return False for non-anonymous users."""
        return False

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admins'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def get_uuid_string(self):
        """Return UUID string for the admin id."""
        return str(self.id)

    def __str__(self):
        return self.email


class SMSOtp(models.Model):
    """Store SMS OTP codes for verification."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_otps')
    code = models.CharField(max_length=6)  # 6-digit OTP
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # 10-minute expiry

    class Meta:
        db_table = 'sms_otps'

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_max_attempts_exceeded(self):
        return self.attempts >= self.max_attempts

    def __str__(self):
        return f"OTP for {self.user.username} (created {self.created_at})"

