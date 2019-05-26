from examsresult.models import Version
from examsresult.models import db_version as db_max_version, DB_VERSION_KEY, SYSTEM_VERSION_KEY


class DBUpdater(object):

    def __init__(self, session):
        self.session = session

    @property
    def version_difference(self):
        _version = self.session.query(Version).filter(Version.key == DB_VERSION_KEY).first()
        try:
            db_version = int(_version.value)
        except AttributeError:
            # no db_version given -> new Database, so it's db_max_version
            p = Version(key=DB_VERSION_KEY, value=db_max_version)
            db_version = db_max_version
            self.session.add(p)
            self.session.commit()

        return db_max_version - db_version

    def _update_v3_to_v4(self):
        # update system to v4
        p = self.session.query(Version).filter(Version.key == SYSTEM_VERSION_KEY).first()
        p.value = 'v1.0.5.1'
        self.session.add(p)
        self.session.commit()

    def _update_v2_to_v3(self):
        # update system to v3
        self.session.execute("alter table student add column image VARCHAR(64)")
        system_version = Version(key=SYSTEM_VERSION_KEY,
                                 value='v1.0.5.0')
        self.session.add(system_version)
        self.session.commit()

    def _update_v1_to_v2(self):
        # update system to v2
        self.session.execute("alter table student add column real_school_class_name_id INTEGER default 0")
        self.session.execute("alter table school_class add column combined_schoolclass BOOLEAN default 0")

    def _update_v0_to_v1(self):
        # update system to v1
        pass

    def dbupdater(self):
        # DB Version to high for this System?
        version_difference = self.version_difference
        if version_difference < 0:
            return version_difference

        _version = self.session.query(Version).filter(Version.key == DB_VERSION_KEY).first()
        try:
            db_version = int(_version.value)
        except AttributeError:
            db_version = 0

        while db_version < db_max_version:
            db_version += 1

            # Update DB Model
            if not hasattr(self, "_update_v%d_to_v%d" % (db_version - 1, db_version)):
                print("Function to update DB to Model Version %d not found" % db_version)
                return 0
            getattr(self, "_update_v%d_to_v%d" % (db_version - 1, db_version))()

            # update DB Model Version
            p = self.session.query(Version).filter(Version.key == DB_VERSION_KEY).first()
            if not p:
                p = Version(key=DB_VERSION_KEY, value=db_version)
            else:
                p.value = db_version
            self.session.add(p)
            self.session.commit()

        return 1
