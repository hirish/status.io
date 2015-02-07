from statusio import db, app
from models import User

with app.app_context():
    db.create_all()

    henry = User('henry')
    james = User('james')
    adam  = User('adam')
    neil  = User('neil')
    kira  = User('kira')

    henry.friends = [james, adam]
    james.friends = [kira, henry, adam]
    adam.friends = [kira, neil]
    neil.friends = [henry, adam]
    kira.friends = [henry, james, adam, neil]
    

    db.session.add(henry)
    db.session.add(james)
    db.session.add(adam)
    db.session.add(neil)
    db.session.add(kira)

    db.session.commit()
