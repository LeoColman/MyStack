from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .managers import LabelManager, CategoryManager, SpanManager, TextLabelManager
from api.models import Project
from examples.models import Example
from label_types.models import CategoryType, SpanType, RelationType


class Label(models.Model):
    objects = LabelManager()

    prob = models.FloatField(default=0.0)
    manual = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Label):
    objects = CategoryManager()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    label = models.ForeignKey(to=CategoryType, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'example',
            'user',
            'label'
        )


class Span(Label):
    objects = SpanManager()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='spans'
    )
    label = models.ForeignKey(to=SpanType, on_delete=models.CASCADE)
    start_offset = models.IntegerField()
    end_offset = models.IntegerField()

    def validate_unique(self, exclude=None):
        allow_overlapping = getattr(self.example.project, 'allow_overlapping', False)
        is_collaborative = self.example.project.collaborative_annotation
        if allow_overlapping:
            super().validate_unique(exclude=exclude)
            return

        overlapping_span = Span.objects.exclude(id=self.id).filter(example=self.example).filter(
            models.Q(start_offset__gte=self.start_offset, start_offset__lt=self.end_offset) |
            models.Q(end_offset__gt=self.start_offset, end_offset__lte=self.end_offset) |
            models.Q(start_offset__lte=self.start_offset, end_offset__gte=self.end_offset)
        )
        if is_collaborative:
            if overlapping_span.exists():
                raise ValidationError('This overlapping is not allowed in this project.')
        else:
            if overlapping_span.filter(user=self.user).exists():
                raise ValidationError('This overlapping is not allowed in this project.')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def is_overlapping(self, other: 'Span'):
        return (other.start_offset <= self.start_offset < other.end_offset) or\
               (other.start_offset < self.end_offset <= other.end_offset) or\
               (self.start_offset < other.start_offset and other.end_offset < self.end_offset)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_offset__gte=0), name='startOffset >= 0'),
            models.CheckConstraint(check=models.Q(end_offset__gte=0), name='endOffset >= 0'),
            models.CheckConstraint(check=models.Q(start_offset__lt=models.F('end_offset')), name='start < end')
        ]


class TextLabel(Label):
    objects = TextLabelManager()
    example = models.ForeignKey(
        to=Example,
        on_delete=models.CASCADE,
        related_name='texts'
    )
    text = models.TextField()

    def is_same_text(self, other: 'TextLabel'):
        return self.text == other.text

    class Meta:
        unique_together = (
            'example',
            'user',
            'text'
        )


class Relation(models.Model):
    annotation_id_1 = models.IntegerField()
    annotation_id_2 = models.IntegerField()
    type = models.ForeignKey(RelationType, related_name='annotation_relations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, related_name='annotation_relations', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='annotation_relations', on_delete=models.CASCADE)

    def __str__(self):
        return self.__dict__.__str__()

    class Meta:
        unique_together = ('annotation_id_1', 'annotation_id_2', 'type', 'project')
