import random
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from authentication.models import User
from django.test import TransactionTestCase
from brain.models import Animal, ScanRun

