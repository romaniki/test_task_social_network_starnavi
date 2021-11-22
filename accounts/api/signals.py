from django.dispatch import Signal, receiver
track_login_signal = Signal(providing_args=['timestamp'])


@receiver(track_login_signal)
def track_login(sender, **kwargs):
    """Update the last_login timestamp of the user"""
    sender.last_login = kwargs.get('timestamp')
    sender.save()
