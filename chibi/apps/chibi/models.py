from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Max
from django.db.models.functions import Length
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.crypto import get_random_string, RANDOM_STRING_CHARS


class UrlManager(models.Manager):
    def shorten_model_object(self, obj):
        """
        Shorten URL of any object that implements get_absolute_url method and returns valid URL
        """
        try:
            url = obj.get_absolute_url()
        except AttributeError:
            raise NotImplementedError("Object passed to this method need to implement get_absolute_url method")

        return self.create(url=url)


class Url(models.Model):
    url = models.URLField(max_length=1000, help_text="Maximum 1000 characters.")
    slug = models.SlugField(help_text="Maximum 100 characters", blank=True, unique=True, max_length=100)
    is_custom_slug = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UrlManager()

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return "{}, {}".format(self.url, self.slug)

    def get_domain_url(self):
        site_url = getattr(settings, "SITE_URL", "")
        return site_url + self.get_absolute_url()

    def get_absolute_url(self):
        return reverse("chibi:short_url", kwargs={"slug": self.slug})

    def set_slug(self):
        self.is_custom_slug = False
        length = self.get_slug_length()

        self.slug = get_random_string(length)

        while Url.objects.filter(slug=self.slug).exists():
            self.slug = get_random_string(length)

    def get_slug_length(self, offset=0):
        slug_length_query = Url.objects.all().annotate(slug_len=Length("slug"))
        max_slug_length = (slug_length_query.filter(is_custom_slug=False).aggregate(max_slug_length=Max("slug_len")))[
            "max_slug_length"
        ] or 1

        max_slug_length += offset
        num_urls_longest_slug = slug_length_query.filter(slug_len=max_slug_length).count()

        if num_urls_longest_slug < (len(RANDOM_STRING_CHARS) ** max_slug_length) * 0.4:
            return max_slug_length
        else:
            return self.get_slug_length(offset=offset + 1)


# auto update url on first save and save social tags headers if celery is present
@receiver(pre_save, sender=Url)
def update_url(*args, **kwargs):
    instance = kwargs["instance"]

    if instance.id is None and not instance.slug:
        instance.set_slug()


def generate_secret_key():
    return get_random_string(50)


class ApiToken(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50, unique=True, default=generate_secret_key)
    user = models.ForeignKey(User, on_delete=CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
