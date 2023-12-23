from capsphere.data.db.entity.abstract_entity import DbEntity
from capsphere.data.db.helpers.utils import get_dataclass_list_from_query

from capsphere.data.db.service import DbQueryService
from capsphere.data.model.loan_payment import LoanPayment


class LoanPaymentEntity(DbEntity):
    def get_by_loan_payment_ref_no(self, loan_payment_ref_no: str) -> list[LoanPayment]:
        select_query = "SELECT * FROM loan_payments WHERE loan_payment_ref_no = %s"
        query_result = self.db_query_service.execute(select_query, (loan_payment_ref_no,), fetch_results=True)
        data = get_dataclass_list_from_query(query_result, LoanPayment)

        return data

    def create(self, payment: LoanPayment):
        # TODO logic.py line 19 CHECK
        insert_query = (
            "INSERT INTO loan_payments (loan_amount_paid, loan_payment_ref_no,"
            "loan_payment_processing_fee, loan_paid_uid,loan_id,created_by,"
            "updated_by,created_by_id,updated_by_id, loan_payment_type, manual_payment_proof_file, fpx_mode) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        return self.db_query_service.execute(insert_query, tuple(
            [payment.loan_amount_paid, payment.loan_payment_ref_no,
             payment.loan_payment_processing_fee, payment.loan_paid_uid, payment.loan_id, payment.created_by,
             payment.updated_by, payment.created_by_id, payment.updated_by_id, payment.loan_payment_type,
             payment.manual_payment_proof_file, payment.fpx_mode]), fetch_results=False)

    def update(self, payment: LoanPayment):
        loan_payment_ref_no = payment.loan_payment_ref_no
        if not loan_payment_ref_no:
            raise ValueError("payment_reference_no is required to update loan payment")

        verify_loan_exists = self.get_by_loan_payment_ref_no(loan_payment_ref_no)

        if not verify_loan_exists:
            raise ValueError(
                f"loan_payment_ref_no: {loan_payment_ref_no} does not exist in loan_payments table. Please check that "
                f"the loan payment record has already been created")

        update_query = (
            "UPDATE loan_payments SET fpx_mode = %s, "
            "loan_amount_verified = %s, loan_payment_status = %s, "
            "approved_at = %s WHERE loan_payment_ref_no=%s"
        )
        return self.db_query_service.execute(update_query, tuple(
            [payment.fpx_mode, payment.loan_amount_verified, payment.loan_payment_status, payment.approved_at,
             loan_payment_ref_no]), fetch_results=False)
