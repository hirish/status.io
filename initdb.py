from statusio import db, app
from models import User

with app.app_context():
    db.create_all()

    henry = User('Mark Zuckerberg')
    james = User('Larry Page')
    adam  = User('Elon Musk')
    neil  = User('Marissa Mayer')
    kira  = User('Jack Dorsey')

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
