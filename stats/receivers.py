from django.dispatch import receiver
from stats.signals import trigger as trigger_signal
from stats.signals import offer_does_not_exist


@receiver(trigger_signal)
def on_trigger(sender, trigger, **kwargs):
    from stats.models import Offer

    offer = Offer.objects.get(pk=trigger.offer_id)

    if offer.action == Offer.ACTION_ONLY_EMAIL:
        notify_affiliate(trigger)
    elif offer.action == Offer.ACTION_PAUSE_IMMEDIATELY:
        unapprove_affiliate(trigger)


@receiver(trigger_signal)
def run_trigger_actions(sender, trigger, **kwargs):
    from stats.models import Action

    actions = Action.objects.filter(key=trigger.key)

    for action in actions:
        if action.action_type.name == 'notify':
            notify_affiliate(trigger)
        elif action.action_type.name == 'pause':
            unapprove_affiliate(trigger)


def notify_affiliate(trigger):
    from workers.notify.tasks.notify_affiliate import notify_affiliate
    notify_affiliate.delay(trigger)


def unapprove_affiliate(trigger):
    from workers.notify.tasks.notify_affiliate_unapprovement import notify_affiliate_unapprovement
    from workers.notify.tasks.notify_manager_unapprovement import notify_manager_unapprovement
    from workers.hasoffers_calls.tasks.unapprove_affiliate_offer import unapprove_affiliate_offer

    unapprove_affiliate_offer.delay(trigger)
    notify_affiliate_unapprovement.delay(trigger)
    notify_manager_unapprovement.delay(trigger)


@receiver(offer_does_not_exist)
def on_offer_does_not_exist(sender, offer_id, **kwargs):
    from workers.loaders.tasks.load_offer import load_offer

    load_offer.delay(offer_id)
