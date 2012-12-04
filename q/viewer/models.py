

from django.db import models



class Qcourses(models.Model):
    field = models.CharField(max_length=384)
    number = models.CharField(max_length=384)
    title = models.CharField(max_length=3072)
    description = models.CharField(max_length=6144, blank=True)
    prerequisites = models.CharField(max_length=3072, blank=True)
    notes = models.CharField(max_length=3072, blank=True)
    meetings = models.CharField(max_length=3072, blank=True)
    building = models.CharField(max_length=768, blank=True)
    room = models.CharField(max_length=384, blank=True)
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
    wouldyourecommend = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='WouldYouRecommend', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Qcourses'

class Qcomments(models.Model):
    course = models.ForeignKey(Qcourses)
    comment = models.CharField(max_length=24576)
    class Meta:
        db_table = u'Qcomments'


class Qfields(models.Model):
    field = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'Qfields'

class Qinstructors(models.Model):
    course = models.ForeignKey(Qcourses)
    id = models.CharField(max_length=255, primary_key=True)
    first = models.CharField(max_length=384)
    last = models.CharField(max_length=384)
    overall = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='InstructorOverall', blank=True) # Field name made lowercase.
    lectures = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='EffectiveLecturesorPresentations', blank=True) # Field name made lowercase.
    accessible = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='AccessibleOutsideClass', blank=True) # Field name made lowercase.
    enthusiasm = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='GeneratesEnthusiasm', blank=True) # Field name made lowercase.
    discussion = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='FacilitatesDiscussionEncouragesParticipation', blank=True) # Field name made lowercase.
    feedback = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='GivesUsefulFeedback', blank=True) # Field name made lowercase.
    returns_assignments = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='ReturnsAssignmentsinTimelyFashion', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.first+' '+self.last
    class Meta:
        db_table = u'Qinstructors'

