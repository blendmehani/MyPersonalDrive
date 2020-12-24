from django.db import models


class Requests(models.Model):
    full_name = models.CharField(verbose_name='Full Name', max_length=40)
    email = models.EmailField(verbose_name='Email Address', max_length=40)
    message = models.TextField(verbose_name='Message')
    staff = models.EmailField(verbose_name='Staff user working on the request',null=True, blank=True)
    is_new = models.BooleanField(verbose_name='Is it a new request?', default=True)
    is_registered = models.BooleanField(verbose_name="Is the user registered?", default=False)
    is_processed = models.BooleanField(verbose_name="Is it being processed?", default=False)
    is_finished = models.BooleanField(verbose_name='Is it finished?', default=False)
    is_informed = models.BooleanField(verbose_name='Is user informed?', default=False)
    request_date = models.DateTimeField(verbose_name='Date of request', auto_now_add=True)
    finished_date = models.DateTimeField(verbose_name='Date of finished request', null=True, blank=True)

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'
        ordering = ('is_new', 'request_date')

    def clean(self):
        if self.is_processed:
            self.is_new = False
        if self.is_finished:
            self.is_new = False
        if self.is_informed:
            self.is_new = False
        from accounts.models import User
        try:
            User.objects.get(email=self.email)
            result = True
        except User.DoesNotExist:
            result = False
        self.is_registered = result

    def __str__(self):
        return self.email
