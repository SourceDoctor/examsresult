from examsresult.models import Version
from examsresult.models import db_version as db_max_version


class DBUpdater(object):

    # Fixme: get DB Updater to run, so it can update DB Models

    def __init__(self, session):
        self.session = session

    @property
    def version_difference(self):
        _version = self.session.query(Version).filter(Version.key == 'db_version').first()
        try:
            db_version = int(_version.value)
        except AttributeError:
            db_version = 0

        if db_version < db_max_version:
            return 1
        elif db_version > db_max_version:
            return -1
        else:
            return 0

    # def _update_v2_to_v3(self):
    #     # update DB Model to v3
    #     pass

    # def _update_v1_to_v2(self):
    #     # update DB Model to v2
    #     pass

    def _update_v0_to_v1(self):
        # update DB Model to v1
        pass

    def dbupdater(self):
        _version = self.session.query(Version).filter(Version.key == 'db_version').first()
        try:
            db_version = int(_version.value)
        except AttributeError:
            db_version = 0

        # DB Version to high for this System?
        if db_version > db_max_version:
            return -1

        old_db_version = db_version
        handle_db_version = db_version

        while handle_db_version < db_max_version:
            handle_db_version += 1

            # Update DB Model
            if not hasattr(self, "_update_v%d_to_v%d" % (handle_db_version - 1, handle_db_version)):
                print("Function to update DB to Model Version %d not found" % handle_db_version)
                return 0
            getattr(self, "_update_v%d_to_v%d" % (handle_db_version - 1, handle_db_version))()

            # update DB Model Version
            p = self.session.query(Version).filter(Version.key == 'db_version').first()
            if not p:
                p = Version(key='db_version', value=handle_db_version)
            else:
                p.value = handle_db_version
            self.session.add(p)
            self.session.commit()

        return 1
