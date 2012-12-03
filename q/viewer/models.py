# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Qcomments(models.Model):
    number = models.CharField(max_length=384)
    cat_num = models.CharField(max_length=765)
    year = models.IntegerField() # changed to integer
    term = models.IntegerField()
    comment = models.CharField(max_length=24576)
    class Meta:
        db_table = u'Qcomments'

class Qcourses(models.Model):
    number = models.CharField(max_length=384)
    course_id = models.IntegerField(primary_key=True)
    cat_num = models.CharField(max_length=765)
    year = models.IntegerField() # changed to integer
    term = models.IntegerField()
    enrollment = models.IntegerField(null=True, db_column='Enrollment', blank=True) # Field name made lowercase.
    evaluations = models.IntegerField(null=True, db_column='Evaluations', blank=True) # Field name made lowercase.
    response_rate = models.DecimalField(decimal_places=2, null=True, max_digits=8, db_column='ResponseRate', blank=True) # Field name made lowercase.
    overall = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='CourseOverall', blank=True) # Field name made lowercase.
    materials = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Materials', blank=True) # Field name made lowercase.
    assignments = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Assignments', blank=True) # Field name made lowercase.
    feedback = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Feedback', blank=True) # Field name made lowercase.
    section = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Section', blank=True) # Field name made lowercase.
    workload = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Workload', blank=True) # Field name made lowercase.
    difficulty = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='Difficulty', blank=True) # Field name made lowercase.
    recommend = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='WouldYouRecommend', blank=True) # Field name made lowercase.

    class Meta:
        db_table = u'Qcourses'

class Qinstructors(models.Model):
    number = models.CharField(max_length=384)
    cat_num = models.CharField(max_length=765)
    year = models.IntegerField() # changed to integer
    term = models.IntegerField()
    instructor_id = models.CharField(max_length=765)
    first = models.CharField(max_length=384)
    last = models.CharField(max_length=384)
    overall = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='InstructorOverall', blank=True) # Field name made lowercase.
    lectures = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='EffectiveLecturesorPresentations', blank=True) # Field name made lowercase.
    accessible = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='AccessibleOutsideClass', blank=True) # Field name made lowercase.
    enthusiasm = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='GeneratesEnthusiasm', blank=True) # Field name made lowercase.
    facilitates_discussion = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='FacilitatesDiscussionEncouragesParticipation', blank=True) # Field name made lowercase.
    feedback = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='GivesUsefulFeedback', blank=True) # Field name made lowercase.
    returns_assignments = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='ReturnsAssignmentsinTimelyFashion', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Qinstructors'

