import pytest

from seaworthy.definitions import ContainerDefinition, VolumeDefinition


class DBBackupContainer(ContainerDefinition):

    WAIT_PATTERNS = (r"Ready for jobs run",)

    def __init__(self, name='db_backup', image='nthienan/db-backup', config_volume=None):
        super().__init__(name, image, self.WAIT_PATTERNS, wait_timeout=60)
        self.config_volume = config_volume

    def clean(self):
        pass

    def base_kwargs(self):
        return {
            "volumes": {
                self.config_volume.inner(): "/var/db-backup/config/db-backup.yaml"
            }
        }


cfg_vol = VolumeDefinition("socket")
container = DBBackupContainer(config_volume=cfg_vol)
fixture = container.pytest_fixture('db_backup_container', dependencies=["cfg_vol"])


def test_type(db_backup_container):
    output = db_backup_container.exec_cake('type')
    assert output == ['chocolate']
