from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, BooleanField


class InputForm(FlaskForm):
    att_flagship = IntegerField("Attacker Flagship", default=0)
    def_flagship = IntegerField("Defender Flagship", default=0)

    att_warsun = IntegerField("Attacker War Sun", default=0)
    def_warsun = IntegerField("Defender War Sun", default=0)

    att_dread = IntegerField("Attacker Dreadnought", default=0)
    def_dread = IntegerField("Defender Dreadnought", default=0)

    att_cruiser = IntegerField("Attacker Cruiser", default=0)
    def_cruiser = IntegerField("Defender Cruiser", default=0)

    att_carrier = IntegerField("Attacker Carrier", default=0)
    def_carrier = IntegerField("Defender Carrier", default=0)

    att_destroyer = IntegerField("Attacker Destroyer", default=0)
    def_destroyer = IntegerField("Defender Destroyer", default=0)

    att_fighter = IntegerField("Attacker Fighter", default=0)
    def_fighter = IntegerField("Defender Fighter", default=0)

    att_mech = IntegerField("Attacker Mech", default=0)
    def_mech = IntegerField("Defender Mech", default=0)

    att_infantry = IntegerField("Attacker Infantry", default=0)
    def_infantry = IntegerField("Defender Infantry", default=0)

    att_pds = IntegerField("Attacker PDS", default=0)
    def_pds = IntegerField("Defender PDS", default=0)

    ground_combat = BooleanField("Ground Combat", default=False)

    submit = SubmitField("Calculate")
