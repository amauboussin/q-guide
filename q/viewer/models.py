from django.db import models
import string


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
    recommend = models.DecimalField(decimal_places=2, null=True, max_digits=5, db_column='WouldYouRecommend', blank=True) # Field name made lowercase.

    def __unicode__(self):
        return self.field+' '+self.number+': '+self.title

    def get_absolute_url(self):
        return '/courses/%s/%s/%s/%s/' % (self.field, self.number, self.year, string.lower(self.term_text()))

    #gets a list of the professors who have taught this course.
    #returns a list of Qinstructors objects
    def get_profs(self):
        profs =  Qinstructors.objects.filter(course_id__exact = self.course_id)
        if profs:
            return profs
        else:
            return None

    def get_prof_chart(self):
        data = ""
        for p in Qinstructors.objects.filter(course_id__exact = self.course_id):
            scores = [
            {"label":"Overall", "value": float(p.overall)},
            {"label":"Lectures","value": float(p.lectures)},
            {"label":"Accessible", "value": float(p.accessible)},
            {"label":"Enthusiasm","value": float(p.enthusiasm)},
            {"label":"Discussion","value": float(p.discussion)},
            {"label": "Feedback","value": float(p.feedback)}
            ]

            data+= "{\n key:'"
            data+= p.__unicode__()+"'"
            data+=",\n values: " + str(scores)
            data+="\n},"
        return data

    #get the text representing this course's term
    def term_text(self):
        if self.term == 1:
            return 'Fall'
        elif self.term==2:
            return 'Spring'
        else: return 'Unknown'
    
    class Meta:
        db_table = u'Qcourses'

class Qcomments(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Qcourses)
    comment = models.CharField(max_length=24576)
    class Meta:
        db_table = u'Qcomments'


class Qfields(models.Model):
    field = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255,db_column='name')

    def __unicode__(self):
        if self.name != '':
            return self.name
        else:
            return self.field

    def get_absolute_url(self):
        return '/courses/'+self.field+'/'

    class Meta:
        db_table = u'Qfields'

class Qinstructors(models.Model):
    course = models.ForeignKey(Qcourses)
    id = models.IntegerField(primary_key=True)
    prof_id = models.CharField(max_length=255)
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

    def get_name(self):
        return self.first+' '+self.last

    def get_absolute_url(self):
        return '/profs/'+self.prof_id+'/'

    class Meta:
        db_table = u'Qinstructors'

