from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


class UrlManager(models.Manager):
    def shorten_model_object(self, obj):
        """
        Shorten URL of any object that implements get_absolute_url method and returns valid URL
        """
        try:
            url = obj.get_absolute_url()
        except AttributeError:
            raise NotImplementedError('Object passed to this method need to implement get_absolute_url method')

        return self.create(url=url)


class Url(models.Model):
    url = models.URLField(max_length=1000, help_text='Maximum 1000 characters.')
    slug = models.SlugField(help_text="Maximum 100 characters", blank=True, unique=True, max_length=100)
    slug_id = models.IntegerField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UrlManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return '{}, {}'.format(self.url, self.slug)

    @models.permalink
    def get_absolute_url(self):
        return 'chibi:short_url', (), {'slug': self.slug}

    def set_slug(self):
        self.slug_id = (Url.objects.all().aggregate(max_slug_id=Max('slug_id'))['max_slug_id'] or 0) + 1
        self.slug = self.get_code()

        while Url.objects.filter(slug=self.slug).exists():
            self.slug_id += 1
            self.slug = self.get_code()

    def get_code(self):
        string = "1aqzxsw23edcvfr45tgbnhy67ujmki89olp0QAZXRSWEDCVFTGBNHYUJMKIOLP"
        length = len(string)
        output = ""

        if self.id == 0:
            return string[0]

        number = self.slug_id
        while number != 0:
            i = number % length
            number /= length
            number = int(number)
            output = string[i] + output

        return output


# auto update url on first save and save social tags headers if celery is present
@receiver(pre_save, sender=Url)
def update_url(*args, **kwargs):
    instance = kwargs['instance']

    if instance.id is None and not instance.slug:
        instance.set_slug()


def generate_secret_key():
    return get_random_string(50)


class ApiToken(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50, unique=True, default=generate_secret_key)
    user = models.ForeignKey(User, on_delete=CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
