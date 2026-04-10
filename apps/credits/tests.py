from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.credits.models import CreditRequest

class IntermediationFlowTests(APITestCase):

    def setUp(self):
        # Admin setup
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='adminpassword')
        
        self.company_data = {
            "username": "agrocompany",
            "email": "agro@company.com",
            "password": "testpassword123",
            "company_name": "AgroTech CA",
            "rif": "J-12345678"
        }
        
        self.producer_data = {
            "username": "juanproducer",
            "email": "juan@producer.com",
            "password": "testpassword123",
            "farm_name": "Finca La Esperanza",
            "address": "Llanos Venezolanos",
            "rif": "V-12345678",
            "national_id": "V-12345678",
            "total_area": "100.50",
            "cultivated_area": "50.00"
        }

    def test_full_intermediation_flow(self):
        # 1. Company Registration
        response = self.client.post('/api/accounts/register/company/', self.company_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        company_user = User.objects.get(username="agrocompany")
        self.assertEqual(company_user.company_profile.status, 'pending')

        # 2. Producer Registration
        response = self.client.post('/api/accounts/register/producer/', self.producer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        producer_user = User.objects.get(username="juanproducer")
        self.assertEqual(producer_user.producer_profile.total_area, 100.50)
        
        # 3. Admin verifies Company
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(f'/api/accounts/company/{company_user.company_profile.id}/review/', {"status": "verified"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        company_user.company_profile.refresh_from_db()
        self.assertEqual(company_user.company_profile.status, 'verified')
        self.assertIsNotNone(company_user.company_profile.is_verified_at)

        # 4. Company publishes credit plan
        self.client.force_authenticate(user=company_user)
        plan_data = {
            "title": "Maize Starter Pack",
            "description": "Credit for seeds",
            "agricultural_sector": "Agriculture",
            "min_amount": 500.00,
            "max_amount": 5000.00,
            "interest_rate": 5.5,
            "term_months": 12
        }
        response = self.client.post('/api/credits/plans/', plan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plan_id = response.data['id']

        # 5. Producer requests credit plan
        self.client.force_authenticate(user=producer_user)
        request_data = {
            "credit_plan": plan_id
        }
        response = self.client.post('/api/credits/applications/', request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        credit_request = CreditRequest.objects.get(id=response.data['id'])
        self.assertEqual(credit_request.producer, producer_user.producer_profile)
        self.assertEqual(credit_request.credit_plan.id, plan_id)

    def test_company_status_protection(self):
        # Register company
        self.client.post('/api/accounts/register/company/', self.company_data)
        company_user = User.objects.get(username="agrocompany")
        
        # Try to modify status yourself via the public Company Profile ViewSet
        self.client.force_authenticate(user=company_user)
        response = self.client.patch(f'/api/accounts/company/{company_user.company_profile.id}/', {"status": "verified"})
        
        # Status should remain pending due to read_only_fields
        company_user.company_profile.refresh_from_db()
        self.assertEqual(company_user.company_profile.status, 'pending')
