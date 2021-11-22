from django.dispatch import Signal, receiver
track_activity_signal = Signal(providing_args=['timestamp'])

@receiver(track_activity_signal)
def track_activity(sender, **kwargs):
    sender.last_activity = kwargs.get('timestamp')
    sender.save()
