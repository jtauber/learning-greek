from django.dispatch import receiver

from account.signals import password_changed
from account.signals import user_sign_up_attempt, user_signed_up
from account.signals import user_login_attempt, user_logged_in

from eventlog.models import log

from learning_greek.signals import adoption_level_change, blurb_read
from learning_greek.activities.signals import activity_start, activity_play


@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_LOGGED_IN",
        extra={}
    )


@receiver(password_changed)
def handle_password_changed(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="PASSWORD_CHANGED",
        extra={}
    )


@receiver(user_login_attempt)
def handle_user_login_attempt(sender, **kwargs):
    log(
        user=None,
        action="LOGIN_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_sign_up_attempt)
def handle_user_sign_up_attempt(sender, **kwargs):
    log(
        user=None,
        action="SIGNUP_ATTEMPTED",
        extra={
            "username": kwargs.get("username"),
            "email": kwargs.get("email"),
            "result": kwargs.get("result")
        }
    )


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get("user"),
        action="USER_SIGNED_UP",
        extra={}
    )


@receiver(adoption_level_change)
def handle_adoption_level_change(sender, **kwargs):
    log(
        user=kwargs.get("request").user,
        action="ADOPTION_LEVEL_CHANGE",
        extra={
            "level": kwargs.get("level"),
        }
    )


@receiver(blurb_read)
def handle_blurb_read(sender, **kwargs):
    log(
        user=kwargs.get("request").user,
        action="BLURB_READ",
        extra={}
    )


@receiver(activity_start)
def handle_activity_start(sender, **kwargs):
    log(
        user=kwargs.get("request").user,
        action="ACTIVITY_START",
        extra={
            "slug": kwargs.get("slug"),
            "activity_state_pk": kwargs.get("activity_state").pk,
        }
    )


@receiver(activity_play)
def handle_activity_play(sender, **kwargs):
    if kwargs.get("request").method == "POST":
        log(
            user=kwargs.get("request").user,
            action="ACTIVITY_PLAY_POST",
            extra={
                "slug": kwargs.get("slug"),
                "activity_occurence_state_pk": kwargs.get("activity_occurrence_state").pk,
                "post": {
                    key: value for key, value in kwargs.get("request").POST.items()
                    if key != u"csrfmiddlewaretoken"
                },
            }
        )
    else:
        log(
            user=kwargs.get("request").user,
            action="ACTIVITY_PLAY_GET",
            extra={
                "slug": kwargs.get("slug"),
                "activity_occurence_state_pk": kwargs.get("activity_occurrence_state").pk,
            }
        )
