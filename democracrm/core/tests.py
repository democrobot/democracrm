from django.test import TestCase

from .models import CRMBase, CRMTreeBase

class CRMBaseTests(TestCase):

    def test_crm_base_creation(self):
        obj = CRMBase()
        with self.assertRaises(TypeError) as cm:  
            obj.save()  
        the_exception = cm.exception
        print(the_exception) 
        #self.assertEqual(the_exception.error_code, 3) 
