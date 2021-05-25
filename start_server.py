from server import main
from server.database.db import session

if __name__ == '__main__':
    main()
    session.close()
