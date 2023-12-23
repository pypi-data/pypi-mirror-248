import unittest

from dotenv import load_dotenv

from capsphere.data.db import DbQueryService
from capsphere.data.db.connector.postgres import PostgresConnector
from capsphere.data.db.entity import LoanPaymentEntity

load_dotenv()


class TestLoanPaymentEntity(unittest.TestCase):
    db_query_service = DbQueryService(PostgresConnector())

    loan_payment_entity = LoanPaymentEntity(db_query_service)

    def test_get_by_loan_payment_ref_no(self):
        self.assertEqual(1, len(self.loan_payment_entity.get_by_loan_payment_ref_no('LPAY_183202262344BEA3B7CB')))
