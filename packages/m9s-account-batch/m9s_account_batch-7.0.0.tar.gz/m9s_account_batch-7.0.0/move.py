# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.i18n import gettext
from trytond.model import fields
from trytond.model.exceptions import AccessError
from trytond.modules.account.move import _MOVE_STATES
from trytond.pool import Pool, PoolMeta


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    reference = fields.Char('Reference', states=_MOVE_STATES)

    @classmethod
    def post(cls, moves):
        BatchLine = Pool().get('account.batch.line')

        ids = [m.id for m in moves]
        batch_lines = BatchLine.search([
                ('move', 'in', ids),
                ])
        for line in batch_lines:
            line.set_code()
        return super(Move, cls).post(moves)

    @classmethod
    def _get_origin(cls):
        return super()._get_origin() + ['account.batch.line']


class MoveLine(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    reference = fields.Char('Reference')

    @classmethod
    def _get_origin(cls):
        return super()._get_origin() + ['account.batch.line']


    @classmethod
    def check_account(cls, lines, field_names=None):
        '''
        We must override completely, because this check is not extensible
        - Instead of the upstream implementation we allow a party to be set
          even if the account is not set to party required.
          This is needed, because we get the VAT-ID from the party
          for reverse-charge moves (where VAT-ID is required, but not party).
          Also there is no reason to not allow to set a party on a move line
          just for reference.
        '''
        if field_names and not (field_names & {'account', 'party'}):
            return
        for line in lines:
            if not line.account.type:
                raise AccessError(
                    gettext('account_batch.msg_line_missing_type',
                        account=line.account.rec_name))
            if line.account.closed:
                raise AccessError(
                    gettext('account_batch.msg_line_closed_account',
                        account=line.account.rec_name))
            if line.account.party_required and not line.party:
                raise AccessError(
                    gettext('account.msg_line_party_required',
                        account=line.account.rec_name,
                        line=line.rec_name))
