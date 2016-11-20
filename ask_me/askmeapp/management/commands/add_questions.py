# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from askmeapp.models import Question, Tag, Category
from random import choice, randint
from faker import Factory
import os

class Command(BaseCommand):
    help = 'Creates questions'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=10,
                help='Number of questions to add'
        )

    def handle(self, *args, **options):
        fake = Factory.create()

        number = int(options['number'])

        users = User.objects.all()[1:]

        starts = (
                'How do I Sort a Multidimensional Array in PHP [duplicate]',
                'How to make recursive sorted list function work?',
                'How to sort a table with persian content column in SQL Server'                
                )
        tags = Tag.objects.all()
        categorys = Category.objects.all()

        for i in range(0, number):
            q = Question()

            q.title = fake.sentence(nb_words=randint(4, 6), variable_nb_words=True)
            q.text = u"%s %s %s" % (
                    choice(starts),
                    os.linesep,
                    fake.paragraph(nb_sentences=randint(4, 17), variable_nb_sentences=True),
                    )
            q.user = choice(users)
            q.rating = randint(-100, 1000)
            q.is_published = True
            #q.tag = choice(tags)
            q.category = choice(categorys)
            q.id = i
            q.save()
            self.stdout.write('add question [%d]' % (q.id))
