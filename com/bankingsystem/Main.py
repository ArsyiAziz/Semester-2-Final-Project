from com.bankingsystem.database.Portal import Portal


def __main():
    __portal = Portal.get_instance()
    __portal.interface()


if __name__ == '__main__':
    __main()