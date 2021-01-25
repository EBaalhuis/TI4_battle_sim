from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, BooleanField, SelectField


class InputForm(FlaskForm):
    factions = ["Arborec", "Argent", "Creuss", "Empyrean", "Hacan", "Jol-Nar", "L1Z1X", "Letnev", "Mahact", "Mentak",
                "Muaat", "Naalu", "Naaz-Rokha", "Nekro", "Nomad", "Saar", "Sardakk", "Sol", "Titans", "Vuil'Raith",
                "Winnu", "Xxcha", "Yin", "Yssaril"]
    att_faction = SelectField("Attacker faction", choices=factions)
    def_faction = SelectField("Defender faction", choices=factions)

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

    # Technologies
    att_antimass = BooleanField("Antimass Deflectors", default=False)
    def_antimass = BooleanField("Antimass Deflectors", default=False)
    att_graviton = BooleanField("Graviton Laser System", default=False)
    def_graviton = BooleanField("Graviton Laser System", default=False)
    att_plasma = BooleanField("Plasma Scoring", default=False)
    def_plasma = BooleanField("Plasma Scoring", default=False)
    def_magen = BooleanField("Magen Defense Grid", default=False)
    def_magen_o = BooleanField("Magen Defense Grid Ω", default=False)
    att_x89 = BooleanField("X-89 Bacterial Weapon Ω", default=False)
    att_duranium = BooleanField("Duranium Armor", default=False)
    def_duranium = BooleanField("Duranium Armor", default=False)
    att_assault = BooleanField("Assault Cannon", default=False)
    def_assault = BooleanField("Assault Cannon", default=False)

    # Action Cards
    att_morale = BooleanField("Morale Boost 1st Round", default=False)
    def_morale = BooleanField("Morale Boost 1st Round", default=False)
    def_bunker = BooleanField("Bunker", default=False)
    def_experimental = BooleanField("Experimental Battlestation", default=False)
    att_prototype = BooleanField("Fighter Prototype", default=False)
    def_prototype = BooleanField("Fighter Prototype", default=False)
    att_fireteam = BooleanField("Fire Team", default=False)
    def_fireteam = BooleanField("Fire Team", default=False)
    att_maneuvering = BooleanField("Maneuvering Jets", default=False)
    def_maneuvering = BooleanField("Maneuvering Jets", default=False)
    att_waylay = BooleanField("Waylay", default=False)
    def_waylay = BooleanField("Waylay", default=False)
