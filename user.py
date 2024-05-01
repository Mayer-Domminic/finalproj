def login():
    print('Workout App')
    print('Please Log In')

    user = input('Username: ')
    # in the future i would validate this username
    # TODO
    # check if user exists, if yes pass find uid, if not create user

    return user


def user_inp(user):
    print('Choices [0, 1, 2, 3]:')
    print('[0] View Log')
    print('[1] View Workouts')
    print('[2] Find an exercise')
    print('[3] Quit')
    choice = input('Choice: ')

    while choice == 0 or 1 or 2:
        if choice == 0:
            log(user)
        elif choice == 1:
            workout(user)
        elif choice == 2:
            exercise(user)


# display items, then ask to perform crud
def log(user):
    # TODO
    pass

def workout(user):
    # TODO
    pass

def exercise(user):
    # TODO
    pass