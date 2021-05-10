from django.db import models
from django.contrib.auth.models import (User, Group)
from django.contrib.postgres.fields import ArrayField


class Delegate(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    # When a user deletes their account, their user object is not deleted.
    # "is_active" field is set to 'False'.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # is_autogenerated is used for compatibility with an unreleased app.
    # do not use for RxC Voice or RxC Conversations
    is_autogenerated = models.BooleanField(default=False, blank=True)
    GITHUB = 'git'
    TWITTER = 'twt'
    APPLICATION = 'app'
    OAUTH_CHOICES = (
        (GITHUB, 'Github'),
        (TWITTER, 'Twitter'),
        (APPLICATION, 'Application'),
    )
    oauth_provider = models.CharField(max_length=3, choices=OAUTH_CHOICES,
                              default=GITHUB)
    oauth_token = models.CharField(max_length=256, blank=True, null=True)
    oauth_token_secret = models.CharField(max_length=256, blank=True, null=True)
    is_verified = models.BooleanField(default=False, blank=True)
    public_username = models.CharField(max_length=64, blank=True, null=True)
    # Represented by path
    profile_pic = models.TextField(null=True, blank=True)
    # encrypted
    # phone_number = models.CharField(max_length=20, blank=True)
    invited_by = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.SET_NULL)
    credit_balance = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=0)  # must be staff to change from default

    def __str__(self):
        return self.user.email


class Election(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    negative_votes = models.BooleanField(default=True)
    # What icon should be used to represent voice credits. Represented by path.
    vote_token = models.TextField(
        blank=True, default='../../../frontend/public/black-square.png')
    # Number of voice credits each voter will start out with.
    num_tokens = models.DecimalField(
        default=99, blank=True, max_digits=4, decimal_places=0)
    groups = models.ManyToManyField(Group, blank=True, default=[])

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_vote", "Can vote"),
            ("can_view_results", "Can view results"),
        ]


class Proposal(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True)
    ballot_ratification = models.BooleanField(default=False)
    link = models.CharField(max_length=512, blank=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE,
                                 null=True, blank=False)
    credits_received = models.DecimalField(
        default=0, max_digits=10, decimal_places=0, editable=False)
    votes_received = models.DecimalField(
        default=0, max_digits=10, decimal_places=0, editable=False)

    def __str__(self):
        return self.title


class Vote(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    # When a user deletes their account, their user object is not deleted.
    # "is_active" field is set to 'False'.
    sender = models.ForeignKey(Delegate, null=True, on_delete=models.SET_NULL)
    proposal = models.ForeignKey(Proposal, on_delete=models.SET_NULL,
                                 null=True, blank=False)
    amount = models.DecimalField(
        default=0, max_digits=4, decimal_places=0)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.sender) + " " + str(self.amount) + " -> " + str(self.proposal)


class Conversation(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    uuid = models.CharField(max_length=256, null=True, editable=False)
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    show_report = models.BooleanField(default=False, blank=True)
    report_id = models.CharField(max_length=256, blank=True)
    groups = models.ManyToManyField(Group, blank=True, default=[])

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_view", "Can view"),
        ]


class Process(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    groups = models.ManyToManyField(Group, blank=True, default=[])
    delegates = models.ManyToManyField(Delegate, blank=True, default=[])
    matching_pool = models.DecimalField(
        default=0, max_digits=10, decimal_places=0, blank=True, null=True)
    conversation = models.OneToOneField(
        Conversation, null=True, on_delete=models.SET_NULL)
    curation_info = models.TextField(blank=True, null=True)
    top_posts = ArrayField(
        models.CharField(max_length=140), blank=True, null=True)
    election = models.OneToOneField(
        Election, null=True, on_delete=models.SET_NULL)
    DELEGATION = 'Delegation'
    DELIBERATION = 'Deliberation'
    ELECTION = 'Election'
    STATUS_CHOICES = (
        (DELEGATION, 'Delegation'),
        (DELIBERATION, 'Deliberation'),
        (ELECTION, 'Election'),
    )
    status = models.CharField(max_length=14, choices=STATUS_CHOICES,
                              default=DELEGATION)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "processes"
        permissions = [
            ("can_view", "Can view"),
        ]


class Transfer(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    sender = models.ForeignKey(
        Delegate, related_name="sender", null=True, on_delete=models.SET_NULL)
    recipient = models.CharField(max_length=64, blank=True, null=True)
    recipient_object = models.ForeignKey(
        Delegate, related_name="recipient_object", null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=0)
    date = models.DateTimeField(blank=False)
    PENDING = 'P'
    ACCEPTED = 'A'
    CANCELED = 'C'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (CANCELED, 'Canceled'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default=PENDING)
    process = models.ForeignKey(Process, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.sender) + " " + str(self.amount) + " -> " + self.recipient


class MatchPayment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    recipient = models.ForeignKey(
        Delegate, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=0)
    date = models.DateTimeField(blank=False)
    process = models.ForeignKey(Process, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.process) + " " + str(self.amount) + " -> " + str(self.recipient)
