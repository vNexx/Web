# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from askmeapp.models import Question, Tag
from random import randint, choice
import os

class Command(BaseCommand):
    help = 'Add question tags'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=3,
                            help='Number of tags for a question'
                            )

    def handle(self, *args, **options):
        tags = [
            'JavaScript', 'Java', 'Django', 'Nginx', 'Gunicorn', 'C++', 'php', 'Android', 'Jquery', 'Python',
            'HTML', 'CSS', 'ios', 'MySQL',  'Ruby-on-rails', 'Windows', 'Docker'
        ]

        for tag in tags:
            if len(Tag.objects.filter(text=tag)) == 0:
                t = Tag()
                t.text = tag
                t.style_number = randint(1, 8)
                t.save()

        number = int(options['number'])

        tags = Tag.objects.all()
        #category = Category.objects.get(title = u'General')

        questions = Question.objects.all()

        for q in questions:
            if len(q.tags.all()) < number:
                for i in range(0, number - len(q.tags.all())):
                    t = choice(tags)

                    if t not in q.tags.all():
                        q.tags.add(t)
                        q.save()
            self.stdout.write('in question [%d] add tags' % q.id)
